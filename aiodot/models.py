from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    user_id: str = ""
    username: str = ""
    display_name: str = ""
    bio: str = ""
    location: str = ""
    website: str = ""
    avatar_url: str = ""
    header_url: str = ""
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    is_verified: bool = False
    is_dotone_staff: bool = False
    account_type: str = "standard"
    profile_visibility: str = "public"
    created_at: str = ""
    email: str = ""
    phone_number: str = ""
    kyc_status: str = "not_requested"
    joined_date: Optional[str] = None
    last_username_change: Optional[str] = None
    is_own_profile: bool = False
    gender: str = ""
    birthdate: str = ""
    default_wallet_address: Optional[str] = None
    has_nft_username: bool = False
    is_blocked: bool = False
    is_muted: bool = False
    incoming_follow_status: Optional[str] = None
    follow_status: Optional[str] = None
    badge_request: Optional[Dict] = None
    selected_badge: Optional[Dict] = None
    email_verified: bool = False
    phone_verified: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        viewer = data.get("viewer_context", {})
        return cls(
            user_id=data.get("user_id", data.get("id", "")),
            username=data.get("username", ""),
            display_name=data.get("display_name", data.get("name", "")),
            bio=data.get("bio", ""),
            location=data.get("location", ""),
            website=data.get("website", ""),
            avatar_url=data.get("avatar_url", data.get("avatar", "")),
            header_url=data.get("header_url", data.get("header", "")),
            followers_count=data.get("followers_count", 0),
            following_count=data.get("following_count", 0),
            posts_count=data.get("posts_count", 0),
            is_verified=data.get("is_verified", False),
            is_dotone_staff=data.get("is_dotone_staff", False),
            account_type=data.get("account_type", "standard"),
            profile_visibility=data.get("profile_visibility", "public"),
            created_at=data.get("created_at", ""),
            email=data.get("email", ""),
            phone_number=data.get("phone_number", data.get("phone", "")),
            kyc_status=data.get("kyc_status", "not_requested"),
            joined_date=data.get("joined_date") or data.get("joinedDate"),
            last_username_change=data.get("last_username_change") or data.get("lastUsernameChange"),
            is_own_profile=viewer.get("is_own_profile", False) or data.get("isOwnProfile", False),
            gender=data.get("gender", ""),
            birthdate=data.get("birthdate", ""),
            default_wallet_address=data.get("default_wallet_address"),
            has_nft_username=data.get("has_nft_username", False),
            is_blocked=viewer.get("is_blocked", False) or data.get("is_blocked", False),
            is_muted=viewer.get("is_muted", False) or data.get("is_muted", False),
            incoming_follow_status=data.get("incoming_follow_status"),
            follow_status=data.get("follow_status"),
            badge_request=data.get("badge_request"),
            selected_badge=data.get("selected_badge"),
            email_verified=data.get("email_verified", False),
            phone_verified=data.get("phone_verified", False),
        )

    @property
    def profile_url(self) -> str:
        return f"https://mydot.one/@{self.username}"

    @property
    def joined_date_formatted(self) -> str:
        if not self.joined_date:
            return ""
        try:
            dt = datetime.fromisoformat(self.joined_date.replace("Z", "+00:00"))
            return dt.strftime("%B %Y")
        except (ValueError, TypeError):
            return self.joined_date or ""

    @property
    def is_kyc_verified(self) -> bool:
        return self.kyc_status == "success"

    @property
    def has_badge(self) -> bool:
        return self.selected_badge is not None

    @property
    def badge_name(self) -> str:
        return self.selected_badge.get("name", "") if self.selected_badge else ""

    @property
    def display_name_or_username(self) -> str:
        return self.display_name or self.username

    def __repr__(self) -> str:
        return f"User(@{self.username})"


