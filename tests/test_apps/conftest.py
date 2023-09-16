import uuid

import pytest
from mimesis import Address, Datetime, Person
from mimesis.locales import Locale

from server.apps.identity.models import User


@pytest.fixture
def user_data():
    person: Person = Person(Locale.RU)
    return {
        'email': person.email(),
        'password':str(uuid.uuid4()),
        'first_name': person.first_name(),
        'last_name': person.last_name(),
        'date_of_birth': Datetime().date().strftime('%Y-%m-%d'),
        'address': Address().address(),
        'job_title': person.occupation(),
        'phone': person.phone_number(),
    }

@pytest.fixture
def password():
    person: Person = Person(Locale.RU)
    return person.password()

@pytest.fixture
@pytest.mark.django_db()()
def user(django_user_model: User, user_data) -> User:
    return django_user_model.objects.create_user(**user_data)
