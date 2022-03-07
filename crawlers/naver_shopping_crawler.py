from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup

import pandas as pd
import time
import re


def get_url(keyword):
    url = f'https://search.shopping.naver.com/search/all?query={keyword}'
    return url


def main(keyword):
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    url = get_url(keyword)
    driver.get(url)

    for i in range(3):
        driver.execute_script("window.scrollTo(0, 5000)")
        time.sleep(0.5) 

    info = get_item_info(driver)

    # driver.close()
    driver.quit()
    info.rename({'title':'상품명',
    'price':'가격(원)',
    'reviews':'누적 리뷰수'},axis=1,inplace=True)
    return info

def get_item_info(driver):
    item_info = []
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find_all('div',{'class':'basicList_inner__eY_mq'})


    #리스트 형태 item_info
    for item in item_list:
        item_title = item.find('div',{'class':'basicList_title__3P9Q7'}).text.strip()
        item_price = item.find('span',{'class':'price_num__2WUXn'}).text.strip()
        item_price = int(re.sub('[^0-9]', '',item_price))
        reviews = item.find('em',{'class':'basicList_num__1yXM9'}).text.strip()
        reviews = int(re.sub('[^0-9]', '',reviews))
        item_info.append([item_title,item_price,reviews])
    # print(item_info)
    #네이버 쇼핑 상품 리스트 중 앞 4개 광고 상품 제외
    item_info = item_info[4:] 
    item_info_df = pd.DataFrame(item_info, columns= ['title', 'price', 'reviews'])
    return item_info_df

if __name__ == '__main__':
    # keyword = input('검색할 상품 키워드를 입력하세요...')
    keyword = '밥솥'
    print(main(keyword))

