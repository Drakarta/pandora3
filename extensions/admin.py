import lightbulb
from util.extension import Extension

loader = lightbulb.Loader()


class Admin(Extension):
    pass


@loader.command
class Ping(lightbulb.SlashCommand, name="ping", description="Ping the bot."):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context):
        await ctx.respond("Pong!")


extension = Admin()
