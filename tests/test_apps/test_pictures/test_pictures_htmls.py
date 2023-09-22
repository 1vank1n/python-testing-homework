from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture


@pytest.mark.django_db()
def test_favourites_template(
    as_user: User,
    as_user_client: Client,
    favourite_picture: FavouritePicture,
) -> None:
    """Test the favourites template."""
    data_test_id = 'data-test-id="favourites-picture-db"'
    response = as_user_client.get(reverse('pictures:favourites'))
    template = 'pictures/pages/favourites.html'

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, template)
    assert as_user == favourite_picture.user
    assert data_test_id in response.content.decode('utf-8')
