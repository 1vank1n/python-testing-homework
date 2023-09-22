import pytest
from mimesis import Field, Schema
from mimesis.locales import Locale

from server.apps.identity.models import _UserManager  # noqa: WPS450


@pytest.mark.django_db()
def test_user_manager_exception_for_create_user(faker_seed: int) -> None:
    """Test the exception when user hasnot email."""
    mf = Field(locale=Locale.RU, seed=faker_seed)
    schema = Schema(
        schema=lambda: {
            'email': '',
            'password': mf('password'),
        },
        iterations=1,
    )

    with pytest.raises(ValueError, match='Users must have an email address'):
        _UserManager().create_user(**schema.create()[0])
