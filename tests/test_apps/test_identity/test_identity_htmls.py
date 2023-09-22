from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db()
def test_registration_template(
    client: Client,
) -> None:
    """Test the registration template."""
    response = client.get(reverse('identity:registration'))
    template = 'identity/pages/registration.html'

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, template)


@pytest.mark.django_db()
def test_login_template(
    client: Client,
) -> None:
    """Test the login template."""
    response = client.get(reverse('identity:login'))
    template = 'identity/pages/login.html'

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, template)


@pytest.mark.django_db()
def test_user_update_template(
    as_user_client: Client,
) -> None:
    """Test the user_update template."""
    response = as_user_client.get(reverse('identity:user_update'))
    template = 'identity/pages/user_update.html'

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, template)
