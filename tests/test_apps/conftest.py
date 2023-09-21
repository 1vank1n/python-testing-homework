import random
from typing import Unpack

import pytest
from mimesis import Field, Schema
from mimesis.locales import Locale

from server.apps.identity.models import User
from plugins.identity.user import (
    RegistrationData,
    RegistrationDataFactory,
    UserAssertion,
    UserData,
)  # TODO не смог завести в ветвлении if TYPE_CHECKING:


@pytest.fixture()
def user_data(registration_data: 'RegistrationData') -> 'UserData':
    """
    We need to simplify registration data to drop passwords.
    Basically, it is the same as ``registration_data``, but without passwords.
    """
    return { # type: ignore[return-value]
        key_name: value_part
        for key_name, value_part in registration_data.items()
        if not key_name.startswith('password')
    }


@pytest.fixture()
def registration_data_factory(
    faker_seed: int,
) -> 'RegistrationDataFactory':
    """Returns factory for fake random data for regitration."""
    def factory(**fields: Unpack['RegistrationData']) -> 'RegistrationData':
        mf = Field(locale=Locale.RU, seed=faker_seed)
        password = mf('password') # by default passwords are equal
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
        return {
            **schema.create()[0], # type: ignore[misc]
            **{'password1': password, 'password2': password},
            **fields,
        }
    return factory


@pytest.fixture()
def registration_data(registration_data_factory: 'RegistrationDataFactory') -> 'RegistrationData':
    """
    We need to simplify registration data to register user
    """
    return registration_data_factory()


@pytest.fixture()
def expected_user_data(user_data: 'UserData') -> 'UserData':
      return user_data


@pytest.fixture(scope='session')
def assert_correct_user() -> UserAssertion:
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
