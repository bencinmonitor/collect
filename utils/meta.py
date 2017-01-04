import re
from slugify import slugify
from utils.dict import flatten_dict

PETROL_FUEL_NAMES = [
    ('Q Max 95', ("max 95", re.IGNORECASE)),
    ('Q Max 100', ("max 100", re.IGNORECASE)),
    ('Q Max Diesel', ("diesel", re.IGNORECASE)),
    ('Q Max LPG', ("LPG", re.IGNORECASE)),
    ('Kurilno olje EL', ("kurilno|olje", re.IGNORECASE))
]

OMV_FUEL_NAMES = [
    ('MaxxMotion 95', (r"(\b95\b|motion\s9)", re.IGNORECASE)),
    ('OMV AdBlue', (r"AdBlue|blue", re.IGNORECASE)),
    ('MaxxMotion 100', (r"(\b100\b|motion\s1)", re.IGNORECASE)),
    ('Kurilno olje OMV futurPlus', (r"kurilno|olje|futur|plus", re.IGNORECASE)),
    ('OMV Avtoplin (LPG)', (r"\S+plin|LPG", re.IGNORECASE)),
    ('OMV Diesel', (r"diesel", re.IGNORECASE)),
]

FUEL_NAMES = {
    'petrol': [pair[0] for pair in PETROL_FUEL_NAMES],
    'omv': [pair[0] for pair in OMV_FUEL_NAMES]
}

FUEL_CODES = dict([val for sl in
                   [[(v, slugify("%s %s" % (key, v))) for v in val] for key, val in
                    FUEL_NAMES.items()] for val in sl])

REVERSED_FUEL_CODES = {v: k for k,v in FUEL_CODES.items()}