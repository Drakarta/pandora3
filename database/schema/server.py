from typing import Optional
from sqlmodel import SQLModel, Field


class Server(SQLModel, table=True):
    server_id: int = Field(primary_key=True)

    # Voice channel IDs
    create_voice_channel_id: Optional[int] = None
    waiting_room_channel_id: Optional[int] = None
    afk_voice_channel_id: Optional[int] = None

    # Text channel IDs
    quotes_channel_id: Optional[int] = None
    daily_music_channel_id: Optional[int] = None

    # Role IDs
    custom_role_divider_id: Optional[int] = None
