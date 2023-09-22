from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.identity.user import (
        RegistrationDataFactory,
        UserAssertion,
    )


@pytest.mark.django_db()
def test_user_update(
    as_user: User,
    as_user_client: Client,
    registration_data_factory: 'RegistrationDataFactory',
    assert_correct_user: 'UserAssertion',
) -> None:
    """Test that user update works with correct user data."""
    updated_data = {
        key_name: value_part
        for key_name, value_part in registration_data_factory().items()
        if not key_name.startswith('password') and key_name != 'email'
    }
    response = as_user_client.post(
        reverse('identity:user_update'),
        data=updated_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.get('Location') == reverse('identity:user_update')
    assert_correct_user(as_user.email, updated_data)
