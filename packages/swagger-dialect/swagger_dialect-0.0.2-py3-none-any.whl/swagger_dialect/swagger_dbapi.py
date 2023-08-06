import yaml


class SwaggerDBAPI:
    def __init__(self, filename):
        self.filename = None
        self.schema = None
        self.load_yaml_file(filename)

    def load_yaml_file(self, filename):
        self.filename = filename
        with open(filename, "rb") as yaml_file:
            self.schema = yaml.safe_load(yaml_file)

    def get_swagger_version(self):
        if 'swaggerVersion' in self.schema:
            return self.schema['swaggerVersion']
        elif 'swagger' in self.schema:
            return self.schema['swagger']
        return None

    def close(self) -> None:
        pass

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def get_table_names(self):
        tables = []
        for definition, obj in self.schema["definitions"].items():
            # id type not set , then assume it is an object
            definition_type = obj.get("type", "object")
            match definition_type:
                case "object":
                    tables.append(definition)
                case default:
                    continue
        return tables

    def get_columns(self, table_name):
        """
        # TODO: handle x-sensitiveData
        """
        columns = []
        if table_name in self.schema["definitions"]:
            required_cols = self.schema["definitions"][table_name].get("required", [])
            for name, obj in self.schema["definitions"][table_name].get("properties", {}).items():
                column_type = obj.get("type")
                column_format = obj.get("format")
                if column_type in ("string", "integer", "number", "boolean"):
                    # regular column reference
                    columns.append({
                        "name": name,
                        "type": column_type,
                        "format": column_format,
                        "required": name in required_cols,
                        "comment": None,
                    })

                elif obj.get("$ref") and column_type is None:
                    # foreign key reference
                    ref_info = obj.get("$ref").split("/")
                    if len(ref_info) == 3 and ref_info[0] == "#" and ref_info[1] == "definitions":
                        ref_table = ref_info[2]
                        columns.append({
                            "name": name,
                            "type": "integer",
                            "format": "int64",
                            "required": name in required_cols,
                            "comment": None,
                            "referred_schema": None,
                            "referred_table": ref_table,
                            "referred_column": "id",
                            "referred_options": {},
                        })
                else:
                    continue

        return columns
