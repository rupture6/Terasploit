# -*- coding: utf-8 -*-

class DataStore:
    """ Global datastore implemented as a simple dictionary """

    _data: dict[str, object] = {}

    @classmethod
    def set(cls, key: str, value: object) -> None:
        """ Set a value in the datastore (key is case-insensitive) """
        cls._data[key.upper()] = value

    @classmethod
    def get(cls, key: str, default: object = None) -> object:
        """ Retrieve a value from the datastore """
        return cls._data.get(key.upper(), default)

    @classmethod
    def all(cls) -> dict[str, object]:
        """ Return the entire datastore """
        return dict(cls._data)


def datastore(key: str | None = None, value: object | None = None) -> object:
    """ Helper function to interact with the datastore like a dictionary """
    if key is not None and value is not None:
        DataStore.set(key, value)
        return None

    if key is not None:
        return DataStore.get(key)

    return DataStore.all()
