import re
from slugify import slugify
from utils.dict import flatten_dict

FUEL_TYPES = {
    'bencin-95': 'Bencin 95',
    'bencin-100': 'Bencin 100',
    'diesel': 'Diesel',
    'lpg': 'LPG',
    'kurilno-olje': 'Kurilno Olje',
    'ad-blue': 'AdBlue'
}

PETROL_FUEL_NAMES = [
    ('Q Max 95', ("max 95", re.IGNORECASE, 'bencin-95')),
    ('Q Max 100', ("max 100", re.IGNORECASE, 'bencin-100')),
    ('Q Max Diesel', ("diesel", re.IGNORECASE, 'diesel')),
    ('Q Max LPG', ("LPG", re.IGNORECASE, 'lpg')),
    ('Kurilno olje EL', ("kurilno|olje", re.IGNORECASE, 'kurilno-olje'))
]

OMV_FUEL_NAMES = [
    ('MaxxMotion 95', (r"(\b95\b|motion\s9)", re.IGNORECASE, 'bencin-95')),
    ('OMV AdBlue', (r"AdBlue|blue", re.IGNORECASE, 'ad-blue')),
    ('MaxxMotion 100', (r"(\b100\b|motion\s1)", re.IGNORECASE, 'bencin-100')),
    ('Kurilno olje OMV futurPlus', (r"kurilno|olje|futur|plus", re.IGNORECASE, 'kurilno-olje')),
    ('OMV Avtoplin (LPG)', (r"\S+plin|LPG", re.IGNORECASE, 'lpg')),
    ('OMV Diesel', (r"diesel", re.IGNORECASE, 'diesel')),
]

ALL_FUEL_NAMES = dict(PETROL_FUEL_NAMES + OMV_FUEL_NAMES)

FUEL_NAMES = {
    'petrol': [pair[0] for pair in PETROL_FUEL_NAMES],
    'omv': [pair[0] for pair in OMV_FUEL_NAMES]
}

FUEL_CODES = dict([val for sl in
                   [[(v, slugify("%s %s" % (key, v))) for v in val] for key, val in
                    FUEL_NAMES.items()] for val in sl])

REVERSED_FUEL_CODES = {v: k for k, v in FUEL_CODES.items()}
