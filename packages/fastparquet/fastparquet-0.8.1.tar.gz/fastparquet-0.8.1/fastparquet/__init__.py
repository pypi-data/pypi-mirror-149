"""parquet - read parquet files."""
__version__ = "0.8.1"

from .writer import write
from . import core, schema, converted_types, api
from .api import ParquetFile
from .util import ParquetException
