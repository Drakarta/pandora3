import lightbulb
from util.extension import Extension, listener
from database.database import db
from database.schema.server import Server

loader = lightbulb.Loader()


class Admin(Extension):
    pass


@loader.command
class Ping(lightbulb.SlashCommand, name="ping", description="Ping the bot."):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context):
        await ctx.respond("Pong!")


@loader.command
class Setup(
    lightbulb.SlashCommand, name="setup", description="Set up the server for the bot."
):
    create_voice_channel_id = lightbulb.string(
        "create_voice_channel_id",
        "The ID of the voice channel to create for users.",
        default=None,
    )
    waiting_room_channel_id = lightbulb.string(
        "waiting_room_channel_id",
        "The ID of the waiting room voice channel.",
        default=None,
    )
    afk_voice_channel_id = lightbulb.string(
        "afk_voice_channel_id", "The ID of the AFK voice channel.", default=None
    )
    quotes_channel_id = lightbulb.string(
        "quotes_channel_id",
        "The ID of the text channel to post quotes in.",
        default=None,
    )
    daily_music_channel_id = lightbulb.string(
        "daily_music_channel_id",
        "The ID of the text channel to post daily music in.",
        default=None,
    )
    custom_role_divider_id = lightbulb.string(
        "custom_role_divider_id",
        "The ID of the role to use as a divider for custom roles.",
        default=None,
    )

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context):
        kwargs = {
            "server_id": ctx.guild_id,
        }
        if self.create_voice_channel_id:
            kwargs["create_voice_channel_id"] = int(self.create_voice_channel_id)
        if self.waiting_room_channel_id:
            kwargs["waiting_room_channel_id"] = int(self.waiting_room_channel_id)
        if self.afk_voice_channel_id:
            kwargs["afk_voice_channel_id"] = int(self.afk_voice_channel_id)
        if self.quotes_channel_id:
            kwargs["quotes_channel_id"] = int(self.quotes_channel_id)
        if self.daily_music_channel_id:
            kwargs["daily_music_channel_id"] = int(self.daily_music_channel_id)
        if self.custom_role_divider_id:
            kwargs["custom_role_divider_id"] = int(self.custom_role_divider_id)

        async with db.session() as session:
            await session.merge(Server(**kwargs))

        await ctx.respond("Server setup saved.", ephemeral=True)


extension = Admin()
