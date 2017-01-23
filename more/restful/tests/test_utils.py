from more.restful.utils import remerge

DEFAULTS = {
    'host': '127.0.0.1',
    'port': 8000,
    'owners': {
        'secondary': ['jane']
    },
    'notes': ['this is the default']
}

OVERLAY = {
    'port': 8080,
    'owners': {
        'primary': ['john'],
        'secondary': ['jessy']
    },
    'notes': ['this is the overlay']
}


def test_remerge():
    merged = remerge([DEFAULTS, OVERLAY])
    assert merged == {
        'host': '127.0.0.1',
        'port': 8080,
        'owners': {
            'primary': ['john'],
            'secondary': ['jane', 'jessy']
        },
        'notes': ['this is the default', 'this is the overlay']
    }


def test_remerge_sourced():
    merged, sourced = remerge(
        [('defaults', DEFAULTS), ('overlay', OVERLAY)],
        sourced=True
    )
    assert merged == {
        'host': '127.0.0.1',
        'port': 8080,
        'owners': {
            'primary': ['john'],
            'secondary': ['jane', 'jessy']
        },
        'notes': ['this is the default', 'this is the overlay']
    }
    assert sourced == {
        ('host',): 'defaults',
        ('notes',): 'overlay',
        ('owners',): 'overlay',
        ('owners', 'primary'): 'overlay',
        ('owners', 'secondary'): 'overlay',
        ('port',): 'overlay'
    }
