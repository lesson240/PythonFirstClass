# pip install lxml
# pip install numpy --user 관리자 권한 이슈를 해소
# robots.txt  scraping으로 인한 지재권 등 윤리적 이슈 확인

"""
웹 크롤링: 검색 엔진의 구축 등을 위하여 특정한 방법으로 웹 페이지를 수집하는 프로그램
웹 스크래핑: 웹에서 데이터를 수집하는 프로그램
"""

# pip install -U selenium  https://www.selenium.dev/selenium/docs/api/py/index.html
from selenium import webdriver  # Web browser 상호 작용을 자동화하는데 지원

# pip install asyncio  https://peps.python.org/pep-3156/
import asyncio  # 비동기 I/O 지원

# pip install beautifulsoup4  https://www.crummy.com/software/BeautifulSoup/  https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup  # Screen scraping 지원

# pip install aiohttp   https://docs.aiohttp.org/en/stable/
import aiohttp  # 비동기 HTTP Client/Server 지원

# pip install aiodns   https://docs.aiohttp.org/en/stable/glossary.html#term-aiodns
import aiodns  # 비동기식 DNS 확인을 수행

import time

# selenium 4 에서는 chrome driver auto up-to-date 지원
from selenium.webdriver.chrome.service import Service as ChromeService

# pip install pytest   https://docs.pytest.org/en/latest/
# import re

# pip install pymongo   https://www.w3schools.com/PYTHON/python_mongodb_getstarted.asp
import pymongo 
from types import NoneType




class ScrapingBrowser:
    """Brower를 Scraping 해주는 class"""

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def chrome_webdriver(self):
        """chrome webdriver 함수"""
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        service = webdriver.ChromeService()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
            537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        # chrome://version 에서 확인
        options = webdriver.ChromeOptions()

        # options.add_argument("headless") # no browser
        options.add_argument("window_size=1920x1080")  # --window-size=x,y
        options.add_argument("lang=ko_KR")
        options.add_argument("disable-gpu")  # gpu err 발생시 , --disable-gpu로 변경
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("mute-audio")  # --mute-audio
        # options.add_argument("inconnito") # secret mode

        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("detach", True)

        browser = webdriver.Chrome(service=service, options=options)
        browser.maximize_window()

        browser.get(self.url)
        # print(self.url)
        # browser.implicitly_wait(10)
        # browser.quit()

        # return browser


    def oliveyoung(self):
        """scraping oliveyoung"""
        # ScrapingBrowser.chrome_webdriver(self)
        # print(self)
        
    async def fetch01_oliveyoung(self):
        """aiohttp ClientSession"""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                # print(resp.status)
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                area_info = soup.select("a[data-ref-onlbrndcd]")
                num = 1
                for info in area_info:
                    code = info["data-ref-onlbrndcd"]
                    name = info.text
                    branddic = {"number":f"{num}","code":f"{code}","brand":f"{name}","staus":True}
                    num = num + 1
                    # myclient, mydb 접속
                    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                    mydb = myclient["allcodatabase"]   
                    mycol = mydb["oliveyoungbrandlist"]
                    # 중복 field 확인 후, update 및 field 없을 경우 추가 insert 
                    mycol.create_index("number", unique=True)
                    mycol.update_one({"code":f"{code}"}, {"$set":branddic}, upsert=True)                          
                    # print(x.inserted_id)

            await session.close() # 43초 기록
       

    def oliveyoungbrandlist(self):
        """oliveyoung brand list scraping function"""
        asyncio.run(ScrapingBrowser.fetch01_oliveyoung(self))







browser_db = ["https://www.oliveyoung.co.kr"]
oliveyoung_brandlist = {"아벤느": "A000003"}
goodslist = {"아벤느 오 떼르말 300ml 2입 기획": "A000000010498"}

oliveyoung_page_brandlist_arg = ScrapingBrowser(
    "올리브영", f"{browser_db[0]}/store/main/getBrandList.do"
)

oliveyoung_page_brandshopdetail_arg = ScrapingBrowser(
    "올리브영",
    f"{browser_db[0]}/display/getBrandShopDetail.do?onlBrndCd={oliveyoung_brandlist['아벤느']}",
)
oliveyoung_page_goodsdetail_arg = ScrapingBrowser(
    "올리브영",
    f"{browser_db[0]}/store/goods/getGoodsDetail.do?goodsNo={goodslist['아벤느 오 떼르말 300ml 2입 기획']}",
)

oliveyoung_page_brandlist = f"{browser_db[0]}/store/main/getBrandList.do"
oliveyoung_page_brandshopdetail = f"{browser_db[0]}/display/getBrandShopDetail.do?onlBrndCd={oliveyoung_brandlist['아벤느']}"
oliveyoung_page_goodsdetail = f"{browser_db[0]}/store/goods/getGoodsDetail.do?goodsNo={goodslist['아벤느 오 떼르말 300ml 2입 기획']}"






if __name__ == "__main__":
    start = time.time()
    # asyncio.run(main())
    ScrapingBrowser.oliveyoungbrandlist(oliveyoung_page_brandlist_arg)
    # ManagingDatabase()
    end = time.time()
    print(end - start)
    # ScrapingBrowser.chrome_webdriver(oliveyoung_page_brandlist)


# async def main():
#     """aiohttp ClientSession"""
#     async with aiohttp.ClientSession() as session:
#         async with session.get(oliveyoung_page_brandlist) as resp:
#             print(resp.status)
#             html = await resp.text()
#             soup = BeautifulSoup(html, "html.parser")
#             area_info = soup.select("a[data-ref-onlbrndcd]")
#             for i in area_info:                      
#                print(i["data-ref-onlbrndcd"], i.text)
#         await session.close()















# oliveYong = "https://www.oliveyoung.co.kr/store/display/getBrandShopDetail.do?onlBrndCd=A000003"
# test = "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010013&fltDispCatNo=&prdSort=01"
# test2 = "https://www.oliveyoung.co.kr/store/main/getSaleList.do?dispCatNo=900000100090001&fltDispCatNo=&prdSort=01"

# urls = [f"{test2}&pageIdx={i}&rowsPerPage=24" for i in range(1,3)]


# async def fetch(session, url):
#     async with session.get(url) as response:
#         html = await response.text()
#         soup = BeautifulSoup(html, 'html.parser')
#         prd_info = soup.find_all("div","prd_info")
#         # print(prd_info)
#         for info in prd_info:
#             product_name = info.find("p", "tx_name")
#             if product_name is not None:
#                 print(product_name.text)


# async def main():
#     async with aiohttp.ClientSession() as session:
#         result = await asyncio.gather(*[fetch(session, url) for url in urls])

# if __name__=="__main__":

#     asyncio.run(main())
#     end = time.time()
#     print(end - start)
