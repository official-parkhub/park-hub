from src.modules.shared.models.user.user import User
from uuid import uuid4
from faker import Faker


class UserBuilder:
    faker = Faker()

    def __init__(self):
        self.user = User(
            id=uuid4(),
            email=self.faker.email(),
            password_hash=self.faker.password(),
            is_admin=False,
        )

    def customize(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.user, key, value)
        return self

    def get_user(self) -> User:
        return self.user

    async def build(self, db) -> User:
        db.add(self.user)
        await db.flush()
        return self.user
