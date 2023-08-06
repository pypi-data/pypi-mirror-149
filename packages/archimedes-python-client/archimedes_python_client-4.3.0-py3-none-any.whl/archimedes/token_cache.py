from msal_extensions import (
    build_encrypted_persistence,
    FilePersistence,
    PersistedTokenCache,
)

from .configuration import SAVED_MSAL_TOKEN_CACHE_PATH


def build_persistence(location, fallback_to_plaintext=False):
    """Build a suitable persistence instance based your current OS"""
    try:
        return build_encrypted_persistence(location)
    except:
        if not fallback_to_plaintext:
            raise
        return FilePersistence(location)


persistence = build_persistence(SAVED_MSAL_TOKEN_CACHE_PATH, True)

token_cache = PersistedTokenCache(persistence)
