import re

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
