<div align="center">

<img alt="Crudly" src="./.assets/crudly.png" height="200">

Super simple FastAPI CRUD generator for async SQLModel ORM

[<img alt="FastAPI" height=150 src="https://camo.githubusercontent.com/4ebb06d037b495f2c4c67e0ee4599f747e94e6323ece758a7da27fbbcb411250/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f6c6f676f2d6d617267696e2f6c6f676f2d7465616c2e706e67" />](https://fastapi.tiangolo.com) [<img alt="SQLModel" height=150 src="https://camo.githubusercontent.com/af233532c9930e308adc996aa83bb1dedcdda51a98bb9e252ca03e937767e919/68747470733a2f2f73716c6d6f64656c2e7469616e676f6c6f2e636f6d2f696d672f6c6f676f2d6d617267696e2f6c6f676f2d6d617267696e2d766563746f722e737667236f6e6c792d6c69676874" />](https://sqlmodel.tiangolo.com)


</div>

## ⚙️ Usage example

1. Create database model

> [!IMPORTANT]
> Model must have primary key `id` field to create CRUD for it with Crudly

`database/models.py`:

```python
from sqlmodel import SQLModel, Field

class Post(SQLModel, table=True):
    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    text: str = Field(nullable=False)

```

2. Create schemas for model object creation and updation:

`schemas/posts.py`:

```python
from pydantic import BaseModel

class PostCreateSchema(BaseModel):
    title: str
    text: str

class PostUpdateSchema(PostCreateSchema):
    pass

```

3. Create database async session generator

`database/session.py`:

```python
from typing import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = # URL to database

engine: AsyncEngine = create_async_engine(DATABASE_URL)

session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:    
    yield session_maker()

```

4. Create FastAPI app and include Crudly router to it

> [!NOTE]
> Crudly creates router without prefix

`app.py`:

```python
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

```

### Swagger

<img alt="Swagger" src="./.assets/swagger.png">

## ⚖️ License

See [LICENSE](./LICENSE)

## 🧑‍🤝‍🧑 Contributing

See [CONTRIBUTING](./CONTRIBUTING)

## ⭐ References

Project inspired by [igorbenav/FastCRUD](https://github.com/igorbenav/FastCRUD)