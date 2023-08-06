"""
.. dialect:: swagger
:name: swagger
:dbapi: None
:connectstring: swagger:///swagger_yaml_file_path

from sqlalchemy.dialects import registry
registry.register("swagger", "swagger_dialect", "SwaggerDialect")
"""
from abc import ABC

from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy import types as sqlalchemy_types
from sqlalchemy.engine import reflection

import swagger_dialect

swagger_type_mappings = {
    "string": sqlalchemy_types.String,
    "string-date": sqlalchemy_types.Date,
    "string-date-time": sqlalchemy_types.DateTime,
    "integer": sqlalchemy_types.Integer,
    "integer-int32": sqlalchemy_types.Integer,
    "integer-int64": sqlalchemy_types.BigInteger,
    "number": sqlalchemy_types.Numeric,
    "number-double": sqlalchemy_types.Numeric,
    "boolean": sqlalchemy_types.Boolean,
}


def map_col_swagger_types(col_type, col_format=None):

    if col_format:
        map_type = f"{col_type}-{col_format}"
    else:
        map_type = col_type

    match col_type:
        case "string":
            return_map = swagger_type_mappings.get(map_type, sqlalchemy_types.String)
        case "integer":
            return_map = swagger_type_mappings.get(map_type, sqlalchemy_types.Integer)
        case "number":
            return_map = swagger_type_mappings.get(map_type, sqlalchemy_types.Numeric)
        case "boolean":
            return_map = sqlalchemy_types.Boolean
        case default:
            return_map = None

    return return_map


class SwaggerDialect(DefaultDialect, ABC):
    name = "swagger"
    paramstyle = "pyformat"

    def __init__(self, **kwargs):
        DefaultDialect.__init__(self, **kwargs)

    def get_swagger_columns(self, connection, table_name, schema=None, **kw):
        cols = [{'default': None,
                 'autoincrement': "auto",
                 'primary_key': False,
                 'type': map_col_swagger_types(col["type"], col["format"]),
                 'name': col["name"],
                 'nullable': not col["required"],
                 "referred_schema": col.get("referred_schema"),
                 "referred_table": col.get("referred_table"),
                 "referred_column": col.get("referred_column"),
                 "referred_options": col.get("referred_options", {}),
                 } for col in connection.connection.get_columns(table_name)]
        return cols

    @classmethod
    def dbapi(cls):
        return swagger_dialect

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        return connection.get_table_names()

    @reflection.cache
    def has_table(self, connection, table_name, schema=None, **kw):
        table_names = self.get_table_names(connection, schema)
        return table_name in table_names

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        cols = self.get_columns(connection, table_name, schema, **kw)
        primary_keys = []
        for col in cols:
            if col["primary_key"]:
                primary_keys.append(col["name"])
        return {"constrained_columns": primary_keys, "name": None}

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        """
        # TODO:             con_kw = {}
        #             for opt in ("onupdate", "ondelete"):
        #                 if spec.get(opt, False) not in ("NO ACTION", None):
        #                     con_kw[opt] = spec[opt]
        """
        cols = self.get_swagger_columns(connection, table_name, schema, **kw)
        fkeys = {}
        for col in cols:
            if col.get("referred_table"):
                fkey = fkeys.setdefault(col.get("referred_table"), {
                    "name": f"fk_{table_name}_{col['referred_table']}",
                    "constrained_columns": [],
                    "referred_schema": col["referred_schema"],
                    "referred_table": col["referred_table"],
                    "referred_columns": [],
                    "options": col["referred_options"],
                })
                fkey["constrained_columns"].append(col["name"])
                fkey["referred_columns"].append(col["referred_column"])
        return fkeys.values()

    @reflection.cache
    def get_unique_constraints(self, connection, table_name, schema=None, **kw):
        return []

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        return []

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        # identity_options is a string that starts with 'ALWAYS,' or
        # 'BY DEFAULT,' and continues with
        # START WITH: 1, INCREMENT BY: 1, MAX_VALUE: 123, MIN_VALUE: 1,
        # CYCLE_FLAG: N, CACHE_SIZE: 1, ORDER_FLAG: N, SCALE_FLAG: N,
        # EXTEND_FLAG: N, SESSION_FLAG: N, KEEP_VALUE: N
        cols = [{'type': sqlalchemy_types.BigInteger,
                 'name': "id",
                 "autoincrement": "auto",
                 "identity": {
                     "always": True,
                     "on_null": True,
                     "start": 1,
                     "increment" : 1},
                 'primary_key': True,
                 'nullable': False}]
        swagger_cols = self.get_swagger_columns(connection, table_name, schema, **kw)
        cols += [col for col in swagger_cols]
        return cols
