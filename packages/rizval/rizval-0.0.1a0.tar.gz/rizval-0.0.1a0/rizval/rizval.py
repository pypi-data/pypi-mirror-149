from . import types


class Schema:
    def __init__(self, type):
        print(type(self))
        self.type = type
        self.type_name = types.get_type_name(type)

    def assert_validation(self, value):
        same_type = True
        try:
            if not isinstance(value, self.type):
                same_type = False
        except:
            raise TypeError(f"\"{value}\" is not a {self.type_name}")
        else:
            if not same_type:
                raise TypeError(f"\"{value}\" is not a {self.type_name}")

    def validate(self, value):
        errors: list[str] = []

        try:
            if not isinstance(value, self.type):
                errors.append(f"\"{value}\" is not a {self.type_name}")
        except:
            errors.append(f"\"{value}\" is not a {self.type_name}")
        else:
            pass

        return errors


def string():
    schema = Schema(types.string)
    return schema


def integer():
    schema = Schema(types.integer)
    return schema


def float():
    schema = Schema(types.float)
    return schema


def boolean():
    schema = Schema(types.boolean)
    return schema