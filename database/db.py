from sqlmodel import create_engine, SQLModel

engine = create_engine("sqlite:///database/database.db")
SQLModel.metadata.create_all(engine)
