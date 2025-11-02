import pytest

from src.modules.shared.services.user import UserService
from src.modules.shared.schemas.user import UserCreateSchema


class TestUserService:
    @pytest.fixture(autouse=True)
    def setup(self, rc):
        self.service = UserService(rc)

    async def test_create_user_and_duplicate_email(self, faker):
        email = faker.unique.email()
        user = await self.service.create_user(
            UserCreateSchema(email=email, password=faker.password())
        )
        assert user.id
        assert user.email == email
        # Creating again with same email should raise
        with pytest.raises(Exception):
            await self.service.create_user(
                UserCreateSchema(email=email, password=faker.password())
            )

    async def test_get_user_by_id_not_found(self, faker):
        with pytest.raises(Exception):
            await self.service.get_user_by_id(faker.uuid4())
