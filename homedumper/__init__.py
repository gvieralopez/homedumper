import logging
from homedumper._extract import extract
from homedumper._boxify import boxify

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

__all__ = [
    'extract',
    'boxify'
]

__version__ = '0.0.1'