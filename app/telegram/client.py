from dataclasses import dataclass

import httpx


class TelegramAPIError(RuntimeError):
    pass


@dataclass
class TelegramClient:
    token: str

    @property
    def api_base(self) -> str:
        return f"https://api.telegram.org/bot{self.token}"

    async def _call(self, method: str, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.api_base}/{method}",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        if not data.get("ok"):
            raise TelegramAPIError(
                data.get("description") or f"Telegram {method} failed"
            )
        return data["result"]

    async def send_message(
        self,
        chat_id: int,
        text: str,
        *,
        reply_to_message_id: int | None = None,
    ) -> dict:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        }
        if reply_to_message_id is not None:
            payload["reply_parameters"] = {
                "message_id": reply_to_message_id,
                "allow_sending_without_reply": True,
            }
        return await self._call("sendMessage", payload)

    async def send_chat_action(self, chat_id: int, action: str = "typing") -> None:
        await self._call(
            "sendChatAction",
            {"chat_id": chat_id, "action": action},
        )

    async def download_file(self, file_id: str) -> bytes:
        file_info = await self._call("getFile", {"file_id": file_id})
        file_path = file_info.get("file_path")
        if not file_path:
            raise TelegramAPIError("Telegram did not return file_path")

        url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content
