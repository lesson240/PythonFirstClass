import datetime 
import time
from datetime import date
import math
import re
import aiohttp
from bs4 import BeautifulSoup
import asyncio
import pymongo


async def fetch01_oliveyoung(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            area_info = soup.select("a[data-ref-onlbrndcd]")
            branddics = []
            for info in area_info:
                code = info["data-ref-onlbrndcd"]
                name = info.text
                collectiontime = date.today()
                item = [ i ["code"] for i in branddics]

                if code in item:
                    pass
                else:
                    branddic = {
                        "code": f"{code}",
                        "brand": f"{name}",
                        "time": f"{collectiontime}",
                        "status": "Old",
                    }
                    branddics.append(branddic)
            print(branddics)
            # myclient, mydb 접속
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["allcodatabase"]
            mycol = mydb["oliveyoungbrandlist"] 
            mycol.insert_many(branddics)

        await session.close()  # 43초 기록 # logging module 필요


def oliveyoungbrandlist():
    url = "https://www.oliveyoung.co.kr/store/main/getBrandList.do"
    """Function for scraping the brand list of the oliveyoung"""
    asyncio.run(fetch01_oliveyoung(url))

if __name__ == "__main__":
    start = time.time()
    # asyncio.run(main())
    oliveyoungbrandlist()
    # ScrapingBrowser.oliveyoungbrandshop(oliveyoung_page_brandshopdetail_arg)
    # ScrapingBrowser.oliveyounggoodsdetail(oliveyoung_page_goodsdetail_arg)
    # ManagingDatabase()
    end = time.time()
    print(end - start)

# aa = "17,000원\n14,900원 오늘드림\n4.5(49)"
# aa = "33,000원 오늘드림\n4.8(999+)"

# sub_condition = re.sub("(원|오늘드림|\n)"," ", aa)
# replace_condition = {"," : "_", "." : "_", "(" : "_", ")" : "_", "+" : "_"}
# condition_key = "".join(list(replace_condition.keys()))
# condition_value = "".join(list(replace_condition.values()))
# extract_value = sub_condition.translate(str.maketrans(condition_key,condition_value)).replace("_","").strip().split()

# if len(extract_value) == 2:
#     print(extract_value[0])
# else:
#     print(extract_value[1])

# totCnt = 105
# num_view = 48
# rows = 4
# # page = 1
# page_calculation = math.ceil(totCnt/num_view)
# print("총 페이지 수:",page_calculation)

# columns_ = []
# rows_ = []

# for page in range(1,page_calculation+1):

#     if page_calculation == 1:
#         num_columns = math.ceil(totCnt/rows)
#         for column in range(1,num_columns+1):
#             for row in range(1,5):
#                 columns_.append(column)
#                 rows_.append(row)
#                 # print("열:",column,"행:",row)
#     elif page_calculation > 1:
#         if page < page_calculation:
#             print("현재 페이지:",page)
#             num_columns = math.ceil(num_view / rows)
#             for column in range(1,num_columns+1):
#                 for row in range(1,5):
#                     columns_.append(column)
#                     rows_.append(row)
#                     # print("열:",column,"행:",row)
#         elif page == page_calculation:
#             print("현재 페이지:",page)
#             num_columns = math.ceil((totCnt - ((page - 1) * num_view)) / rows)
#             for column in range(1,num_columns+1):
#                 for row in range(1,5):
#                     columns_.append(column)
#                     rows_.append(row)
#                     # print("열:",column,"행:",row) 
# print(columns_,rows_)

# for page in range(page_calculation):


# if aa < num_view:
#     e = aa / 4
#     print(e)
#     print(math.ceil(e))





# totCnt = [36]
# maxCnt = 48

# calculation = totCnt[0]/maxCnt
# print(calculation)
# print(math.ceil(calculation))
# if __name__=="__main__":

#     num_viewnum_view = datetime.datetime.now()
#     cc = date.today()

#     print(num_viewnum_view, cc)


# num_view = ['hi', 'hello', 'num_viewye', 'hello', 'hi']
# a = 'helloo'


# try:
#     if a == num_view.index(a):
#         print(a)
# except ValueEsub_conditionor:
#     pass