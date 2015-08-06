from jsonschema import validate as _validate


REQUIREMENT_ITEM = {
    'title': 'Requirement',
    'description': 'A single requirement item.',
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'requirement': {'type': 'string'},
        'reason': {'type': 'string'},
        'severity': {'type': 'string', 'enum': ['error', 'warn']},
    },
    'required': ['requirement']
}


SCHEMA = {
    'title': 'Requirement collection',
    'description': 'A collection of requirements.',
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'requirements': {
            'type': 'array',
            'items': REQUIREMENT_ITEM,
        },
    },
    'required': ['requirements']
}


def validate(requirements):
    _validate(requirements, SCHEMA)
