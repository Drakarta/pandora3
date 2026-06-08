from sqlmodel import SQLModel, Field


class Server(SQLModel, table=True):
    server_id: int = Field(default=None, primary_key=True)

    # Voice channel IDs
    create_voice_channel_id: int
    waiting_room_channel_id: int
    afk_voice_channel_id: int

    # Text channel IDs
    quotes_channel_id: int
    daily_music_channel_id: int

    # Role IDs
    custom_role_divider_id: int
