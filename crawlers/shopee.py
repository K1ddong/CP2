from os import link
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import re


#동적웹 컨트롤
def page_control(driver):
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
                # driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button').click()
                driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button').click()
            except:
                break
        y += 500
        last_height = new_height

        
#검색 상품 url
def get_url(keyword):
    url = 'https://shopee.com.my/'
    top_sales_url = f'{url}search?keyword={keyword}&sortBy=sales' #페이지 필요할 경우 &page={}
    return url, top_sales_url


#판매량 전처리
def solds_unifier(solds):
    amount = solds.split(' ')[0]
    if amount[-1] == 'k':
        amount = float(amount[:-1]) * 1000
    elif amount[-1] == 'm':
        amount = float(amount[:-1]) * 1000000
    else:
        return int(amount)
    return int(amount)


#상품 리스트 가져오기
def get_item_list(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find_all('div',{'class':'col-xs-2-4 shopee-search-item-result__item'})
    return item_list


#상품 정보 가져오기
def get_item_info(item_list):
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


def get_item_link(item_list, url):
    item_link = []
    for item in item_list:
        link = item.find('a').get('href')
        item_link.append(url + link)
    return item_link


def get_item_details(item_link):
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(item_link)
    time.sleep(1)
    driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button').click()
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    likes = soup.findAll('div',{'class':'Rs4O3p'})[1].text.split(' ')[1][1:-1]
    ratings_star = soup.findAll('div',{'class':'_3uBhVI'})[0].text
    ratings_counts = soup.findAll('div',{'class':'_3uBhVI'})[1].text
    total_solds = soup.findAll('div',{'class':'_3b2Btx'})[0].text
    driver.quit()
    return likes, ratings_star, ratings_counts, total_solds


def main(keyword):
    start = time.time()
    options = FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    url, top_sales_url = get_url(keyword)
    driver.get(top_sales_url)

    page_control(driver)

    item_list = get_item_list(driver)
    item_link = get_item_link(item_list, url)
    info = get_item_info(item_list)

    details = []
    for link in item_link:
        print('시작')
        likes, ratings_star, ratings_counts, total_solds = get_item_details(link)
        details.append([likes, ratings_star, ratings_counts, total_solds])
        print(details)
        print('완료')

    driver.quit()
    info.rename({'title':'상품명',
    'price':'가격(RM)',
    'solds':'판매량(월 평균)'},axis=1,inplace=True)
    # return info
    print("작업 시간 :", time.time() - start)
    return details




if __name__ == '__main__':
    # keyword = input('검색할 상품 키워드를 입력하세요...')
    keyword = 'rice cooker'
    print(main(keyword))

