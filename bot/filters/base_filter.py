from aiogram.filters import Filter
from aiogram.types import Message

from database import User


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
    """
    Listning birinchi elementidan 'id' qiymatini qaytaradi.
    Agar list bo'sh bo'lsa yoki 'id' bo'lmasa, None qaytaradi.
    """
    if items and len(items) > 0:
        item = items[0]
        # Agar bu dict bo'lsa (values qaytarilgan bo'lsa)
        if isinstance(item, dict):
            return item.get('id')
        # Agar bu model bo'lsa (Tortoise yoki SQLAlchemy obyekti)
        return getattr(item, 'id', None)
    return None
