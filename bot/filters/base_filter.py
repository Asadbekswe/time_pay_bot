import datetime

from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy import select

from database import User, Lead
from database.base import async_session


class IsUser(Filter):
    async def __call__(self, message: Message) -> bool:
        data = message.from_user.model_dump(include={"id", "first_name", "last_name", "username"})
        user = await User.get(data["id"])
        if not user:
            user = await User.create(**data)
        return user.type == User.Type.USER


class IsOperator(Filter):

    async def __call__(self, message: Message) -> bool:
        operator = await User.get(message.from_user.id)
        return operator.type == User.Type.OPERATOR


class IsAdmin(Filter):

    async def __call__(self, message: Message) -> bool:
        admin = await User.get(message.from_user.id)
        return admin.type == User.Type.ADMIN


class IsSuperUser(Filter):

    async def __call__(self, message: Message) -> bool:
        super_user = await User.get(message.from_user.id)
        return super_user.type == User.Type.SUPER_USER


# class DriverHasPermission(Filter):
#
#     async def __call__(self, message: Message) -> bool:
#         driver = await Driver.get_or_none(user_id=message.from_user.id)
#         return driver is not None and driver.has_permission
async def first_id_or_none(items: list):
    if items and len(items) > 0:
        item = items[0]
        if isinstance(item, dict):
            return item.get('id')
        return getattr(item, 'id', None)
    return None


async def get_leads(operator_id, start_date, end_date):
    async with async_session() as session:
        async with session.begin():
            stmt = (
                select(Lead)
                .where(
                    Lead.operator_id == operator_id,
                    Lead.status == Lead.Status.SOLD,
                    Lead.updated_at >= start_date,
                    Lead.updated_at < end_date
                )
            )
            result = await session.execute(stmt)
        return result.scalars().all()
