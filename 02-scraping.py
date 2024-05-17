# pip install lxml
# pip install numpy --user 관리자 권한 이슈를 해소
# robots.txt  scraping으로 인한 지재권 등 윤리적 이슈 확인

"""
웹 크롤링: 검색 엔진의 구축 등을 위하여 특정한 방법으로 웹 페이지를 수집하는 프로그램
웹 스크래핑: 웹에서 데이터를 수집하는 프로그램
"""

# pip install -U selenium  https://www.selenium.dev/selenium/docs/api/py/index.html Web browser 상호 작용을 자동화하는데 지원
from selenium import webdriver

# https://selenium-python.readthedocs.io/locating-elements.html#locating-by-id
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# pip install asyncio  https://peps.python.org/pep-3156/ 비동기 I/O 지원
import asyncio

# pip install beautifulsoup4  https://www.crummy.com/software/BeautifulSoup/  https://www.crummy.com/software/BeautifulSoup/bs4/doc/ Screen scraping 지원
from bs4 import BeautifulSoup

# pip install aiohttp   https://docs.aiohttp.org/en/stable/ 비동기 HTTP Client/Server 지원
import aiohttp

# pip install aiodns   https://docs.aiohttp.org/en/stable/glossary.html#term-aiodns  비동기식 DNS 확인을 수행
import aiodns

# selenium 4 에서는 chrome driver auto up-to-date 지원
from selenium.webdriver.chrome.service import Service as ChromeService

# pip install pytest   https://docs.pytest.org/en/latest/
import re

# pip install pymongo   https://www.w3schools.com/PYTHON/python_mongodb_getstarted.asp
import pymongo

# https://docs.python.org/ko/3/library/datetime.html#date-objects
from datetime import date

# https://docs.python.org/ko/3/library/math.html
import math
import time


