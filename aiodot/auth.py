# ==========================================
# aiodot/auth.py
# ==========================================

"""Authentication module for MyDot.one. Token-based with session file."""

import json
import time
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, Optional

import aiohttp
import requests


@dataclass
class Session:
    token: str = ""
    user_id: str = ""
    username: str = ""
    display_name: str = ""
    phone: str = ""
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        fields = cls.__dataclass_fields__
        return cls(**{k: v for k, v in data.items() if k in fields})


class MyDotAuth:
    BASE_URL = "https://api.mydot.one/mydot/api/v1"

    def __init__(self, session_file: Optional[str] = None):
        self.session_file = Path(session_file or Path.home() / ".mydot" / "session.json")
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        self.session_data = Session()
        self._loaded = False
        if self.session_file.exists():
            self._load()

    def _load(self) -> bool:
        try:
            self.session_data = Session.from_dict(
                json.loads(self.session_file.read_text(encoding="utf-8"))
            )
            self._loaded = bool(self.session_data.token)
            return True
        except Exception:
            return False

    def save(self) -> None:
        self.session_file.write_text(
            json.dumps(self.session_data.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def clear(self) -> None:
        self.session_data = Session()
        if self.session_file.exists():
            self.session_file.unlink()

    def login(self, username: str, password: str) -> bool:
        resp = requests.post(
            f"{self.BASE_URL}/auth/login/",
            json={"identifier": username, "password": password},
            headers=self._headers(),
        )
        if not resp.ok:
            print(f"❌ Login failed: {resp.status_code}")
            return False

        token = resp.cookies.get("__Secure-access_token")
        if not token:
            print("❌ No token in response")
            return False

        self.session_data.token = token
        self._loaded = True
        self._fetch_and_save()
        return True

    def login_with_token(self, token: str) -> bool:
        self.session_data.token = token
        resp = requests.get(
            f"{self.BASE_URL}/auth/profile/",
            cookies={"__Secure-access_token": token},
            headers=self._headers(),
        )
        if not resp.ok:
            print("❌ Invalid token")
            return False

        self._loaded = True
        self._fetch_and_save()
        return True

    async def refresh(self) -> bool:
        headers = self._headers()
        headers["Cookie"] = f"__Secure-access_token={self.token}"
        async with aiohttp.ClientSession() as s:
            async with s.post(f"{self.BASE_URL}/auth/token/refresh/", headers=headers, json={}) as resp:
                if resp.status == 200:
                    for key, cookie in resp.cookies.items():
                        if key == "__Secure-access_token":
                            self.session_data.token = cookie.value
                            self.save()
                            return True
        return False

    def _fetch_and_save(self) -> None:
        try:
            resp = requests.get(
                f"{self.BASE_URL}/auth/profile/",
                cookies={"__Secure-access_token": self.session_data.token},
                headers=self._headers(),
            )
            if resp.ok:
                p = resp.json()
                self.session_data.user_id = p.get("user_id", "")
                self.session_data.username = p.get("username", "")
                self.session_data.display_name = p.get("display_name", "")
                self.save()
                print(f"✅ @{self.username}")
        except Exception:
            pass

    @staticmethod
    def _headers() -> Dict[str, str]:
        return {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://mydot.one",
            "Referer": "https://mydot.one/",
            "User-Agent": "Mozilla/5.0",
        }

    @property
    def token(self) -> Optional[str]:
        return self.session_data.token

    @property
    def user_id(self) -> Optional[str]:
        return self.session_data.user_id

    @property
    def username(self) -> Optional[str]:
        return self.session_data.username

    @property
    def display_name(self) -> Optional[str]:
        return self.session_data.display_name

    @property
    def is_logged_in(self) -> bool:
        return self._loaded and bool(self.token)

    def __repr__(self) -> str:
        return f"MyDotAuth(@{self.username})" if self.username else "MyDotAuth(not logged in)"