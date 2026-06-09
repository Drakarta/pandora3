from sqlmodel import SQLModel, Field


class Roles(SQLModel, table=True):
    server_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, primary_key=True)
    role_id: int
