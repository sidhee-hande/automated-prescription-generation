import uuid


def get_smith_item():
    smith_item = {
        'id': 'Johnson_' + str(uuid.uuid4()),
        'lastName': 'Johnson',
        'district': None,
        'registered': False
    }
    return smith_item


def get_johnson_item():
    johnson_item = {
        'id': 'Smith_' + str(uuid.uuid4()),
        'lastName': 'Smith',
        'parents': None,
        'children': None,
        'address': {
            'state': 'WA',
            'city': 'Redmond'
        },
        'registered': True
    }
    return johnson_item
