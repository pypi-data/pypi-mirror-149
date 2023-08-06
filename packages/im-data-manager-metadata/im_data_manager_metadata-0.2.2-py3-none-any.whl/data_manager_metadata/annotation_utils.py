"""Utilities for creating annotations
"""
from ast import literal_eval

def _check_array(field_value: str) -> bool:
    """If the field is a string that contains commas there is a fair chance
    that its an array of something.

    returns: true if estimated to be an array
             false otherwise
    """

    element_list = field_value.split(",")
    if len(element_list) > 1:
        return True

    return False

def est_schema_field_type(field_value: str) -> str:
    """Estimates a standard json schema type for an input field_value.

    Returns one of:
        string
        number
        integer
        object (can't be derived from a field - here for completeness)
        array (effectively a python list)
        boolean
        null
    """

    field_value = field_value.strip()
    if len(field_value) == 0:
        return 'null'

    try:
        field_type = literal_eval(field_value)
    except ValueError:
        # If a type cannot be identified, then check specific values.
        # If no specific value can be found return a string.
        if field_value in [
            True, False, 'TRUE', 'FALSE', 'true', 'false', 'yes', 'no',
            'YES', 'NO', 'Yes', 'No', "True", "False" ]:
            return 'boolean'
        return 'string'
    except SyntaxError:
        return 'string'
    else:
        # Check types
        if type(field_type) in [int, float, list]:
            if type(field_type) is int:
                return 'integer'
            if type(field_type) is float:
                return 'number'
            if type(field_type) is list:
                return 'array'
        else:
            if field_value in [
                True, False, 'TRUE', 'FALSE', 'true', 'false', 'yes', 'no',
                'YES', 'NO', 'Yes', 'No', "True", "False"]:
                return 'boolean'
            if _check_array(field_value):
                return 'array'
            return 'string'
