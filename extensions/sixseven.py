import re
import hikari
import lightbulb
from util.extension import Extension, listener
from util.impersonate_webhook import ImpersonateWebhook

loader = lightbulb.Loader()

PATTERN = re.compile(r"\b6[\s\-./,\s]*7\b", re.IGNORECASE)


class SixSeven(Extension):
    @listener(hikari.GuildMessageCreateEvent)
    async def on_message_create(self, event: hikari.GuildMessageCreateEvent):
        if event.author.is_bot or not event.content:
            return
        if not PATTERN.search(event.content):
            return
        new_content = PATTERN.sub("[REDACTED]", event.content)
        await event.message.delete()
        webhook = ImpersonateWebhook(
            event.app, event.channel_id, event.guild_id, "67-Impersonator"
        )
        await webhook.impersonate_message(event.author.id, new_content)


extension = SixSeven()
