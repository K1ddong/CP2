# import hashlib
# import hmac
# import base64
# import time
# import requests
# import pandas as pd
# from config import get_secret


# class Signature:

#     @staticmethod
#     def generate(timestamp, method, uri, secret_key):
#         message = "{}.{}.{}".format(timestamp, method, uri)
#         hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

#         hash.hexdigest()
#         return base64.b64encode(hash.digest())


# def get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID):
#     timestamp = str(round(time.time() * 1000))
#     signature = Signature().generate(timestamp, method, uri, SECRET_KEY)
#     return {'Content-Type': 'application/json; charset=UTF-8', 
#             'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 
#             'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


# def main(keyword,API_KEY, SECRET_KEY, CUSTOMER_ID):
#     uri = '/keywordstool'
#     method = 'GET'
#     BASE_URL = 'https://api.naver.com'
#     r = requests.get(BASE_URL + uri+'?hintKeywords={}&showDetail=1'.format(keyword),
#                     headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

#     #전체 키워드 관련 자료
#     print(r.json())
#     keyword_data = list(filter(lambda x:keyword in x['relKeyword'], r.json()['keywordList']))
#     #필요한 것
#     ##키워드 검색량
#     # print('키워드 검색량', keyword_data[0])
#     keyword_search_volume = pd.DataFrame(keyword_data[0],index=[0])
#     ##검색량 기준 연관키워드 검색량
#     volume_by_mobile = [x for x in keyword_data if type(x['monthlyMobileQcCnt']) == int ]
#     top_10_by_volume = sorted(volume_by_mobile, key = lambda x: x['monthlyMobileQcCnt'], reverse=True)
#     # print('연관 키워드',top_10_by_volume[:10])
#     top_10_related_keywords = pd.DataFrame.from_dict(top_10_by_volume[:10])
#     #모바일/PC 검색량 비율
#     #모바일 ctr, pc ctr
#     keyword_search_volume.rename({'compIdx':'경쟁정도',
#            'monthlyAveMobileClkCnt':'월평균클릭수_모바일',
#            'monthlyAveMobileCtr':'월평균클릭률_모바일',
#            'monthlyAvePcClkCnt':'월평균클릭수_PC',
#            'monthlyAvePcCtr':'월평균클릭률_PC', 
#            'monthlyMobileQcCnt':'월간검색수_모바일',
#            'monthlyPcQcCnt': '월간검색수_PC',
#            'plAvgDepth':'월평균노출광고수', 
#            'relKeyword':'연관키워드'},axis=1,inplace=True)
#     top_10_related_keywords.rename({'compIdx':'경쟁정도',
#     'monthlyAveMobileClkCnt':'월평균클릭수_모바일',
#     'monthlyAveMobileCtr':'월평균클릭률_모바일',
#     'monthlyAvePcClkCnt':'월평균클릭수_PC',
#     'monthlyAvePcCtr':'월평균클릭률_PC', 
#     'monthlyMobileQcCnt':'월간검색수_모바일',
#     'monthlyPcQcCnt': '월간검색수_PC',
#     'plAvgDepth':'월평균노출광고수', 
#     'relKeyword':'연관키워드'},axis=1,inplace=True)
#     keyword_search_volume.drop(['경쟁정도','월평균노출광고수'], axis=1, inplace=True)
#     top_10_related_keywords.drop(['경쟁정도','월평균노출광고수'], axis=1, inplace=True)
#     return keyword_search_volume,top_10_related_keywords
    

# if __name__ == '__main__':
#     # API_KEY = get_secret("API_KEY")
#     # SECRET_KEY = get_secret("SECRET_KEY")
#     # CUSTOMER_ID = get_secret("CUSTOMER_ID")
#     API_KEY = '0100000000afa69f72b3c8bc4aafb5e6187150da5534d7783b03358f354e673aac259be185'
#     SECRET_KEY = 'AQAAAAASBRfCcUPFPghzJx1XVPKGRpnHOHymkhaF0G3GRS6H3Q=='
#     CUSTOMER_ID = '2129113'
#     keyword = '밥솥'
#     main(keyword,API_KEY, SECRET_KEY, CUSTOMER_ID)

import hashlib
import hmac
import base64
import time
import random
import requests
import json
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


def get_data(keyword):
    uri = '/keywordstool'
    method = 'GET'
    r = requests.get(BASE_URL + uri+'?hintKeywords={}&showDetail=1'.format(keyword),
                    headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    #전체 키워드 관련 자료
    keyword_data = list(filter(lambda x:keyword in x['relKeyword'], r.json()['keywordList']))
    keyword_data = [x for x in keyword_data if type(x['monthlyMobileQcCnt']) == int ]
    #필요한 것
    ##키워드 검색량
    print('키워드 검색량', keyword_data[0])
    ##검색량 기준 연관키워드 검색량
    top_10 = sorted(keyword_data, key = lambda x: x['monthlyMobileQcCnt'], reverse=True)[:10]
    print('연관 키워드',top_10[:10])
    #모바일/PC 검색량 비율

    #모바일 ctr, pc ctr

    return keyword_data,top_10

if __name__ == '__main__':
    BASE_URL = 'https://api.naver.com'
    # API_KEY = get_secret("API_KEY")
    # SECRET_KEY = get_secret("SECRET_KEY")
    # CUSTOMER_ID = get_secret("CUSTOMER_ID")
    API_KEY = '0100000000afa69f72b3c8bc4aafb5e6187150da5534d7783b03358f354e673aac259be185'
    SECRET_KEY = 'AQAAAAASBRfCcUPFPghzJx1XVPKGRpnHOHymkhaF0G3GRS6H3Q=='
    CUSTOMER_ID = '2129113'
    keyword = '밥솥'
    data,top_10 = get_data(keyword) 
