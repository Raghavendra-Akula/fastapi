from src.db.models import User
from .schemas import UserCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import generate_passwd_hash
from sqlmodel import select


class UserService():
    async def get_user(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user
    
    async def user_exists(self, email: str, session:AsyncSession):
        user = await self.get_user(email, session)
        return True if user is not None else False
    
    async def create_user(self, user_data: UserCreateModel, session:AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(
            **user_data_dict
        )
        new_user.passwd_hash = generate_passwd_hash(user_data_dict['password'])
        new_user.role = "user"
        session.add(new_user)
        await session.commit()
        return new_user
