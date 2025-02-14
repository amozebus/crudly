from typing import Annotated, AsyncGenerator

from pydantic import BaseModel

from fastapi import APIRouter, Depends

from sqlmodel import SQLModel, select

from sqlmodel.ext.asyncio.session import AsyncSession

class Crudly:
    def __new__(
        self,
        model: type[SQLModel],
        db_session_generator: AsyncGenerator[AsyncSession, None],
        create_schema: type[BaseModel],
        update_schema: type[BaseModel],
    ) -> APIRouter:
        """
        ### Description:
        Creates APIRouter with CRUD methods
             
        ### Parameters:

        model: type[SQLModel] - SQLModel model type

        db_session_generator: AsyncGenerator[AsyncSession, None] - database `AsyncSession` type session async generator

        create_schema: type[BaseModel] - `model` creation schema

        update_schema: type[BaseModel] - `model` updation schema

        ### Usage example:
        ```python
        from fastapi import FastAPI

        from crudly import Crudly

        from database.models import Post
        from database.session import get_db_session

        from posts.schemas import PostCreateSchema, PostUpdateSchema

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
        """

        router = APIRouter()

        @router.post(
            "/",
            response_model=model,
            description=f"Create {model.__name__} object"
        )
        async def create(
            schema: create_schema, # type: ignore
            db_session: Annotated[AsyncSession, Depends(db_session_generator)]
        ):
            obj = model(**schema.model_dump())

            db_session.add(obj)
            await db_session.commit()
            await db_session.close()

            return obj
        
        @router.get(
            "/",
            response_model=list[model],
            description=f"Get {model.__name__} object"
        )
        async def read_all(
            db_session: Annotated[AsyncSession, Depends(db_session_generator)],
        ):
            result = await db_session.exec(select(model))
            await db_session.close()

            return result.all()

        @router.get(
            "/{id}",
            response_model=model,
            description=f"Get all {model.__name__} objects"
        )
        async def read(
            id: int,
            db_session: Annotated[AsyncSession, Depends(db_session_generator)],
        ):
            result = await db_session.exec(select(model).where(model.id == id))
            await db_session.close()

            return result.first()
        
        @router.patch(
            "/{id}",
            response_model=model,
            description=f"Update {model.__name__} object"
        )
        async def update(
            id: int,
            schema: update_schema, # type: ignore
            db_session: Annotated[AsyncSession, Depends(db_session_generator)],
        ):
            obj = await read(id, db_session)

            for k, v in schema.model_dump().items():
                setattr(obj, k, v)
            
            await db_session.add(obj)
            await db_session.commit()
            await db_session.close()

            return obj
    
        @router.delete(
            "/{id}",
            response_model=model,
            description=f"Delete {model.__name__} object"
        )
        async def delete(
            id: int,
            db_session: Annotated[AsyncSession, Depends(db_session_generator)],
        ):
            await db_session.delete(await read(id, db_session))
            await db_session.commit()
            await db_session.close()

            return {
                "message": "Object successfully deleted"
            }
        
        return router