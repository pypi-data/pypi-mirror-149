try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

def version():
    return metadata.version("imaplar")
