import os
import aiohttp
import asyncio
from config import get_secret
import aiofiles
from fake_useragent import UserAgent

# from user_agent import generate_user_agent, generate_navigator

# print(generate_user_agent(device_type='desktop'))
# print(generate_user_agent(os='win', device_type='desktop'))
# print(generate_user_agent(os=('mac', 'linux'), device_type='desktop'))

# navigator = generate_navigator()
# print(navigator)
# print(navigator['platform'])

# pip install aiofiles==0.7.0
# pip install fake_useragent
# pip install user-agent

ua = UserAgent()
ua.random

async def img_downloader(session, img):
    img_name = img.split("/")[-1].split("?")[0]

    try:
        os.mkdir("./images")
    except FileExistsError:
        pass

    async with session.get(img) as response:
        if response.status == 200:
            async with aiofiles.open(f"./images/{img_name}", mode="wb") as file:
                await file.write(await response.read())

async def fetch(session, url, i):
    print(i + 1)
    headers = {
        "X-Naver-Client-Id" : get_secret("NAVER_API_ID"),
        "X-Naver-Client-Secret" : get_secret("NAVER_API_SECRET"),
        "User-Agent" : ua.random,
    }
    async with session.get(url, headers=headers) as response:
        result = await response.json()
        items = result["items"]
        images = [ item['link'] for item in items]
        await asyncio.gather(*[img_downloader(session, img) for img in images])

async def main():
    BASE_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "cat"
    urls = [f"{BASE_URL}?query={keyword}&display=20&start={1 + i*20}" for i in range(10)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url, i) for i, url in enumerate(urls)])

if __name__ == "__main__":
    asyncio.run(main())