from aiogram.filters import Filter
from aiogram.types import Message

from database import User


# class IsUser(Filter):
#
#     async def __call__(self, message: Message) -> bool:
#         user = await User.get(message.from_user.id)
#         return user.Type.USER == User.Type.USER


class IsOperator(Filter):

    async def __call__(self, message: Message) -> bool:
        operator = await User.get(message.from_user.id)
        return operator.Type.OPERATOR == User.Type.OPERATOR


class IsAdmin(Filter):

    async def __call__(self, message: Message) -> bool:
        admin = await User.get(message.from_user.id)
        return admin.Type.ADMIN == User.Type.ADMIN


class IsSuperUser(Filter):

    async def __call__(self, message: Message) -> bool:
        super_user = await User.get(message.from_user.id)
        return super_user.Type.SUPER_USER == User.Type.SUPER_USER

# class DriverHasPermission(Filter):
#
#     async def __call__(self, message: Message) -> bool:
#         driver = await Driver.get_or_none(user_id=message.from_user.id)
#         return driver is not None and driver.has_permission
