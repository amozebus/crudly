from fastapi import FastAPI

from crudly import Crudly

from database.models import Post
from database.session import get_db_session

from schemas.posts import PostCreateSchema, PostUpdateSchema

app = FastAPI()

app.include_router(
    router=Crudly(
        model=Post,
        create_schema=PostCreateSchema,
        update_schema=PostUpdateSchema,
        db_session_generator=get_db_session
    ),
    prefix="/posts",
    tags=["Posts"]
)