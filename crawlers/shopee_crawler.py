from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import pandas as pd
import time
import re


def get_url(keyword):
    url = f'https://shopee.com.my/search?keyword={keyword}&sortBy=sales' #페이지 필요할 경우 &page={}
    return url

def solds_unifier(solds):
    amount = solds.split(' ')[0]
    if amount[-1] == 'k':
        amount = float(amount[:-1]) * 1000
    elif amount[-1] == 'm':
        amount = float(amount[:-1]) * 1000000
    else:
        return int(amount)
    return int(amount)

def get_item_info(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find_all('div',{'class':'col-xs-2-4 shopee-search-item-result__item'})

    item_info = []

    

    for item in item_list:
        item_title = item.find('div',{'class':'_10Wbs- _2STCsK _3IqNCf'}).text.strip()
        item_price = item.find('span',{'class':'_3c5u7X'}).text.strip()
        item_price = float(re.sub('[^0-9.]', '',item_price))
        sold = item.find('div',{'class':'_1uq9fs'}).text.strip()
        try:
            solds = solds_unifier(sold)
        except IndexError:
            solds = 999999
        # reviews = int(re.sub('[^0-9]', '',reviews))
        item_info.append([item_title,item_price,solds])
    
    #쇼피 첫 5개 및 마지막 5개 광고 상품 제외
    item_info = item_info[5:55]
    item_info_df = pd.DataFrame(item_info, columns=['title','price','solds'])
    return item_info_df

def main(keyword):
    options = FirefoxOptions()
    options.add_argument("--headless")

    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))


    driver = webdriver.Firefox(
        firefox_binary=binary,
        executable_path=os.environ.get('GECKODRIVER_PATH'),
        options=options)

    url = get_url(keyword)
    driver.get(url)

    # 페이지 스크롤
    SCROLL_PAUSE_TIME = 0.5
    y = 100
    # 현재 페이지 위치
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # y만큼 스크롤 다운
        driver.execute_script("window.scrollTo(0, "+str(y)+")")
        # 페이지 로딩
        time.sleep(SCROLL_PAUSE_TIME)
        # 현재 페이지 위치
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button').click()
            except:
                break
        y += 500
        last_height = new_height

    info = get_item_info(driver)

    # driver.close()
    driver.quit()
    info.rename({'title':'상품명',
    'price':'가격(RM)',
    'solds':'판매량(월 평균)'},axis=1,inplace=True)
    return info


if __name__ == '__main__':
    # keyword = input('검색할 상품 키워드를 입력하세요...')
    keyword = 'rice cooker'
    main(keyword)

