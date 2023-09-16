from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()()
def test_GET_dashboard(client: Client, user: User) -> None:
    url = reverse('pictures:dashboard')
    client.force_login(user)

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
