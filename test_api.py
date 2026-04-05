import asyncio
import httpx

async def test():
    async with httpx.AsyncClient() as client:
        r = await client.post('http://127.0.0.1:8000/shortener', json={'long_url': 'https://www.google.com'})
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")

asyncio.run(test())
