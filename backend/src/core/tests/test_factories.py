import pytest
from core.factories import UserFactory


@pytest.mark.django_db
class TestUserFactory:
    def test_user_factory(self):
        user = UserFactory()
        assert user.username.startswith("user")
        assert "@example.com" in user.email
        assert user.check_password("testpass123")