@dataclass
class Dot:
    id: str = ""
    short_id: str = ""
    content: str = ""
    dot_type: str = "dot"
    author: Dict[str, Any] = field(default_factory=dict)
    reply_to: Optional[str] = None
    repost_of: Optional[str] = None
    quote_of: Optional[str] = None
    likes_count: int = 0
    replies_count: int = 0
    reposts_count: int = 0
    quotes_count: int = 0
    bookmarks_count: int = 0
    view_count: int = 0
    stars: int = 0
    is_liked: bool = False
    is_reposted: bool = False
    is_bookmarked: bool = False
    created_at: Optional[str] = None
    edited_at: Optional[str] = None
    media: List[Dict] = field(default_factory=list)
    entities: Dict = field(default_factory=dict)
    sensitive_type: str = "normal"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Dot":
        vc = data.get("viewer_context", {})
        return cls(
            id=data.get("id", ""),
            short_id=data.get("short_id", ""),
            content=data.get("content", ""),
            dot_type=data.get("dot_type", "dot"),
            author=data.get("author", {}),
            reply_to=data.get("reply_to"),
            repost_of=data.get("repost_of"),
            quote_of=data.get("quote_of"),
            likes_count=data.get("likes_count", 0),
            replies_count=data.get("replies_count", 0),
            reposts_count=data.get("reposts_count", 0),
            quotes_count=data.get("quotes_count", 0),
            bookmarks_count=data.get("bookmarks_count", 0),
            view_count=data.get("view_count", 0),
            stars=data.get("stars", 0),
            is_liked=vc.get("is_liked", False),
            is_reposted=vc.get("is_reposted", False),
            is_bookmarked=vc.get("is_bookmarked", False),
            created_at=data.get("created_at"),
            edited_at=data.get("edited_at"),
            media=data.get("media", []),
            entities=data.get("entities", {}),
            sensitive_type=data.get("sensitive_type", "normal"),
        )

    @property
    def author_username(self) -> str:
        return self.author.get("username", "")

    @property
    def url(self) -> str:
        return f"https://mydot.one/@{self.author_username}/status/{self.short_id}"

    @property
    def is_reply(self) -> bool:
        return self.dot_type == "reply"

    @property
    def is_repost(self) -> bool:
        return self.dot_type == "repost"

    @property
    def is_quote(self) -> bool:
        return self.dot_type == "quote"


@dataclass
class Notification:
    id: str = ""
    type: str = ""
    created_at: str = ""
    is_read: bool = False
    actor: Optional[Dict] = None
    dot: Optional[Dot] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Notification":
        dot = Dot.from_dict(data["dot"]) if data.get("dot") else None
        return cls(
            id=data.get("id", ""),
            type=data.get("type", ""),
            created_at=data.get("created_at", ""),
            is_read=data.get("is_read", False),
            actor=data.get("actor"),
            dot=dot,
        )


@dataclass
class PaginatedResponse:
    count: int = 0
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[Any] = field(default_factory=list)


@dataclass
class Thread:
    id: str = ""
    root_dot_id: str = ""
    dots: List[Dict] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Thread":
        return cls(
            id=data.get("id", ""),
            root_dot_id=data.get("root_dot_id", data.get("post_id", "")),
            dots=data.get("dots", []),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )


@dataclass
class ThreadView:
    thread: Optional[Thread] = None
    replies: List[Dot] = field(default_factory=list)
    all_dots: List[Dot] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThreadView":
        return cls(
            thread=Thread.from_dict(data.get("thread", {})),
            replies=[Dot.from_dict(d) for d in data.get("replies", [])],
            all_dots=[Dot.from_dict(d) for d in data.get("all_dots", [])],
        )


@dataclass
class ReplyPermission:
    permission: str = "everyone"
    allowed_users: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReplyPermission":
        return cls(
            permission=data.get("permission", "everyone"),
            allowed_users=data.get("allowed_users", []),
        )


@dataclass
class ChatMessage:
    id: str = ""
    content: str = ""
    conversation_id: str = ""
    sender_id: str = ""
    sender: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    is_read: bool = False
    is_own: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatMessage":
        return cls(
            id=data.get("id", ""),
            content=data.get("content", ""),
            conversation_id=data.get("conversation_id", ""),
            sender_id=data.get("sender_id", ""),
            sender=data.get("sender", {}),
            created_at=data.get("created_at", ""),
            is_read=data.get("is_read", False),
            is_own=data.get("is_own", False),
        )


@dataclass
class Conversation:
    id: str = ""
    name: str = ""
    type: str = "direct"
    participants: List[Dict[str, Any]] = field(default_factory=list)
    last_message: Optional[ChatMessage] = None
    unread_count: int = 0
    is_blocked: bool = False
    created_at: str = ""
    updated_at: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conversation":
        last = ChatMessage.from_dict(data["last_message"]) if data.get("last_message") else None
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            type=data.get("type", "direct"),
            participants=data.get("participants", []),
            last_message=last,
            unread_count=data.get("unread_count", 0),
            is_blocked=data.get("is_blocked", False),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )