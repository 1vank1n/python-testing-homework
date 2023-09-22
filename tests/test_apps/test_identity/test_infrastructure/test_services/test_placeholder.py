import pytest

from server.apps.identity.intrastructure.services import placeholder
from server.apps.identity.models import User


@pytest.mark.django_db()
def test_serialize_user_with_date_of_birth(as_user: User) -> None:
    """Test the serialization of a user with the date of birth."""
    serialize_user = placeholder._serialize_user(as_user)  # noqa: WPS437
    date_of_birth = as_user.date_of_birth.strftime('%d.%m.%Y')
    assert serialize_user['birthday'] == date_of_birth


@pytest.mark.django_db()
def test_serialize_user_without_date_of_birth(as_user: User) -> None:
    """Test the serialization of a user without the date of birth."""
    as_user.date_of_birth = None
    serialize_user = placeholder._serialize_user(as_user)  # noqa: WPS437
    assert serialize_user['birthday'] == ''
