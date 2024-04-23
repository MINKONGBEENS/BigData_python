# 동적 크롤링 : 동적 사이트에서 정보를 가지고 오는 작업
# 동적 웹 페이지 -> 자바스크립트를 사용하여 페이지가 연결 되어 있는 형태
# 원하는 데이터가 자바스크립트가 동작해야 노출 됨
# Java script를 쓰기 때문에 정적 크롤링처럼 HTML로 쉽게 구조를 파악 할 수 없다.
# Java script가 가진 이벤트를 파악하고 있어야함.
# ex ) 마우스 오버 : 마우스를 올려두었을 때, 특정 정보를 얻어올 수 있음.


from bs4 import BeautifulSoup

from selenium import webdriver #자바스크립트를 사용하는 동적 웹페이지를 크롤링 하기위한 웹브라우저 원격조작 라이브러리

from webdriver_manager.chrome import ChromeDriverManager #크롬브라우저 드라이버 매니저 호출

driver = webdriver.Chrome() #크롬 브라우저 웹드라이버 객체 생성


# https://www.coffeebeankorea.com/main/main.asp


driver.get("https://www.coffeebeankorea.com/store/store.asp") #웹드라이버 객체를 통해 원격조작 크롬 웹페이지창에 해당 주소 접속

driver.execute_script("storePop2(390)") #해당 스크립트를 실행


html = driver.page_source #자바스크립트 함수가 수행된 페이지의 소스코드 획득

bf1 = BeautifulSoup(html,'html.parser') #구조분석 객체 생성

print(bf1.prettify()) #소스코드 구조적 형태로 출력하여 확인 

store_name_h2 = bf1.select("div.store_txt > h2") 
store_name = store_name_h2[0].string
store_name


store_info = bf1.select("div.store_txt > table.store_table > tbody > tr > td")
store_info
store_address_list = list(store_info[2])
store_address_list
store_address = store_address_list[0]
store_address
store_phone = store_info[3].string


from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

wd=webdriver.Chrome()

from bs4 import BeautifulSoup

import urllib.request

import pandas as pd

import time



#[CODE 1]

def CoffeeBean_store(result):

    CoffeeBean_URL = "https://www.coffeebeankorea.com/store/store.asp"



    for i in range(50, 300): 

        wd.get(CoffeeBean_URL)

        time.sleep(1) #웹페이지에 연결할시간을 주기위해 딜레이 1초주기

        try:

            wd.execute_script("storePop2(%d)" %i)

            time.sleep(1) #스크립트를 실행할 시간을 주기위해 딜레이 주기

            html = wd.page_source

            bf1 = BeautifulSoup(html, 'html.parser')

            store_name_h2 = bf1.select("div.store_txt > h2")

            store_name = store_name_h2[0].string

            print(store_name)  #매장 이름 출력하기

            store_info = bf1.select("div.store_txt > table.store_table > tbody > tr > td")

            store_address_list = list(store_info[2])

            store_address = store_address_list[0]

            store_phone = store_info[3].string

            result.append([store_name]+[store_address]+[store_phone])

        except:

            continue 

    return



#[CODE 0]

def main():

    result = []

    print('CoffeeBean store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')

    CoffeeBean_store(result)  #[CODE 1]

    

    df = pd.DataFrame(result, columns=('store', 'address','phone'))

    df.to_csv('./crdata.csv', encoding='cp949', index=True)



if __name__ == '__main__':

     main()

