# ==========================================
# aiodot/wallet.py
# ==========================================

"""Wallet management module for MyDot.one."""

from typing import Dict, List, Any


class WalletManager:
    """Manage user wallets on MyDot.one."""

    def __init__(self, client):
        self.client = client

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.client._post("/wallet/create/", json=data)

    async def list(self) -> List[Dict[str, Any]]:
        data = await self.client._get("/wallet/list/")
        return data.get("results", []) if isinstance(data, dict) else data

    async def transactions(self, wallet_id: str) -> List[Dict[str, Any]]:
        data = await self.client._get(f"/wallet/transactions/{wallet_id}/")
        return data.get("results", []) if isinstance(data, dict) else data

    async def get(self, wallet_id: str) -> Dict[str, Any]:
        return await self.client._get(f"/wallet/{wallet_id}/")

    async def toggle_default(self, wallet_id: str) -> None:
        await self.client._post(f"/wallet/toggle/{wallet_id}/")