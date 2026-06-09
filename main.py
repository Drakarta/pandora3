import sys
import hikari
import lightbulb
from config.config import Config
import extensions
from database.database import db


class Bot(hikari.GatewayBot):
    def __init__(self):
        config_file = "config/config.toml"
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        self.config = Config(config_file)
        super().__init__(
            token=self.config.token,
            intents=hikari.Intents.ALL,
        )
        self.client = lightbulb.client_from_app(self)
        self.subscribe(hikari.StartingEvent, self.on_starting)
        self.subscribe(hikari.StoppingEvent, self.on_stopping)

    async def on_starting(self, event: hikari.StartingEvent):
        # Initialize the database and create tables
        db.initialize(self.config.database)
        await db.create_tables()

        # Load extensions
        await self.client.load_extensions_from_package(extensions)
        for ext in extensions.EXTENSIONS:
            await ext.extension.load(self)
        await self.client.start()

    async def on_stopping(self, event: hikari.StoppingEvent):
        # Unload extensions
        for ext in extensions.EXTENSIONS:
            await ext.extension.unload(self)

        # Close the database connection
        await db.close()

    async def on_started(self, event: hikari.StartedEvent):
        await self.update_presence(
            status=hikari.Status.IDLE,
            activity=hikari.Activity(
                name="Observing the box.",
                type=hikari.ActivityType.PLAYING,
            ),
        )

    def run(self):
        self.subscribe(hikari.StartedEvent, self.on_started)
        super().run()


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