class ScrapingBrowser:
    """Brower를 Scraping 해주는 class"""

    def __init__(self, name, url):
        self.name = name
        self.url = url

    async def fetch02_oliveyoung(self):
        """chrome webdriver 함수"""
        # 개발자도구에서 Preferences > Debugger > Disable JavaScript 로 확인
        async with aiohttp.ClientSession() as driver:
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

            driver = webdriver.Chrome(service=service, options=options)
            driver.maximize_window()

            driver.get(self.url)

            # myclient, mydb 접속
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["allcodatabase"]
            mycol = mydb["oliveyoungbrandshop"]

            totCnt = []  # 실제 상품 수
            goods_totCnt = driver.find_element(By.ID, "totCnt").text
            totCnt.append(int(goods_totCnt))
            page_calculation = math.ceil(totCnt[0] / 48)  # total page 구하는 공식
            num_view = 48
            num_column = []  # 상품 열 수 기록
            num_row = []  # 상품 행 수 기록
            # 단순 열/행에 대한 for문으로 list에 담아도 될 듯 함. 다시 함수 재정의
            for page in range(1, page_calculation + 1):
                if page_calculation == 1:
                    num_columns = math.ceil(totCnt[0] / 4)
                    for column in range(1, num_columns + 1):
                        for row in range(1, 5):
                            num_column.append(column)
                            num_row.append(row)
                elif page_calculation > 1:
                    if page < page_calculation:
                        totCnt.append(48)  # 페이지 내 상품 수 정의
                        num_columns = math.ceil(num_view / 4)
                        for column in range(1, num_columns + 1):
                            for row in range(1, 5):
                                num_column.append(column)
                                num_row.append(row)
                    elif page == page_calculation:
                        pages = totCnt[0] - ((page - 1) * 48)
                        totCnt.append(pages)  # 페이지 내 상품 수 정의
                        num_columns = math.ceil(
                            (totCnt[0] - ((page - 1) * num_view)) / 4
                        )
                        for column in range(1, num_columns + 1):
                            for row in range(1, 5):
                                num_column.append(column)
                                num_row.append(row)

            if totCnt[0] > 24:  # 48개 보기 방식으로의 변경
                driver.find_element(
                    By.XPATH, '//*[@id="sub_gbn_cate"]/div[2]/div[2]/ul/li[3]'
                ).click()

            num = [1]
            for page in range(page_calculation):
                for idx in range(0, totCnt[page + 1]):
                    goodsno = (
                        driver.find_element(
                            By.XPATH,
                            f'//*[@id="allGoodsList"]/ul[{num_column[idx]}]/li[{num_row[idx]}]/div/div[1]/a',
                        )
                        .get_attribute("data-ref-goodsno")
                        .strip()
                    )
                    goodsname = driver.find_element(
                        By.XPATH,
                        f'//*[@id="allGoodsList"]/ul[{num_column[idx]}]/li[{num_row[idx]}]/div/div[1]/a/span',
                    ).text.strip()
                    goodstotal = driver.find_element(
                        By.XPATH,
                        f'//*[@id="allGoodsList"]/ul[{num_column[idx]}]/li[{num_row[idx]}]/div/div[1]/div[2]',
                    ).text
                    # 최종 판매가(할인가) 추출 함수
                    sub_condition = re.sub("(원|오늘드림|\n)", " ", goodstotal)
                    replace_condition = {
                        ",": "_",
                        ".": "_",
                        "(": "_",
                        ")": "_",
                        "+": "_",
                    }
                    condition_key = "".join(list(replace_condition.keys()))
                    condition_value = "".join(list(replace_condition.values()))
                    extract_value = (
                        sub_condition.translate(
                            str.maketrans(condition_key, condition_value)
                        )
                        .replace("_", "")
                        .strip()
                        .split()
                    )
                    if len(extract_value) == 2:
                        goodstotal = extract_value[0]
                    else:
                        goodstotal = extract_value[1]

                    # 일시 품절 추출 함수
                    goodssoldout = driver.find_element(
                        By.XPATH,
                        f'//*[@id="allGoodsList"]/ul[{num_column[idx]}]/li[{num_row[idx]}]/div/a',
                    ).text
                    if bool(goodssoldout) == True:
                        goodssoldout = goodssoldout
                    elif bool(goodssoldout) == False:
                        goodssoldout = "판매"

                    # 세일 정보 추출 함수
                    goodssale = driver.find_element(
                        By.XPATH,
                        f'//*[@id="allGoodsList"]/ul[{num_column[idx]}]/li[{num_row[idx]}]/div/div[1]/div[3]',
                    ).text
                    if bool(goodssale) == True:
                        goodssale = "세일"
                    elif bool(goodssale) == False:
                        goodssale = "원가"

                    collectiontime = date.today()
                    elementlist = {
                        "number": f"{num[0]}",
                        "code": f"{goodsno}",
                        "name": f"{goodsname}",
                        "total_price": f"{goodstotal}",
                        "solde_out": f"{goodssoldout}",
                        "sale": f"{goodssale}",
                        "time": f"{collectiontime}",
                    }
                    num[0] = num[0] + 1
                    mycol.create_index("number", unique=True)
                    mycol.update_one(
                        {"code": f"{goodsno}"}, {"$set": elementlist}, upsert=True
                    )

                    # async await 함수 적용하기

                if (page + 1) < page_calculation:
                    driver.find_element(
                        By.XPATH, '//*[@id="allGoodsList"]/div/a'
                    ).click()

            driver.close()

    async def fetch03_oliveyoung(self):
        """scraping from a page of oliveyoung goods detail"""
        async with aiohttp.ClientSession() as driver:
            service = webdriver.ChromeService()
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
                537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
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
            driver = webdriver.Chrome(service=service, options=options)
            driver.maximize_window()
            driver.get(self.url)

            # # myclient, mydb 접속
            # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            # mydb = myclient["allcodatabase"]
            # mycol = mydb["oliveyounggoodsdetail"]

            # 상품명 추출하는 함수
            goodsname = driver.find_element(
                By.XPATH, '//*[@id="Contents"]/div[2]/div[2]/div/p[2]'
            ).text.strip()

            # 가격 정보 추출하는 함수
            price_class = driver.find_elements(By.CLASS_NAME,"price")        

            if len(price_class) == 1:
                goodspricelist = driver.find_element(By.CLASS_NAME, "price").text
                goodstotal = re.sub("(원|,|\n)", "", goodspricelist)

            else:
                driver.find_element(By.ID, "btnSaleOpen").click()
                goodspricelist = driver.find_element(By.ID, "saleLayer").text
                sub_condition = re.sub("(혜택|정보|판매가|원|최적가|레이어|닫기|\n)", " ", goodspricelist)
                replace_condition = {
                    ",": "_",
                    # ".": "_",
                    "(": "_",
                    ")": "_",
                    "~": "_",
                    "-": "_"
                }
                condition_key = "".join(list(replace_condition.keys()))
                condition_value = "".join(list(replace_condition.values()))
                extract_value = (
                    sub_condition.translate(
                        str.maketrans(condition_key, condition_value)
                    )
                    .replace("_", "")
                    .strip()
                    .split()
                )

                if "쿠폰" in extract_value:
                    coupon = extract_value.index("쿠폰")
                    del extract_value[coupon]
                    del extract_value[coupon - 1]
                    if "세일" in extract_value:
                        sale = extract_value.index("세일")
                        del extract_value[sale]
                        if len(extract_value) == 8:
                            goodstotal = extract_value[7]
                            goodsorign = extract_value[0]
                            salestart = extract_value[1]
                            saleend = extract_value[2]
                            saleprice = extract_value[3]
                            couponstart = extract_value[4]
                            couponend = extract_value[5]
                            couponprice = extract_value[6]
                        else:
                            return print("len_extract_value dose not match")
                    else:
                        if len(extract_value) == 5:
                            goodstotal = extract_value[4]
                            goodsorign = extract_value[0]
                            couponstart = extract_value[1]
                            couponend = extract_value[2]
                            couponprice = extract_value[3]
                        else:
                            return print("len_extract_value dose not match")
                elif "세일" in extract_value:
                    sale = extract_value.index("세일")
                    del extract_value[sale]                      
                    if len(extract_value) == 5:
                        goodstotal = extract_value[4]
                        goodsorign = extract_value[0]
                        salestart = extract_value[1]
                        saleend = extract_value[2]
                        saleprice = extract_value[3]
                    else:
                        return print("len_extract_value dose not match")
                # else:
                #     goodstotal = extract_value[len(extract_value)-1]
                #     goodsorign = extract_value[0]                    

            # 배송 정보 추출하는 함수  # 배송 정보 최적화 함수 만들기
            delivery_xpath = driver.find_elements(By.XPATH, '//*[@id="Contents"]/div[2]/div[2]/div/div[3]/div[1]/ul/li')
            if delivery_xpath == 1:
                goodsdelivery = driver.find_element(By.XPATH, '//*[@id="Contents"]/div[2]/div[2]/div/div[3]/div[1]/ul/li/div/b[1]').text
            else:
                goodsdelivery = driver.find_element(By.XPATH,'//*[@id="Contents"]/div[2]/div[2]/div/div[3]/div[1]/ul/li[1]/div').text

            # 일시품절 text 추출하는 함수 만들기
            soldout_css = driver.find_element(By.CSS_SELECTOR, "div.prd_btn_area.new-style.type1").text
            sub_condition = re.sub("\n", " ", soldout_css).split()
            if sub_condition[0] == "일시품절":
                goodssoldout = "일시품절"
            else:
                goodssoldout = "판매"

            # 썸네일(5개) src 추출하는 함수
            thumbcount = len(driver.find_elements(
                        By.XPATH, f'//*[@id="prd_thumb_list"]/li'))
            for thumb in range(1,thumbcount+1):
                driver.find_element(
                    By.XPATH, f'//*[@id="prd_thumb_list"]/li[{thumb}]'
                ).click()
                goodsthumb = driver.find_element(By.ID, "mainImg").get_attribute(
                    "src"
                )

            # 상품정보 제공고시 png 생성 함수
            btn_buyinfo = driver.find_element(By.ID, "buyInfo")
            if bool(btn_buyinfo) == True:
                btn_buyinfo.click()
                buy_info = driver.find_element(By.ID, "artcInfo")
                buy_info.screenshot(f"{goodslist['아벤느 오 떼르말 300ml 2입 기획']}.png")
            else:
                pass

            # # mongDB 적재용 배열 완료하기 ( + page ulr 포함)
            # elementlist = {
            #     # "number": f"{num[0]}",
            #     # "code": f"{goodsno}",
            #     "name": f"{goodsname}",
            #     # "total_price": f"{goodstotal}",
            #     "solde_out": f"{goodssoldout}",
            #     # "sale": f"{goodssale}",
            #     "time": f"{collectiontime}",
            # }

            # mycol.create_index("number", unique=True)
            # collectiontime = date.today()

            # # num[0] = num[0] + 1
            # # mycol.update_one(
            # #     {"code": f"{goodsno}"}, {"$set": elementlist}, upsert=True
            # # )

            # async await 함수 적용하기
            driver.close()

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
                    collectiontime = date.today()
                    branddic = {
                        "number": f"{num}",
                        "code": f"{code}",
                        "brand": f"{name}",
                        "time": f"{collectiontime}",
                        "staus": True,
                    }
                    num = num + 1
                    # myclient, mydb 접속
                    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                    mydb = myclient["allcodatabase"]
                    mycol = mydb["oliveyoungbrandlist"]
                    # 중복 field 확인 후, update 및 field 없을 경우 추가 insert
                    mycol.create_index("number", unique=True)
                    mycol.update_one(
                        {"code": f"{code}"}, {"$set": branddic}, upsert=True
                    )
                    # print(x.inserted_id)

            await session.close()  # 43초 기록 # logging module 필요

    def oliveyoungbrandlist(self):
        """Function for scraping the brand list of the oliveyoung"""
        asyncio.run(ScrapingBrowser.fetch01_oliveyoung(self))

    def oliveyoungbrandshop(self):
        """Function for scraping the detail page of the oliveryoung brand shop"""

        asyncio.run(ScrapingBrowser.fetch02_oliveyoung(self))

    def oliveyounggoodsdetail(self):
        """Function for scraping the detail page of the oliveryoung goods"""
        asyncio.run(ScrapingBrowser.fetch03_oliveyoung(self))


# front input values

browser_db = ["https://www.oliveyoung.co.kr"]
oliveyoung_brandlist = {"아벤느": "A000003"}
goodslist = {"아벤느 오 떼르말 300ml 2입 기획": "A000000188816"}

oliveyoung_page_brandlist_arg = ScrapingBrowser(
    "올리브영", f"{browser_db[0]}/store/main/getBrandList.do"
)

oliveyoung_page_brandshopdetail_arg = ScrapingBrowser(
    "올리브영",
    f"{browser_db[0]}/store/display/getBrandShopDetail.do?onlBrndCd={oliveyoung_brandlist['아벤느']}",
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
    # ScrapingBrowser.oliveyoungbrandlist(oliveyoung_page_brandlist_arg)
    # ScrapingBrowser.oliveyoungbrandshop(oliveyoung_page_brandshopdetail_arg)
    ScrapingBrowser.oliveyounggoodsdetail(oliveyoung_page_goodsdetail_arg)
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
