from typing import TYPE_CHECKING

import pytest
from django.test import Client
from mimesis import Field, Schema
from mimesis.locales import Locale

if TYPE_CHECKING:
    from plugins.identity.user import (
        RegistrationData,
        RegistrationDataFactory,
        UserAssertion,
        UserData,
    )

from server.apps.identity.models import User


@pytest.fixture()
def user_data(registration_data: 'RegistrationData') -> 'UserData':
    """
    We need to simplify registration data to drop passwords.

    Basically, it is the same as ``registration_data``, but without passwords.
    """
    return {
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.fixture()
def registration_data_factory(
    faker_seed: int,
) -> 'RegistrationDataFactory':
    """Returns factory for fake random data for regitration."""
    local_faker_seed = faker_seed

    def factory(**fields: 'RegistrationData') -> 'RegistrationData':
        # TODO спросить Никиту как такие моменты решать
        # реализовал через замыкание, чтобы иметь возможность получать
        # разные данные. При этом отталкиваться от faker_seed,
        # чтобы сохранить воспроизводимость для тестов
        nonlocal local_faker_seed  # noqa: WPS420
        mf = Field(locale=Locale.RU, seed=local_faker_seed)
        password = mf('password')  # by default passwords are equal
        schema = Schema(
            schema=lambda: {
                'email': mf('person.email'),
                'first_name': mf('person.first_name'),
                'last_name': mf('person.last_name'),
                'date_of_birth': mf('datetime.date'),
                'address': mf('address.city'),
                'job_title': mf('person.occupation'),
                'phone': mf('person.telephone'),
            },
            iterations=1,
        )
        local_faker_seed += 1
        return {
            **schema.create()[0],
            **{'password1': password, 'password2': password},
            **fields,
        }
    return factory


@pytest.fixture()
def registration_data(
    registration_data_factory: 'RegistrationDataFactory',
) -> 'RegistrationData':
    """We need to simplify registration data to register user."""
    return registration_data_factory()


@pytest.fixture()
def as_user(user_data: 'UserData') -> User:
    """Create a user using the provided user data."""
    return User.objects.create(**user_data)


@pytest.fixture()
def as_user_client(as_user: User, client: Client) -> Client:
    """A fixture function that returns a client logged in as a specific user."""
    client.force_login(as_user)
    return client


@pytest.fixture(scope='session')
def assert_correct_user() -> 'UserAssertion':
    """
    Fixtures are used to check User contains the correct user data.

    This particular fixture, `assert_correct_user`, is defined with
    the scope set to 'session', meaning it will be available for the entire
    session of tests.

    The fixture is a function that returns another function, `factory`. This
    inner function is used for creating assertions for a user object. It takes
    two parameters: `email` (str) and `expected` (dict). The `email` parameter
    is the email of the user to be retrieved from the database, and the
    `expected` parameter is a dictionary containing the expected data for the
    user.

    Within the `factory` function, the user object is retrieved from the
    database using the provided email. Several special assertions are made
    about the user object:
    - `id` is not None
    - `is_active` is True
    - `is_superuser` is False
    - `is_staff` is False

    After the special assertions, a loop iterates over the `expected`
    dictionary, comparing each field of the user object with its expected
    value. Any field that does not match its expected value will cause an
    assertion error.

    There is no return type specified for the `factory` function, as it does
    not return a value. Instead, it is used for its side effects of performing
    assertions.

    Returns:
        None
    """
    def factory(email: str, expected: 'UserData') -> None:
        user = User.objects.get(email=email)
        # Special fields:
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff
        # All other fields:
        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value
    return factory
