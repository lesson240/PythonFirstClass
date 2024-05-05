from re import search
from types import NoneType
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from urllib.request import urlretrieve
import os
# import pandas as pd
# import csv
# import urllib.request

# options.headless = True

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("window_size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36")
options.add_argument("lang=ko_KR") # 언어 미설정으로 차단되는 경우에 옵션으로 언어 설정
options.add_argument("disable-gpu") # 여기서 GPU err 발생시,  --disable-gpu로 앞에 dash(-)를 두개 더 붙이기
# 이 버그는 크롬 자체에 있는 문제점. 브라우저들은 CPU의 부담을 줄이고 좀더 빠른 화면 렌더링을 위해 GPU를 통해 그래픽 가속을 사용하는데, 
# 이 부분이 크롬에서 버그를 일으키는 현상을 보이고 있습니다
# 혹은 options.add_argument("--disable-gpu")



browser = webdriver.Chrome("chromedriver", chrome_options=options)
browser.maximize_window()

# filename = "test.csv"
# f = open(filename, "w", encoding="utf-8-sig", newline="") 
# writer = csv.writer(f)

# title = "대카테고리	중카테고리	소카테고리".split("\t")
# writer.writerow(title)

category_num =  50000810 # input()
start_num = 0 # int(input())
end_num = 1  # int(input())

url = "https://search.shopping.naver.com/search/category/100000365\
    ?catId={}&frm=NVSHOVS&origQuery&pagingIndex={}&pagingSize=80\
        &productSet=overseas&query&sort=rel&timestamp=&viewType=list"\
            .format(category_num, end_num)

browser.get(url)
interval = 1 # 스크롤 무빙 대기 시간
previous_height = browser.execute_script("return document.body.scrollHeight") # 현재 문서 높이 정의
# browser.execute_script("window.open('http://daum.net', 'new_window')")
browser.execute_script("window.open('');")
# 가장 최근에 연 탭으로 전환 : [-1], 첫번째 탭 : [0]
browser.switch_to.window(browser.window_handles[0])
# browser.find_element(By.XPATH, "/html/body").send_keys(Keys.COMMAND + "t")
# browser.get("https://daum.net")

def find_in_src():
    if "jpg" in path_src:
        return "jpg"
    elif "png" in path_src:
        return "png"

while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)") # 스크롤 가장 아래로 이동
    time.sleep(interval) # 페이지 로딩
    current_height = browser.execute_script("return document.body.scrollHeight")
    if current_height == previous_height:
        break

    previous_height = current_height

soup = BeautifulSoup(browser.page_source, "lxml")

info_area = soup.find_all("div", attrs={"class":"basicList_inner__eY_mq"})

os.chdir(os.path.join("libs_self", "temp_images"))

