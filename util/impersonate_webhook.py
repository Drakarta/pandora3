import hikari


class ImpersonateWebhook:
    def __init__(
        self, bot: hikari.GatewayBot, channel_id: int, guild_id: int, name: str
    ):
        self.bot = bot
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.name = name

    async def _get_or_create_webhook(self) -> hikari.webhooks:
        existing_webhooks: list[hikari.webhooks] = (
            await self.bot.rest.fetch_channel_webhooks(self.channel_id)
        )

        for webhook in existing_webhooks:
            if webhook.name == f"{self.name}-{self.channel_id}":
                return webhook
        return await self.bot.rest.create_webhook(
            self.channel_id, name=f"{self.name}-{self.channel_id}"
        )

    async def impersonate_message(self, user_id: int, content: str):
        webhook = await self._get_or_create_webhook()
        user = await self.bot.rest.fetch_member(self.guild_id, user_id)

        payload = {
            "content": content,
            "username": user.display_name,
            "avatar_url": user.display_avatar_url,
        }

        await webhook.execute(**payload)
