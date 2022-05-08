import logging
from homedumper._extract import extract

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

__all__ = [
    'extract',
]

__version__ = '0.0.1'