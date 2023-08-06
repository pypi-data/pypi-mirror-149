"""MetadataClientApi class"""

from warnings import warn

from .metadata_client import MetadataClient


class MetadataClientApi(MetadataClient):
    def __init__(self, *args, **kwargs):
        warn(
            "MetadataClientApi is deprecated, use MetadataClient instead",
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
