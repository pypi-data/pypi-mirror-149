"""
Functions to deal with system paths
"""

__all__ = ["slugify"]


def slugify(text, keep_characters=None):
    """Turn any text into a string that can be used in a filename

    Parameters
    ----------
    text : str
        text to slugify
    keep_characters : list of str
        characters in this iterable will be kept in the final string. Defaults to ['_']. Any other
        non-alphanumeric characters will be removed.

    Returns
    -------
    slug : str

    """

    keep_characters = ["_"] if keep_characters is None else keep_characters
    end = next(
        (i for i, c in enumerate(text) if not c.isalnum() and c not in keep_characters),
        None,
    )
    slug = text[:end]
    return slug
