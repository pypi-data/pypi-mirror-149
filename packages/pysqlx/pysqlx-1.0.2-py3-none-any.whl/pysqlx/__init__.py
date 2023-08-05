
from .clients import ClientFactory
from .structures import Database, Schema, Table

version_info = (1, 0, 2)

__version__ = '.'.join(
    tuple(
        str(x)
        for x in version_info
    )
)

__all__ = (
    'ClientFactory',
    'Database',
    'Schema',
    'Table',
)
