import sys


if sys.version_info[:2] >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata


version = metadata.version(__package__)
author = 'maximilionus'
