from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import pandas as pd
import time
import re


def shopee_get_url(keyword_en):
    url = f'https://shopee.com.my/search?keyword={keyword_en}&sortBy=sales' #페이지 필요할 경우 &page={}
    return url

def shopee_solds_unifier(solds):
    amount = solds.split(' ')[0]
    if amount[-1] == 'k':
        amount = float(amount[:-1]) * 1000
    elif amount[-1] == 'm':
        amount = float(amount[:-1]) * 1000000
    else:
        return int(amount)
    return int(amount)

def shopee_get_item_info(driver):
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
            solds = shopee_solds_unifier(sold)
        except IndexError:
            solds = 0
        # reviews = int(re.sub('[^0-9]', '',reviews))
        item_info.append([item_title,item_price,solds])
    
    #쇼피 첫 5개 및 마지막 5개 광고 상품 제외
    item_info = item_info[5:55]
    item_info_df = pd.DataFrame(item_info, columns=['title','price','solds'])
    return item_info_df










def main(keyword,keyword_en):

    start_time = time.time()

    options = FirefoxOptions()
    # options.add_argument("--headless")

    profile = webdriver.FirefoxProfile()
    profile.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
    profile.set_preference("loop.enabled", False)
    profile.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
    profile.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
    profile.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
    profile.set_preference("permissions.default.image", 2) # Image load disabled again
    profile.set_preference("webdriver.load.strategy", "unstable")
    profile.update_preferences()


    try:
        binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
    except:
        pass
    try:
        driver = webdriver.Firefox(
            firefox_binary=binary,
            firefox_profile=profile,
            executable_path=os.environ.get('GECKODRIVER_PATH'),
            options=options)
    except:
        driver = webdriver.Firefox(
            firefox_profile=profile,
            options=options)

    shopee_url = shopee_get_url(keyword_en)
    driver.get(shopee_url)

    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "shopee-search-item-result")))

    # 페이지 스크롤
    SCROLL_PAUSE_TIME = 0.3
    y = 100
    # 현재 페이지 위치
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(100):
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

    shopee_info = shopee_get_item_info(driver)
    print('쇼피 데이터 요청 완료')

    #네이버

    def naver_get_url(keyword):
        url = f'https://search.shopping.naver.com/search/all?query={keyword}'
        return url

    def naver_get_item_info(driver):
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


    naver_url = naver_get_url(keyword)

    driver.get(naver_url)

    for i in range(3):
        driver.execute_script("window.scrollTo(0, 5000)")
        time.sleep(0.5) 

    naver_info = naver_get_item_info(driver)
    print('네이버 데이터 요청 완료')

    driver.quit()

    #전처리
    shopee_info.rename({'title':'상품명',
    'price':'가격(RM)',
    'solds':'판매량(월 평균)'},axis=1,inplace=True)
    naver_info.rename({'title':'상품명',
    'price':'가격(원)',
    'reviews':'누적 리뷰수'},axis=1,inplace=True)

    end_time = time.time()
    print('데이터 수집 걸린 시간 : ', end_time-start_time)
   
   
    return shopee_info, naver_info


if __name__ == '__main__':
    # keyword = input('검색할 상품 키워드를 입력하세요...')
    keyword = '밥솥'
    keyword_en = 'rice cooker'
    print(main(keyword,keyword_en))