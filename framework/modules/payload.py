# -*- coding: utf-8 -*-

# Framework
from framework.console.options import OptGet


class Payload:
    """ Utility functions of payload module """

    def opt(self, key: str):
        """ Access the option dictionary to get a specific value """
        return OptGet(key)
