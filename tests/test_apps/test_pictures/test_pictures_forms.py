from typing import TYPE_CHECKING

import pytest

from server.apps.identity.models import User
from server.apps.pictures.intrastructure.django.forms import FavouritesForm
from server.apps.pictures.models import FavouritePicture

if TYPE_CHECKING:
    from plugins.pictures.favourite import FavouritePictureData


@pytest.mark.django_db()
def test_favourites_form(
    as_user: User,
    favourite_picture_data: 'FavouritePictureData',
) -> None:
    """
    Test the favourites form.

    This function is a unit test for the `FavouritesForm` class. It ensures
    that the form is correctly instantiated and that the expected assertions
    hold true.
    """
    favourite_picture = FavouritesForm(
        user=as_user,
        data=favourite_picture_data,
    ).save(commit=False)

    assert favourite_picture
    assert isinstance(favourite_picture, FavouritePicture)
    assert FavouritePicture.objects.count() == 0
