"""Utilities for defining DBC constants.

These are required because Python doesn't have very specific types, and
the classes in this directory are automatically converted into 
construct.Struct objects, which requires specific types.
"""


class SingleString(str):
    """A single string value.

    See https://wowdev.wiki/Common_Types#stringref.
    """


class MultiString(str):
    """A localized string value.

    See https://wowdev.wiki/Common_Types#langstringref.
    """


class SingleEnumString(SingleString):
    """A single string value.

    Indicates that this value should be used as the key when generating
    an enum based on this table.
    """


class MultiEnumString(MultiString):
    """A localized string value.

    Indicates that this value should be used as the key when generating
    an enum based on this table. The "en_us" localization will be used.
    """


class MultiEnumSecondaryString(MultiString):
    """A localized string value.

    Indicates that this value should be used as a secondary key when
    generating an enum based on this table. This will be appended to the
    primary key using an _.
    """
