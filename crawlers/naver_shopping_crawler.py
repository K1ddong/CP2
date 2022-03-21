from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pandas as pd
import time
import re


def get_url(keyword):
    url = f'https://search.shopping.naver.com/search/all?query={keyword}'
    return url


def main(keyword):

    start_time = time.time()

    options = FirefoxOptions()
    options.add_argument("--headless")
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.http.pipelining", True)
    profile.set_preference("network.http.proxy.pipelining", True)
    profile.set_preference("network.http.pipelining.maxrequests", 8)
    profile.set_preference("content.notify.interval", 500000)
    profile.set_preference("content.notify.ontimer", True)
    profile.set_preference("content.switch.threshold", 250000)
    profile.set_preference("browser.cache.memory.capacity", 65536) # Increase the cache capacity.
    profile.set_preference("browser.startup.homepage", "about:blank")
    profile.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
    profile.set_preference("loop.enabled", False)
    profile.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
    profile.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
    profile.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
    profile.set_preference("permissions.default.image", 2) # Image load disabled again

    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))


    driver = webdriver.Firefox(
        firefox_binary=binary,
        firefox_options=profile,
        executable_path=os.environ.get('GECKODRIVER_PATH'),
        options=options)

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

    end_time = time.time()
    print('네이버 데이터 수집 걸린 시간 :',end_time-start_time)
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

