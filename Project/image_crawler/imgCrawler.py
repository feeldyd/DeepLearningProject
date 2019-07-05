import os
# 내장함수
from urllib.request import urlopen
# 명령행 파싱 모듈 argparse 모듈 사용
import argparse
# request => 요청하는거를 웹에 요청한 결과값을 얻어올수 있는 모듈
import requests as req
# 웹에 요청한 결과를 보내주는 모듈
from bs4 import BeautifulSoup
# 다이나믹 웹페이지 로드
from selenium import webdriver

import time

IMG_COUNT = 10
WEBDRIVER_PATH = "/Users/byunghun.lee/Downloads/chromedriver"

parser = argparse.ArgumentParser()
#argparse 모듈 에 ArgumentParse() 함수 사용하여 parser 생성

parser.add_argument("-name", "--searchName", required=True)
#  명령행 옵션을 지정하기 위해 사용합니다 명령행 옵션 인자는 -name으로 지정

args = parser.parse_args()
#parse에 add_argument()함수 사용해 args 인스턴스생성

searchName = args.searchName
# 명령행에서 받은 인자값을 searchName 에 값을 넘겨줌

def scrollDown(driver):
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def main():
    url_info = "https://www.google.co.kr/search?"

    #params에 딕션을 넣어줌
    params = {
        #명령행에서 받은 인자값을 people로 넣어줌
        "q": searchName,
        "tbm": "isch"
    }
    #url 요청 파싱값
    html_object = req.get(url_info, params) #html_object html source 값
    driver = webdriver.Chrome(webdriver)
    driver.get(html_object.url)

    # 버튼 나올때까지 스크롤 다운
    scrollDown(driver)
    # 버튼 클릭
    driver.find_element_by_id("smb").click()
    # 끝까지 스크롤 다운
    scrollDown(driver)

    if html_object.status_code == 200:
        #페이지 status_code 가 200 일때 2XX 는 성공을 이야기함
        bs_object = BeautifulSoup(driver.page_source, "html.parser")
        #인스턴스 생성
        img_data = bs_object.find_all("img")
        #인스턴스의 find_all 이라는 함수에 img 태그가 있으면 img_data에 넣어
        print(len(img_data))

        i = 1
        # 검색 결과의 전체 이미지를 받으려면 아래 주석 해제
        # IMG_COUNT = len(img_data)
        for img in img_data[3:IMG_COUNT]:
            #딕셔너리를 순서대로 넣어줌
            try:
                t = urlopen(img.attrs['src']).read()

                dirName = "./img/" + searchName + "/"

                if not os.path.exists(dirName):
                    os.mkdir(dirName)
                filename = dirName + searchName + "_" + ("%04d" % i) + '.jpg'

                with open(filename, "wb") as f:
                    f.write(t)
                    f.close()
                print("Img Save Success")
                i += 1
            except Exception as e:
                print(e)

if __name__=="__main__":
    main()
