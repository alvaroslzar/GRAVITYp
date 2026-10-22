"""Optical appearance of spherically symmetric compact objects in General
Relativity.

Source: https://github.com/alvaroslzar/GRAVITYp
"""

from .compact_object import *
from .zoo import *
from .geodesic_integration import *
from .ray_tracing import *
from .rings import *
from .transfer_functions import *
from .emission_models import *
from .shadows import *
from .plots import *

from . import (compact_object, zoo, geodesic_integration, ray_tracing, rings,
               transfer_functions, emission_models, shadows, plots)

# Written as `+=` statements so static analysers (e.g. Pylance) can follow them
__all__ = []
__all__ += compact_object.__all__
__all__ += zoo.__all__
__all__ += geodesic_integration.__all__
__all__ += ray_tracing.__all__
__all__ += rings.__all__
__all__ += transfer_functions.__all__
__all__ += emission_models.__all__
__all__ += shadows.__all__
__all__ += plots.__all__


def _package_metadata():
    """Returns (version, author, email) from the installed package metadata"""
    # Imported here so they don't leak into the gravityp namespace
    import email.utils
    from importlib.metadata import metadata, PackageNotFoundError

    try:
        meta = metadata("gravityp")
    except PackageNotFoundError:
        return None, None, None

    # setuptools packs pyproject.toml authors into the 'Author-email' header
    author_email_header = meta.get("Author-email")
    if not author_email_header:
        return meta.get("Version"), meta.get("Author"), None

    # Parse header into [("Name", "email@domain.com"), ...]
    contacts = email.utils.getaddresses([author_email_header])
    names = [name for name, _ in contacts if name]
    emails = [addr for _, addr in contacts if addr]

    # Format as strings so help(gravityp) displays them cleanly
    author = ", ".join(names) if names else meta.get("Author")
    return meta.get("Version"), author, ", ".join(emails) if emails else None


__version__, __author__, __email__ = _package_metadata()
del _package_metadata
