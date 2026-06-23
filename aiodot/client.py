from .models import Dot, User, ThreadView, Notification, PaginatedResponse, Thread, ReplyPermission
from typing import Optional, Dict, List, Any
import asyncio
import aiohttp
from .auth import MyDotAuth
from .wallet import WalletManager


class MyDotClient:
    BASE_URL = "https://api.mydot.one/mydot/api/v1"

    def __init__(self, token: Optional[str] = None, session_file: Optional[str] = None, auth: Optional[MyDotAuth] = None):
        if auth:
            self.auth = auth
        elif token:
            self.auth = MyDotAuth(session_file=session_file)
            self.auth.login_with_token(token)
        else:
            self.auth = MyDotAuth(session_file=session_file)
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        if self._session:
            await self._session.close()
            self._session = None

    @property
    def http(self) -> aiohttp.ClientSession:
        if self._session is None:
            raise RuntimeError("Use 'async with MyDotClient(...) as client:' block.")
        return self._session

    @property
    def wallet(self) -> WalletManager:
        return WalletManager(self)

    async def login(self, username: str, password: str) -> bool:
        return self.auth.login(username, password)

    def _headers(self) -> Dict[str, str]:
        h = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://mydot.one",
            "Referer": "https://mydot.one/",
            "User-Agent": "Mozilla/5.0",
        }
        if self.auth.token:
            h["Cookie"] = f"__Secure-access_token={self.auth.token}"
        return h

    async def _get(self, path: str, params: Dict = None) -> Any:
        url = f"{self.BASE_URL}{path}"
        async with self.http.get(url, params=params, headers=self._headers()) as resp:
            if resp.status == 401 and await self.auth.refresh():
                async with self.http.get(url, params=params, headers=self._headers()) as r:
                    r.raise_for_status()
                    return await r.json() if "json" in r.content_type else await r.text()
            resp.raise_for_status()
            return await resp.json() if "json" in resp.content_type else await resp.text()

    async def _post(self, path: str, json: Dict = None) -> Any:
        url = f"{self.BASE_URL}{path}"
        async with self.http.post(url, json=json, headers=self._headers()) as resp:
            if resp.status == 401 and await self.auth.refresh():
                async with self.http.post(url, json=json, headers=self._headers()) as r:
                    r.raise_for_status()
                    return await r.json() if "json" in r.content_type else await r.text()
            resp.raise_for_status()
            return await resp.json() if "json" in resp.content_type else await resp.text()

    async def _patch(self, path: str, json: Dict = None) -> Any:
        url = f"{self.BASE_URL}{path}"
        async with self.http.patch(url, json=json, headers=self._headers()) as resp:
            if resp.status == 401 and await self.auth.refresh():
                async with self.http.patch(url, json=json, headers=self._headers()) as r:
                    r.raise_for_status()
                    return await r.json() if "json" in r.content_type else await r.text()
            resp.raise_for_status()
            return await resp.json() if "json" in resp.content_type else await resp.text()

    async def _delete(self, path: str) -> Any:
        url = f"{self.BASE_URL}{path}"
        async with self.http.delete(url, headers=self._headers()) as resp:
            if resp.status == 401 and await self.auth.refresh():
                async with self.http.delete(url, headers=self._headers()) as r:
                    r.raise_for_status()
                    return await r.json() if "json" in r.content_type else await r.text()
            resp.raise_for_status()
            return await resp.json() if "json" in resp.content_type else await resp.text()

    # ============ Profile ============
    async def get_me(self) -> User:
        return User.from_dict(await self._get("/auth/profile/"))

    async def update_profile(self, **kwargs) -> User:
        return User.from_dict(await self._patch("/auth/profile/", json=kwargs))

    async def get_profile_visibility(self) -> Dict:
        return await self._get("/auth/profile/visibility/")

    async def set_profile_visibility(self, visibility: str) -> Dict:
        return await self._patch("/auth/profile/visibility/", json={"profile_visibility": visibility})

    async def upload_avatar_request(self, filename: str, content_type: str = "image/gif") -> Dict:
        return await self._post("/auth/profile/avatar/upload/", json={
            "filename": filename,
            "content_type": content_type,
        })

    async def upload_avatar_put(self, upload_url: str, file_path: str, content_type: str = "image/gif") -> bool:
        with open(file_path, "rb") as f:
            data = f.read()
        async with self.http.put(upload_url, data=data, headers={"Content-Type": content_type}) as resp:
            return resp.status in (200, 201, 204)

    async def upload_avatar(self, file_path: str, filename: str = "avatar.gif", content_type: str = "image/gif") -> Optional[str]:
        req = await self.upload_avatar_request(filename, content_type)
        upload_url = req.get("upload_url") or req.get("url")
        if not upload_url:
            return None
        ok = await self.upload_avatar_put(upload_url, file_path, content_type)
        return req.get("avatar_key") or req.get("key") if ok else None

    # ============ Social ============
    async def follow(self, user_id: str) -> bool:
        await self._post("/auth/follow/", json={"target_id": user_id})
        return True

    async def unfollow(self, user_id: str) -> bool:
        await self._post("/auth/unfollow/", json={"target_id": user_id})
        return True

    async def block(self, user_id: str) -> bool:
        await self._post("/auth/block/", json={"target_id": user_id})
        return True

    async def unblock(self, user_id: str) -> bool:
        await self._post("/auth/unblock/", json={"target_id": user_id})
        return True

    async def mute(self, user_id: str) -> bool:
        await self._post("/auth/mute/", json={"target_id": user_id})
        return True

    async def unmute(self, user_id: str) -> bool:
        await self._post("/auth/unmute/", json={"target_id": user_id})
        return True

    # ============ Users ============
    async def get_user_followers(self, username: str, page_size: int = 20) -> Dict:
        return await self._get(f"/auth/{username}/followers/", params={"page_size": page_size})

    async def get_user_following(self, username: str, page_size: int = 20) -> Dict:
        return await self._get(f"/auth/{username}/following/", params={"page_size": page_size})

    async def search_users(self, query: str) -> Any:
        return await self._get("/auth/profile/search", params={"q": query})

    # ============ Dots ============
    async def get_dot(self, dot_id: str) -> Dot:
        return Dot.from_dict(await self._get(f"/dots/{dot_id}/"))

    async def get_thread_view(self, dot_id: str) -> ThreadView:
        return ThreadView.from_dict(await self._get(f"/dots/{dot_id}/thread-view/"))

    async def get_replies(self, dot_id: str, page: int = 1, limit: int = 20) -> Dict:
        return await self._get(f"/dots/{dot_id}/replies/", params={"page": page, "limit": limit})

    async def get_reposts(self, dot_id: str) -> Dict:
        return await self._get(f"/dots/{dot_id}/reposts/")

    async def get_quotes(self, dot_id: str) -> Dict:
        return await self._get(f"/dots/{dot_id}/quotes/")

    async def get_dot_likes(self, dot_id: str) -> Any:
        return await self._get(f"/dots/{dot_id}/likes/")

    async def get_user_dots(self, user_id: str, dot_type: str = "dot,quote,repost", limit: int = 20) -> Dict:
        return await self._get(f"/dots/user/{user_id}/", params={"dot_type": dot_type, "limit": limit})

    async def get_user_replies(self, user_id: str) -> Dict:
        return await self._get(f"/dots/user/{user_id}/", params={"dot_type": "reply"})

    async def get_user_likes(self, user_id: str) -> Dict:
        return await self._get(f"/dots/user/{user_id}/activity/", params={"action_type": "like"})

    async def create_dot(self, content: str, dot_type: str = "dot", reply_to: str = None,
                         repost_of: str = None, quote_of: str = None,
                         media_ids: List[str] = None, reply_permission: str = "everyone") -> Dot:
        body = {k: v for k, v in {
            "dot_type": dot_type, "content": content,
            "reply_to": reply_to, "repost_of": repost_of, "quote_of": quote_of,
            "media_ids": media_ids or [], "reply_permission": reply_permission,
        }.items() if v is not None}
        return Dot.from_dict(await self._post("/dots/", json=body))

    async def reply(self, dot_id: str, content: str, media_ids: List[str] = None, reply_permission: str = "everyone") -> Dot:
        return await self.create_dot(content=content, dot_type="reply", reply_to=dot_id, media_ids=media_ids, reply_permission=reply_permission)

    async def repost(self, dot_id: str, media_ids: List[str] = None) -> Dot:
        return await self.create_dot(content="", dot_type="repost", repost_of=dot_id, media_ids=media_ids)

    async def quote(self, dot_id: str, content: str, media_ids: List[str] = None, reply_permission: str = "everyone") -> Dot:
        return await self.create_dot(content=content, dot_type="quote", quote_of=dot_id, media_ids=media_ids, reply_permission=reply_permission)

    async def like(self, dot_id: str) -> bool:
        await self._post(f"/dots/{dot_id}/like/")
        return True

    async def unlike(self, dot_id: str) -> bool:
        await self._delete(f"/dots/{dot_id}/like/")
        return True

    async def bookmark(self, dot_id: str) -> bool:
        await self._post(f"/dots/{dot_id}/bookmark/")
        return True

    async def unbookmark(self, dot_id: str) -> bool:
        await self._delete(f"/dots/{dot_id}/bookmark/")
        return True

    async def edit_dot(self, dot_id: str, content: str) -> Dot:
        return Dot.from_dict(await self._patch(f"/dots/{dot_id}/", json={"content": content}))

    async def delete_dot(self, dot_id: str) -> bool:
        await self._delete(f"/dots/{dot_id}/")
        return True

    async def undo_repost(self, dot_id: str) -> bool:
        await self._delete(f"/dots/{dot_id}/repost/")
        return True

    async def set_reply_permission(self, dot_id: str, permission: str) -> bool:
        valid = {"everyone", "following", "mentioned", "nobody"}
        if permission not in valid:
            raise ValueError(f"permission must be one of {valid}")
        await self._patch(f"/posts/{dot_id}/permissions/", json={"reply_permission": permission})
        return True

    # ============ Feed ============
    async def home_feed(self, page_size: int = 40) -> Dict:
        return await self._get("/feed/suggestions/timeline/", params={"page_size": page_size})

    async def following_feed(self, **params) -> Dict:
        return await self._get("/feed/following/", params=params)

    async def explore_users_suggestions(self, limit: int = 20, cursor: str = None) -> Dict:
        p = {"limit": limit}
        if cursor:
            p["cursor"] = cursor
        return await self._get("/feed/suggestions/follow/", params=p)

    async def get_topic_dots(self, topic_id: str, limit: int = 20, cursor: str = None) -> Dict:
        p = {"limit": limit}
        if cursor:
            p["cursor"] = cursor
        return await self._get(f"/topics/{topic_id}/dots/", params=p)

    # ============ Notifications ============
    async def get_notifications(self, page_size: int = 50) -> Dict:
        return await self._get("/notifications/", params={"page_size": page_size})

    async def get_notification_preferences(self) -> Dict:
        return await self._get("/notifications/preferences/")

    async def update_notification_preferences(self, **kwargs) -> Dict:
        return await self._patch("/notifications/preferences/", json=kwargs)

    async def mark_all_notifications_read(self) -> bool:
        await self._post("/notifications/read-all/")
        return True

    # ============ Bookmarks ============
    async def get_bookmarks(self, limit: int = 20) -> Dict:
        return await self._get("/dots/bookmarks/", params={"limit": limit})

    # ============ Trending ============
    async def get_trending_hashtags(self) -> Any:
        return await self._get("/dots/hashtags/trending/")

    async def get_trending_media(self, limit: int = 24) -> Dict:
        return await self._get("/dots/media/trending/", params={"limit": limit})

    # ============ Composer ============
    async def get_composer_state(self) -> Dict:
        return await self._get("/composer/state/")

    async def reset_composer(self) -> bool:
        await self._post("/composer/reset/")
        return True

    async def add_thread(self, content: str = "", media_ids: List[str] = None) -> Dict:
        body = {"content": content}
        if media_ids:
            body["media_ids"] = media_ids
        return await self._post("/composer/thread/", json=body)

    async def remove_thread(self, index: int) -> bool:
        await self._delete(f"/composer/thread/{index}/")
        return True

    # ============ Threads ============
    async def create_threads(self, post_id: str, threads_data: Dict) -> Dict:
        return await self._post(f"/posts/{post_id}/threads/", json=threads_data)

    async def get_threads(self, post_id: str) -> Dict:
        return await self._get(f"/posts/{post_id}/threads/")

    async def get_threads_view(self, post_id: str) -> Dict:
        return await self._get(f"/posts/{post_id}/threads/view/")

    # ============ Wallet ============
    async def create_wallet(self, data: Dict) -> Dict:
        return await self._post("/wallet/create/", json=data)

    async def get_wallet_list(self) -> List[Dict]:
        data = await self._get("/wallet/list/")
        return data.get("results", []) if isinstance(data, dict) else data

    async def get_transaction_list(self, wallet_id: str) -> List[Dict]:
        data = await self._get(f"/wallet/transactions/{wallet_id}/")
        return data.get("results", []) if isinstance(data, dict) else data

    async def get_wallet_by_id(self, wallet_id: str) -> Dict:
        return await self._get(f"/wallet/{wallet_id}/")

    async def toggle_wallet_default(self, wallet_id: str) -> None:
        await self._post(f"/wallet/toggle/{wallet_id}/")

    # ============ Other ============
    async def get_alerts(self) -> Any:
        return await self._get("/utils/alerts/active/")

    async def get_invites(self) -> Dict:
        return await self._get("/auth/invites/")

    async def get_wallets(self) -> Dict:
        return await self._get("/auth/wallets/")

    async def get_2fa_state(self) -> Dict:
        return await self._get("/auth/2fa/state/")

    async def get_star_settings(self) -> Dict:
        return await self._get("/reward/default-stars/")

    async def get_star_transactions(self) -> Dict:
        return await self._get("/reward/stars-transaction/")

    async def upload_media(self, file_path: str) -> Dict:
        url = f"{self.BASE_URL}/posts/media/"
        with open(file_path, "rb") as f:
            form = aiohttp.FormData()
            form.add_field("file", f)
            async with self.http.post(url, data=form, headers=self._headers()) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def get_dot_url(self, short_id: str, username: str = None) -> str:
        if username is None:
            username = self.auth.username
        return f"https://mydot.one/@{username}/status/{short_id}"