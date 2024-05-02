# https://docs.aiohttp.org/en/stable/
# pip install aiohttp~=3.7.3

import requests
import time
import aiohttp
import asyncio

url_oy = "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EC%95%84%EB%B2%A4%EB%8A%90&listnum=48&giftYn=N&t_page=%EB%9E%AD%ED%82%B9&t_click=%EC%B5%9C%EA%B7%BC%EA%B2%80%EC%83%89%EC%96%B4&t_search_name=%EC%95%84%EB%B2%A4%EB%8A%90"
url_naver = "https://www.naver.com"
url_google = "https://www.google.com"

urls = [url_oy, url_naver, url_google] * 10
#def io_bound_func():
#    result = requests.get(url_naver)
#    return result

# if __name__=="__main__":
#    result = io_bound_func()
#    print(result)

async def fetcher(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        # result = [fetcher(session, url) for url in urls]
        # print(result)
        result = await asyncio.gather(*[fetcher(session, url) for url in urls])
        # result = await fetcher(session, urls[0])
        print(result)

if __name__=="__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)
