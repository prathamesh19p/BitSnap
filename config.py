from random import sample
from string import ascii_letters, digits
import re

VALID_CHARACTERS = ascii_letters + digits
HASH_LEN = 8
URL_REGEXP = re.compile(r'^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?$')

def generate_hash() -> str:
    return ''.join(sample(VALID_CHARACTERS, HASH_LEN))

def is_url(url: str) -> bool:
    return bool(URL_REGEXP.match(url))

def normalize_url(url: str) -> str:
    translation_table = str.maketrans('', '', '!"#$%&\'()*+,-./@:;<=>[\\]^_`{|}~')
    return url.strip().translate(translation_table)