for idx, info in enumerate(info_area):
    # 상품명 get
    pdt_name = info.find("a", attrs={"class":"basicList_link__1MaTN"})
    if pdt_name:
        pdt_name = [pdt_name.get_text().strip()]
        if pdt_name == None:
            continue
    else:
        continue

    # 상품URL get
    pdt_href = info.find("a", attrs={"class":"thumbnail_thumb__3Agq6"})
    pdt_url = pdt_href["href"].strip()
    # print(pdt_url)
    # if pdt_href:
    #     pdt_href = [pdt_href["href"].strip()]
    #     if pdt_href == None:
    #         continue
    # else:
    #     continue

    # print(pdt_href)
    browser.switch_to.window(browser.window_handles[1])
    browser.get(f"{pdt_url}")
    soup = BeautifulSoup(browser.page_source, "lxml") # get 하는 page의 url이 바뀔때는 soup 객체 변수 재선언 필요.   

    try:
        WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body")))
        # find_until = WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body")))
        # if find_until:
        #     time.sleep(1)
    except:
        browser.quit()
        break
    
    # def 정의하여 재사용할 것.
    # img tag 변수 설정
    pdt_thum_01 = soup.find("div", attrs={"class":"image_thumb__20xyr"})
    pdt_thum_02 = soup.find("img", attrs={"class":"_2P2SMyOjl6"})
    pdt_thum_03 = soup.find("img", attrs={"class":"prod-image__detail"})


    # 2~3개의 src 중에서 값이 있는 주소 찾기 
    if type(pdt_thum_01) != NoneType:
        path_src = pdt_thum_01.find("img")["src"]
        print(path_src)
        urlretrieve(path_src, f"{idx}.{find_in_src()}")
    elif type(pdt_thum_02) != NoneType:
        path_src = pdt_thum_02["src"]
        print(path_src)
        urlretrieve(path_src, f"{idx}.{find_in_src()}")
    elif type(pdt_thum_03) != NoneType:
        path_src = pdt_thum_03["src"]
        print("https:"+ path_src)
        urlretrieve("https:"+ path_src, f"{idx}.{find_in_src()}")
    else: # time out에 따른 src 주소 찾기 실패 시, time.sleep을 두어 재시도
        time.sleep(1)
        if type(pdt_thum_01) != NoneType:
            path_src = pdt_thum_01.find("img")["src"]
            print(path_src)
            urlretrieve(path_src, f"{idx}.{find_in_src()}")
        elif type(pdt_thum_02) != NoneType:
            path_src = pdt_thum_02["src"]
            print(path_src)
            urlretrieve(path_src, f"{idx}.{find_in_src()}")
        elif type(pdt_thum_03) != NoneType:
            path_src = pdt_thum_03["src"]
            print("https:"+ path_src)
            urlretrieve("https:"+ path_src, f"{idx}.{find_in_src()}")
        else:
            time.sleep(2)
            if type(pdt_thum_01) != NoneType:
                path_src = pdt_thum_01.find("img")["src"]
                print(path_src)
                urlretrieve(path_src, f"{idx}.{find_in_src()}")
            elif type(pdt_thum_02) != NoneType:
                path_src = pdt_thum_02["src"]
                print(path_src)
                urlretrieve(path_src, f"{idx}.{find_in_src()}")
            elif type(pdt_thum_03) != NoneType:
                path_src = pdt_thum_03["src"]
                print("https:"+ path_src)
                urlretrieve("https:"+ path_src, f"{idx}.{find_in_src()}")
            else:
                browser.execute_script("window.open('');")
                browser.switch_to.window(browser.window_handles[2])
                browser.get(f"{pdt_url}")

                time.sleep(5)
                if type(pdt_thum_01) != NoneType:
                    path_src = pdt_thum_01.find("img")["src"]
                    print(path_src)
                    urlretrieve(path_src, f"{idx}.{find_in_src()}")
                elif type(pdt_thum_02) != NoneType:
                    path_src = pdt_thum_02["src"]
                    print(path_src)
                    urlretrieve(path_src, f"{idx}.{find_in_src()}")
                elif type(pdt_thum_03) != NoneType:
                    path_src = pdt_thum_03["src"]
                    print("https:"+ path_src)
                    urlretrieve("https:"+ path_src, f"{idx}.{find_in_src()}")
                else:
                    print("img tag 변수 확인 or time_out 확인 or 차단 이슈")
                    browser.close() # 현재 tab 닫기
                    browser.switch_to.window(browser.window_handles[1])
                    continue

    # if type(pdt_thum_01) == NoneType:
    #     pdt_thum_01 = str("")

    # if type(pdt_thum_02) == NoneType:
    #     pdt_thum_02 = str("")

    browser.switch_to.window(browser.window_handles[0])

browser.quit()


#     # 썸네일 get / open tab
#     browser.find_element(By.XPATH, "/html/body").send_keys(Keys.COMMAND + Keys.TAB)
#     # You can use (Keys.CONTROL + 't') on other OSs
#     # 로드할 페이지
#     browser.get(f"{pdt_href}")
    
#     # # close the tab
#     # # (Keys.CONTROL + 'w') on other OSs.
#     # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 


#     # driver.close()

#     # pdt_thum = info.find("a", attrs={"class":"thumbnail_thumb__3Agq6"}).find("img")
#     # if pdt_thum:
#     #     pdt_thum = pdt_thum["src"]
#     #     if pdt_thum == None:
#     #         continue
#     # else:
#     #     continue

#     # writer.writerow(pdt_name + pdt_href)
#     # print("상품명:", pdt_name, "가격:", pdt_price_l, "등록일:", update, review_purch, review_pur_f)


