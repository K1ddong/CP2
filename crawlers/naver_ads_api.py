import hashlib
import hmac
import base64
import time
import requests
import pandas as pd
# from config import get_secret


class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())


def get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID):
    timestamp = str(round(time.time() * 1000))
    signature = Signature().generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 
            'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 
            'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


def main(keyword,API_KEY, SECRET_KEY, CUSTOMER_ID):
    uri = '/keywordstool'
    method = 'GET'
    BASE_URL = 'https://api.naver.com'
    r = requests.get(BASE_URL + uri+'?hintKeywords={}&showDetail=1'.format(keyword.replace(' ','')),
                    headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    #전체 키워드 관련 자료
    keyword_data = list(filter(lambda x:keyword.split(' ')[0] in x['relKeyword'], r.json()['keywordList']))
    #필요한 것
    ##키워드 검색량
    # print('키워드 검색량', keyword_data[0])
    keyword_search_volume = pd.DataFrame(keyword_data[0],index=[0])
    ##검색량 기준 연관키워드 검색량
    volume_by_mobile = [x for x in keyword_data if type(x['monthlyMobileQcCnt']) == int ]
    top_10_by_volume = sorted(volume_by_mobile, key = lambda x: x['monthlyMobileQcCnt'], reverse=True)
    # print('연관 키워드',top_10_by_volume[:10])
    top_10_related_keywords = pd.DataFrame.from_dict(top_10_by_volume[:10])
    #모바일/PC 검색량 비율
    #모바일 ctr, pc ctr
    keyword_search_volume.rename({'compIdx':'경쟁정도',
           'monthlyAveMobileClkCnt':'월평균클릭수_모바일',
           'monthlyAveMobileCtr':'월평균클릭률_모바일',
           'monthlyAvePcClkCnt':'월평균클릭수_PC',
           'monthlyAvePcCtr':'월평균클릭률_PC', 
           'monthlyMobileQcCnt':'월간검색수_모바일',
           'monthlyPcQcCnt': '월간검색수_PC',
           'plAvgDepth':'월평균노출광고수', 
           'relKeyword':'연관키워드'},axis=1,inplace=True)
    top_10_related_keywords.rename({'compIdx':'경쟁정도',
    'monthlyAveMobileClkCnt':'월평균클릭수_모바일',
    'monthlyAveMobileCtr':'월평균클릭률_모바일',
    'monthlyAvePcClkCnt':'월평균클릭수_PC',
    'monthlyAvePcCtr':'월평균클릭률_PC', 
    'monthlyMobileQcCnt':'월간검색수_모바일',
    'monthlyPcQcCnt': '월간검색수_PC',
    'plAvgDepth':'월평균노출광고수', 
    'relKeyword':'연관키워드'},axis=1,inplace=True)
    keyword_search_volume.drop(['경쟁정도','월평균노출광고수'], axis=1, inplace=True)
    top_10_related_keywords.drop(['경쟁정도','월평균노출광고수'], axis=1, inplace=True)
    return keyword_search_volume,top_10_related_keywords
    

if __name__ == '__main__':
    # API_KEY = get_secret("API_KEY")
    # SECRET_KEY = get_secret("SECRET_KEY")
    # CUSTOMER_ID = get_secret("CUSTOMER_ID")
    keyword = '강아지 진드기 스프레이'
    print(main(keyword,API_KEY, SECRET_KEY, CUSTOMER_ID))
