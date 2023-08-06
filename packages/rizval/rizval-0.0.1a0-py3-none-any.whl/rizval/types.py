string = str
integer = int
float = float
boolean = bool

def get_type_name(type):
    if type == string:
        return "string"
    elif type == integer:
        return "integer"
    elif type == float:
        return "float"
    elif type == boolean:
        return "boolean"
    else:
        raise Exception("Invalid type")
