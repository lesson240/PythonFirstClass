# pip install lxml
# pip install numpy --user 관리자 권한 이슈를 해소 
# robots.txt  scraping으로 인한 지재권 등 윤리적 이슈 확인

"""
웹 크롤링: 검색 엔진의 구축 등을 위하여 특정한 방법으로 웹 페이지를 수집하는 프로그램
웹 스크래핑: 웹에서 데이터를 수집하는 프로그램
"""

from bs4 import BeautifulSoup  # Screen scraping 지원
# pip install beautifulsoup4  https://www.crummy.com/software/BeautifulSoup/  https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import asyncio  # 비동기 I/O 지원
# pip install asyncio  https://peps.python.org/pep-3156/
import aiohttp  # 비동기 HTTP Client/Server 지원
# pip install aiohttp   https://docs.aiohttp.org/en/stable/
import aiodns  # 비동기식 DNS 확인을 수행
# pip install aiodns   https://docs.aiohttp.org/en/stable/glossary.html#term-aiodns
import time

from selenium import webdriver  # Web browser 상호 작용을 자동화하는데 지원
# pip install -U selenium  https://www.selenium.dev/selenium/docs/api/py/index.html
from selenium.webdriver.chrome.service import Service as ChromeService  # selenium 4 에서는 chrome driver auto up-to-date 지원

from WebBrowser import Market


class ScrapingBrowser:

    def chrome_webdriver():
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        service = webdriver.ChromeService()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"  # chrome://version 에서 확인
        options = webdriver.ChromeOptions()
        
        # options.add_argument("headless") # no browser
        options.add_argument("window_size=1920x1080") # --window-size=x,y
        options.add_argument("lang=ko_KR") 
        options.add_argument("disable-gpu") # gpu err 발생시 , --disable-gpu로 변경
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("mute-audio") #--mute-audio
        # options.add_argument("inconnito") # secret mode

        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("detach", True)

        browser = webdriver.Chrome(service=service, options=options)
        browser.maximize_window()
        browser.get(Market.brand())
        # browser.implicitly_wait(10)
        # browser.quit()

        # return browser

    def OliveYoung():

        def brand():
            
            pass



    
if __name__=="__main__":

    ScrapingBrowser.chrome_webdriver()
    































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
#     start = time.time()
#     asyncio.run(main())
#     end = time.time()
#     print(end - start)