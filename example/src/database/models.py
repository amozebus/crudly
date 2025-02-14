from sqlmodel import SQLModel, Field

class Post(SQLModel, table=True):
    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    text: str = Field(nullable=False)