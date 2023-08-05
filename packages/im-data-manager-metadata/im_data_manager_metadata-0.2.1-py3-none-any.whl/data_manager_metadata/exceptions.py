"""Data Manager Metadata Exceptions.

    An AnnotationValidationError will be raised with one of the messages
    contained in ANNOTATION_ERRORS.
    Messages can optionally contain one runtime variable that can be used
    to identify, for example, a field in a FieldDescriptorAnnotation.

    ANNOTATION_ERRORS notes:
    1. The field 'regex' is normally used for the field identified by the
    annotation class and field.
    2. The exception is for the 'type' field where a list of enumerated
    types are used.
"""
SCHEMA_FIELD_TYPES = ['string', 'number', 'integer', 'object',
                      'array', 'boolean', 'null']

ANNOTATION_ERRORS \
    = {'PropertyChangeAnnotation': None,
       'LabelAnnotation':
           {'1': {'field': 'label', 'regex': r'^\w{1,12}$',
                  'message': 'Label length must be from 1 to 12 characters'},
            '2': {'field': 'value', 'regex':'^.{0,255}$',
                  'message': 'Value length must be from 1 to 255 characters'}
            },

       'FieldsDescriptorAnnotation':
           {'1': {'field': 'origin', 'regex':'^.{0,255}$',
                  'message': 'Origin length must be from 1 to 255 characters'},
            '2': {'field': 'description', 'regex':'^.{0,255}$',
                  'message': 'Description length must be from 1 to 255 '
                             'characters'},
            '3': {'field': 'field_name', 'regex': r'^.{1,50}$',
                  'message': 'Field name: {}, length must be from 1 to 50 '
                             'characters'},
            '4': {'field': 'type', 'enum': SCHEMA_FIELD_TYPES,
                  'message': 'type for field: {} must be one of string, '
                             'number, integer, '
                             'object, array, boolean and null'},
            '5': {'field': 'field_description', 'regex': '^.{0,255}$',
                  'message': 'Field description for field: {} length must be '
                             'from 1 to 255 characters'},
            },

       'ServiceExecutionAnnotation':
           {'1': {'field': 'service', 'regex': r'^.{1,80}$',
                  'message': 'Service length must be from 1 to 80 characters'},
            '2': {'field': 'service_version', r'regex': r'^.{1,80}$',
                  'message': 'Service version length must be from 1 to 80 '
                             'characters'},
            '3': {'field': 'service_user', 'regex': r'^.{1,80}$',
                  'message': 'Service user name length must be from 1 to 80 '
                             'characters'},
            '4': {'field': 'service_name', 'regex':'^.{1,255}$',
                  'message': 'Service name length must be from 1 to 255 '
                             'characters'},
            '5': {'field': 'service_ref', 'regex':'^.{1,255}$',
                  'message': 'Service ref length must be from 1 to 255 '
                             'characters'},
            },
       }


class AnnotationValidationError(Exception):
    """Exception raised for errors in the input.

     Attributes:
        annotation_type -- annotation class for which the error occurred
        error -- error number of error in ANNOTATION_ERRORS dictionary
        field -- annotation field in error
        field_value -- will be added to error message (if provided and a
        placeholder is specified in the message)
     """

    def __init__(self, annotation_type, error, field, field_value: str = None):

        super(AnnotationValidationError, self).__init__()
        self.annotation_type = annotation_type
        self.error = error
        self.field = field
        if field_value:
            self.message \
                = ANNOTATION_ERRORS[annotation_type][error]['message']\
                .format(field_value)
        else:
            self.message \
                = ANNOTATION_ERRORS[annotation_type][error]['message']

    def __str__(self):
        return self.message