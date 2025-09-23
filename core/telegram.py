import asyncio
from typing import Optional

from .config import get_settings


async def send_telegram_message_async(text: str) -> None:
    settings = get_settings()
    if not settings.telegram_bot_token or not settings.telegram_admin_chat_id:
        return
    try:
        import aiohttp

        async with aiohttp.ClientSession() as session:
            url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
            payload = {"chat_id": settings.telegram_admin_chat_id, "text": text}
            async with session.post(url, json=payload) as resp:
                await resp.text()
    except Exception:
        # Swallow errors to not block API flow
        return


def send_telegram_message(text: str) -> None:
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(send_telegram_message_async(text))
    except RuntimeError:
        asyncio.run(send_telegram_message_async(text))


