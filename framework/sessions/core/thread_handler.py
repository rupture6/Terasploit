# -*- coding: utf-8 -*-

# Python library
import threading
from typing import Any, Optional

# Session handler for managing active sessions and networking state


class Session:
    """Global session handler."""

    # Active sessions
    sessions: list[Any] = []

    # Lock to synchronize access
    thread_lock = threading.Lock()

    # Global events
    alive = threading.Event()
    active_listener = threading.Event()
    active_connector = threading.Event()

    # Handler thread and sockets
    handler_thread: Optional[threading.Thread] = None
    server_socket: Any = None

    @classmethod
    def reset_events(cls) -> None:
        """ Reset all threading events """
        cls.active_listener.clear()
        cls.active_connector.clear()
        cls.alive.clear()

    @classmethod
    def reverse_tcp_reset(cls) -> None:
        """ Reset state when a reverse TCP handler stops """
        cls.active_listener.clear()
        cls.alive.clear()
        cls._reset_core()

    @classmethod
    def bind_tcp_reset(cls) -> None:
        """ Reset state when a bind TCP handler stops """
        cls.active_connector.clear()
        cls.alive.clear()
        cls._reset_core(reset_socket=False)

    @classmethod
    def _reset_core(cls, reset_socket: bool = True) -> None:
        """ Reset common attributes """
        cls.handler_thread = None
        if reset_socket:
            cls.server_socket = None
