from fastapi import HTTPException, status

from sqlmodel import SQLModel

class ObjectNotFound(HTTPException):
    def __init__(self, model: type[SQLModel], id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} object with id {id} not found"
        )