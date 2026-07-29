"""
GRAVITYp: Python library to study the optical appearance of spherically symmetric
compact objects in General Relativity.

Source:    https://github.com/alvaroslzar/GRAVITYp
"""
from importlib.metadata import metadata, PackageNotFoundError

__name__ = "gravityp"

try:
    _meta = metadata(__name__)
    __version__ = _meta["Version"]
    __author__ = _meta["Author"]
    __email__ = _meta["Author-email"]
    
except PackageNotFoundError:
    # Fallback if package is executed directly without pip installation
    __version__ = "0.0.1"
    __author__ = "G.J. Olmo, D. Rubiera-Garcia, J.L Rosa, D. S\'aez-Chill\'on and \'A. Salazar-Cuadros"
    __email__ = "a.salazar@uva.es"