from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from tests.plugins.identity.user import (
        RegistrationData,
        UserAssertion,
        UserData,
    )


@pytest.mark.django_db()
def test_valid_registration(
	client: Client,
	registration_data: 'RegistrationData',
	expected_user_data: 'UserData',
	assert_correct_user: 'UserAssertion',
) -> None:
	"""Test that registration works with correct user data."""
	response = client.post(
		reverse('identity:registration'),
		data=registration_data,
	)
	assert response.status_code == HTTPStatus.FOUND
	assert response.get('Location') == reverse('identity:login')
	assert_correct_user(registration_data['email'], expected_user_data)

# @pytest.mark.django_db()()
# def test_GET_user_update(client: Client, user: User) -> None:
#     url = reverse('identity:user_update')
#     client.force_login(user)

#     response = client.get(url)

#     assert response.status_code == HTTPStatus.OK


# @pytest.mark.django_db()()
# def test_POST_user_update(client: Client, user: User, user_data) -> None:
#     url = reverse('identity:user_update')
#     client.force_login(user)
#     user_data['last_name'] += ' updated'

#     response = client.post(url, data=user_data)

#     updated_user = User.objects.get(pk=user.pk)
#     assert response.url == url
#     assert updated_user.last_name == user_data['last_name']


# @pytest.mark.django_db()()
# def test_POST_register(client: Client, user_data, password: str) -> None:
#     url = reverse('identity:registration')
#     users_count = User.objects.count()
#     user_data['password1'] = password
#     user_data['password2'] = password

#     client.post(url, data=user_data)

#     assert users_count + 1 == User.objects.count()
