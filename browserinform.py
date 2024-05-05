"""
WebBrowser infomation을 managing 하기 위함
purpose is
1. DB 축적
2. DB 유효성 검증
3. DB 유지보수 효율성
"""


class Market:
    """Scraping 하려는 Market 정보"""

    def __init__(self, name, url):

        self.name = name
        self.url = url

    # def titles(self):
    #     pass

    # def link():
    #     pass

    # def main():
    #     pass

    # def list():
    #     pass

    # def store():
    #     pass

    # def category():
    #     pass

    def brand(self):
        """brand page url"""
        print(f"안녕, 출력 {self.name},{self.url}")
        return self.url

    # def special():
    #     pass


oliveyoung = ["https://www.oliveyoung.co.kr"]
oliveyoung_brand = Market("올리브영", f"{oliveyoung[0]}/store/main/getBrandList.do")


if __name__ == "__main__":
    print(Market.brand(oliveyoung_brand))
    # print(oliveyoung_brand.url)
    # print(oliveyoung[0])
