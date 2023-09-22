from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User

if TYPE_CHECKING:
    from plugins.pictures.favourite import FavouritePictureData


@pytest.mark.django_db()
def test_open_dashboard(as_user_client: Client) -> None:
    """Test the functionality of opening the dashboard."""
    response = as_user_client.get(reverse('pictures:dashboard'))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_add_to_favourites_on_dashboard(
    as_user: User,
    as_user_client: Client,
    favourite_picture_data: 'FavouritePictureData',
) -> None:
    """Test the functionality of adding a picture to favourites."""
    response = as_user_client.post(
        reverse('pictures:dashboard'),
        data=favourite_picture_data,
    )

    assert response.status_code == HTTPStatus.FOUND
    assert as_user.pictures.count() == 1


@pytest.mark.django_db()
def test_open_favourites(as_user_client: Client) -> None:
    """Test the functionality of opening favourites."""
    response = as_user_client.get(reverse('pictures:favourites'))

    assert response.status_code == HTTPStatus.OK
