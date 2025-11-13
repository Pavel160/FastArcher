import aiohttp


async def errors_service(resp: aiohttp.ClientResponse, context: str):
    """Единообразно обрабатывает JSON-ответ от API."""
    try:
        data = await resp.json()
    except Exception:
        text = await resp.text()
        raise ValueError(f"Ошибка {context}: {resp.status}, {text}")

    if resp.status != 200:
        raise ValueError(data.get("detail") or f"Ошибка {context}")
    return data
