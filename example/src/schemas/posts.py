from pydantic import BaseModel

class PostCreateSchema(BaseModel):
    title: str
    text: str

class PostUpdateSchema(PostCreateSchema):
    pass
