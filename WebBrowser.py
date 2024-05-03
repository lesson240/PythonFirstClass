"""
WebBrowser infomation을 managing 하기 위함
purpose is
1. DB 축적
2. DB 유효성 검증
3. DB 유지보수 효율성 
"""

class Market:

    oliveyoung = "https://www.oliveyoung.co.kr"

    def titles():
        pass

    def link():
        pass

    def main():
        pass

    def list():
        pass

    def store():
        pass

    def category():
        pass

    def brand():
        url = f"{Market.oliveyoung}/store/main/getBrandList.do"
        name = "올리브영"
        return url
        print(name)

    def special():
        pass
    
    

if __name__=="__main__":
    print(Market.brand())