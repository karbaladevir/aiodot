"""
aiodot - Async Python client for MyDot.one social platform.
Build bots, automation, and tools with ease.

License: MIT
Version: 1.2.0
"""

from .client import MyDotClient
from .auth import MyDotAuth, Session
from .models import Dot, User, ThreadView, Notification, PaginatedResponse, Thread, ReplyPermission
from .wallet import WalletManager

__version__ = "1.2.0"
__license__ = "MIT"
__all__ = [
    "MyDotClient",
    "MyDotAuth",
    "Session",
    "Dot",
    "User",
    "ThreadView",
    "Notification",
    "PaginatedResponse",
    "Thread",
    "ReplyPermission",
    "WalletManager",
]