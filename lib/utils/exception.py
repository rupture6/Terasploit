# -*- coding: utf-8 -*-

# This module provides a base exception class and specialized
# exceptions to handle project-specific error cases consistently.


class TerasploitException(Exception):
    """ Base exception for the project """

    def __init__(
        self,
        message: str = "",
        details: str = ""
    ):
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        return (
            f"{self.message}"
            f"{(' - ' + self.details) if self.details else ''}"
        )


class ValidationError(TerasploitException):
    """ Raised when validation fails """


class InvalidError(TerasploitException):
    """ Raised when an object is invalid """


class NotFoundError(TerasploitException):
    """ Raised when a requested resource is not found """
