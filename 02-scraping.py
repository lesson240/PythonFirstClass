# https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html#installing-beautiful-soup
# pip install beautifulsoup4
# pip install lxml
# robots.txt

"""
웹 크롤링: 검색 엔진의 구축 등을 위하여 특정한 방법으로 웹 페이지를 수집하는 프로그램
웹 스크래핑: 웹에서 데이터를 수집하는 프로그램
"""

from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time


oliveYong = "https://www.oliveyoung.co.kr/store/display/getBrandShopDetail.do?onlBrndCd=A000003"
test = "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010013&fltDispCatNo=&prdSort=01"
test2 = "https://www.oliveyoung.co.kr/store/main/getSaleList.do?dispCatNo=900000100090001&fltDispCatNo=&prdSort=01"

urls = [f"{test2}&pageIdx={i}&rowsPerPage=24" for i in range(1,3)]


async def fetch(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        prd_info = soup.find_all("div","prd_info")
        # print(prd_info)
        for info in prd_info:
            product_name = info.find("p", "tx_name")
            if product_name is not None:
                print(product_name.text)


async def main():
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[fetch(session, url) for url in urls])

if __name__=="__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)
