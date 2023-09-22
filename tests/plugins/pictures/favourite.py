from typing import Protocol, TypedDict, Unpack, final


@final
class FavouritePictureData(TypedDict, total=False):
    """Represent the simplified favourite picture data."""

    foreign_id: int
    url: str


class FavouritePictureDataFactory(Protocol):
    """Protocol for FavouritePictureData data factory."""

    def __call__(
        self,
        **fields: Unpack[FavouritePictureData],
    ) -> FavouritePictureData:
        """Favourite picture data factory protocol."""
