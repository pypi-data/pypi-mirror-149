from sqlalchemy.dialects import registry
from .error import *
from .swagger_dbapi import SwaggerDBAPI
from .swagger_dialect import SwaggerDialect

# Globals https://www.python.org/dev/peps/pep-0249/#globals
apilevel: str = "2.0"
threadsafety: int = 3
paramstyle: str = "pyformat"


def connect(**kwargs):
    return SwaggerDBAPI(filename=kwargs.get("database"))


def register_swagger_dialect():
    registry.register("swagger", "swagger_dialect", "SwaggerDialect")


register_swagger_dialect()
