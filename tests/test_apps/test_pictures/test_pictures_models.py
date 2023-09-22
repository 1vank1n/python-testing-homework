import pytest

from server.apps.pictures.models import FavouritePicture


@pytest.mark.django_db()
def test_favourite_picture_str(favourite_picture: FavouritePicture) -> None:
    """Test the __str__ method of the FavouritePicture model."""
    output = '<Picture {0} by {1}>'.format(
        favourite_picture.foreign_id,
        favourite_picture.user_id,
    )
    assert str(favourite_picture) == output
