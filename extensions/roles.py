import re
import hikari
import lightbulb

from sqlmodel import select
from database.database import db
from database.schema.roles import Roles as UserRoles
from database.schema.server import Server

from util.extension import Extension, listener

loader = lightbulb.Loader()
colour_regex = re.compile(r"^(?:#[0-9A-Fa-f]{6}|0x#?[0-9A-Fa-f]{6}|[0-9A-Fa-f]{6})$")


class Roles(Extension):
    pass


@loader.command
class Role(lightbulb.SlashCommand, name="role", description="Manage roles."):
    name = lightbulb.string("name", "Set the name of your role.", default=None)
    colour = lightbulb.string(
        "colour",
        "Set the colour of your role in hex format (e.g., #FF0000).",
        default=None,
    )

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context):
        await ctx.defer(ephemeral=True)

        if not self.name and not self.colour:
            await ctx.edit_initial_response("You must provide a name or a colour.")
            return
        if self.colour and not colour_regex.match(self.colour):
            await ctx.edit_initial_response(
                "Invalid colour format. Please use hex format (e.g., #FF0000)."
            )
            return

        async with db.session() as session:
            result = await session.exec(
                select(UserRoles).where(UserRoles.user_id == ctx.user.id)
            )
            res = result.first()

        if not res:
            await self.create_role(ctx, self.name, self.colour)
            return

        await self.update_role(ctx, res.role_id, self.name, self.colour)

    async def create_role(self, ctx: lightbulb.Context, name: str, colour: str):
        kwargs = {}
        kwargs["guild"] = ctx.guild_id
        if name:
            kwargs["name"] = name
        else:
            kwargs["name"] = f"{ctx.user.display_name}'s Role"
        if colour:
            kwargs["colour"] = hikari.Colour.of(colour)

        role = await ctx.client.app.rest.create_role(**kwargs)

        async with db.session() as session:
            session.add(
                UserRoles(server_id=ctx.guild_id, user_id=ctx.user.id, role_id=role.id)
            )
            result = await session.exec(
                select(Server.custom_role_divider_id).where(
                    Server.server_id == ctx.guild_id
                )
            )
            divider_id = result.first()

        await ctx.client.app.rest.add_role_to_member(ctx.guild_id, ctx.user.id, role.id)

        if divider_id:
            divider = await ctx.client.app.rest.fetch_role(ctx.guild_id, divider_id)
            await ctx.client.app.rest.reposition_roles(
                ctx.guild_id,
                {divider.position: int(role.id)},
            )

        await ctx.edit_response(
            "@original", content=f'Role "{role.name}" created and assigned to you.'
        )

    async def update_role(
        self, ctx: lightbulb.Context, role_id: int, name: str | None, colour: str | None
    ):
        role = await ctx.client.app.rest.fetch_role(ctx.guild_id, role_id)
        kwargs = {}
        if name:
            kwargs["name"] = name
        if colour:
            kwargs["colour"] = hikari.Colour.of(colour)

        await ctx.client.app.rest.edit_role(ctx.guild_id, role_id, **kwargs)

        await ctx.edit_response(
            "@original", content=f'Role "{role.name}" updated successfully.'
        )


extension = Roles()
