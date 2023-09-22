from typing import TYPE_CHECKING

import pytest
from mimesis import Field, Schema
from mimesis.locales import Locale

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture

if TYPE_CHECKING:
    from plugins.pictures.favourite import (
        FavouritePictureData,
        FavouritePictureDataFactory,
    )


@pytest.fixture()
def favourite_picture_data_factory(
    faker_seed: int,
) -> 'FavouritePictureDataFactory':
    """Returns factory for fake random data for favourite picture data."""
    def factory(**fields: 'FavouritePictureData') -> 'FavouritePictureData':
        mf = Field(locale=Locale.RU, seed=faker_seed)
        schema = Schema(
            schema=lambda: {
                'foreign_id': mf('random.randints')[0],
                'url': mf('internet.stock_image_url'),
            },
            iterations=1,
        )
        return {
            **schema.create()[0],
            **fields,
        }
    return factory


@pytest.fixture()
def favourite_picture_data(
    favourite_picture_data_factory: 'FavouritePictureDataFactory',
) -> 'FavouritePictureData':
    """A fixture that creates a favourite picture data object."""
    return favourite_picture_data_factory()


@pytest.fixture()
def favourite_picture(
    as_user: User,
    favourite_picture_data: 'FavouritePictureData',
) -> FavouritePicture:
    """
    Creates a favourite picture object.

    Using the given user and favourite picture data.
    """
    return FavouritePicture.objects.create(**{
        'user': as_user,
        **favourite_picture_data,
    })
