# -*- coding: utf-8 -*-

# Python library
import logging
from typing import Any
from logging.handlers import RotatingFileHandler

# Library
from lib.container.console import Config

# NOTE: Console logging is not yet properly implemented in the framework.


class Log:
    """ Custom logger with file + optional console output """

    def __init__(
        self,
        logfile: str = "terasploit.log",
        level: str | int = "INFO",
        console: bool = False,
    ) -> None:
        """ Initialize the logger """

        self.logfile: str = logfile
        self.level: int = self._resolve_level(level)
        self.console_enabled: bool = console

        self.logger: logging.Logger = logging.getLogger()
        self.logger.setLevel(self.level)

        # Prevent duplicate handlers
        self.logger.handlers.clear()

        # File handler with rotation
        self.file_handler = RotatingFileHandler(
            self.logfile,
            maxBytes=10_000,
            backupCount=3,
        )
        self.file_handler.setFormatter(self._formatter())
        self.logger.addHandler(self.file_handler)

        # Optional console handler
        if self.console_enabled:
            self._add_console_handler()

    @staticmethod
    def _formatter() -> logging.Formatter:
        """ Return a standard log formatter """
        format = ("[%(levelname).1s] %(asctime)s :: %(message)s")
        return logging.Formatter(format)

    @staticmethod
    def _resolve_level(level: Any) -> int:
        """ Convert level to int if string, else validate int """
        if isinstance(level, str):
            return getattr(logging, level.upper(), logging.INFO)
        if isinstance(level, int):
            return level
        raise TypeError("Log level must be str or int.")

    def set_level(self, level: str | int) -> None:
        """ Change the logging level dynamically """
        self.level = self._resolve_level(level)
        self.logger.setLevel(self.level)

    def _add_console_handler(self) -> None:
        """ Attach a console handler """
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self._formatter())
        self.logger.addHandler(self.console_handler)

    def enable_console(self) -> None:
        """ Enable console logging """
        if not self.console_enabled:
            self._add_console_handler()
            self.console_enabled = True

    def disable_console(self) -> None:
        """ Disable console logging """
        self.logger.handlers = [
            h for h in self.logger.handlers
            if not isinstance(h, logging.StreamHandler)
        ]
        self.console_enabled = False

    def disable_all(self) -> None:
        """ Disable all logging (console + file) """
        self.logger.handlers.clear()

    def log(
        self,
        message: str,
        level: str | int = "INFO",
    ) -> None:
        """ Log a message if global logging is enabled """
        if not Config.logging:
            self.disable_all()
            return
        if Config.logging and not self.console_enabled:
            self.enable_console()

        lvl = self._resolve_level(level)
        self.logger.log(lvl, message)
