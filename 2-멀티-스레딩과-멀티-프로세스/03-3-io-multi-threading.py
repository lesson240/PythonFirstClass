# https://docs.python.org/3.7/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
import requests
import time
import os
import threading
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor


url_oy = "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EC%95%84%EB%B2%A4%EB%8A%90&listnum=48&giftYn=N&t_page=%EB%9E%AD%ED%82%B9&t_click=%EC%B5%9C%EA%B7%BC%EA%B2%80%EC%83%89%EC%96%B4&t_search_name=%EC%95%84%EB%B2%A4%EB%8A%90"
url_naver = "https://www.naver.com"
url_google = "https://www.google.com"


urls = [url_oy, url_naver, url_google] * 10


def fetcher(params):
    session = params[0]
    url = params[1]
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    with session.get(url) as response:
        return response.text
    
def main():

    executor = ThreadPoolExecutor(max_workers=10)
    # Thread 할당 또한 연산 작업임으로 메모리 점유율이 높음, Threading async process를 활용하는 게 좋음

    with requests.Session() as session:
        params = [(session, url) for url in urls]
        result = list(executor.map(fetcher, params))
        print(result)

if __name__=="__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start) # requests single thread workers= 1 기록 4.35초 , multi threading worker = 10  기록 2.69초
