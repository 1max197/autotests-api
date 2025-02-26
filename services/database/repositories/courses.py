import uuid
from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from services.database.client import get_database_session
from services.database.models import CoursesModel
from utils.clients.database.repository import BasePostgresRepository


class CoursesRepository(BasePostgresRepository):
    model = CoursesModel

    async def filter(self, user_id: uuid.UUID) -> Sequence[CoursesModel]:
        return await self.model.filter(
            self.session,
            options=(joinedload(self.model.preview_file), joinedload(self.model.created_by_user)),
            clause_filter=(self.model.created_by_user_id == user_id,)
        )

    async def get_by_id(self, course_id: uuid.UUID) -> CoursesModel | None:
        return await self.model.get(
            self.session,
            options=(joinedload(self.model.preview_file), joinedload(self.model.created_by_user)),
            clause_filter=(self.model.id == course_id,)
        )

    async def create(self, data: dict) -> CoursesModel:
        course = await self.model.create(self.session, **data)
        return await self.get_by_id(course.id)

    async def update(self, course_id: uuid.UUID, data: dict) -> CoursesModel:
        course = await self.model.update(
            self.session, clause_filter=(self.model.id == course_id,), **data
        )
        return await self.get_by_id(course.id)

    async def delete(self, course_id: uuid.UUID) -> None:
        return await self.model.delete(self.session, clause_filter=(self.model.id == course_id,))


async def get_courses_repository(
        session: Annotated[AsyncSession, Depends(get_database_session)]
) -> CoursesRepository:
    return CoursesRepository(session=session)
