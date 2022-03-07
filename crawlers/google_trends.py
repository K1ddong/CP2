from distutils.log import info
from pytrends.request import TrendReq



class GoogleTrend:
    def __init__(self,keyword):
        self.keyword = keyword
        self.trendshow = TrendReq(hl='en-US', tz=360, timeout=(3,12), 
                                retries=1, backoff_factor=0.1)
        self.trendshow.build_payload(keyword, cat=0, timeframe='today 12-m', geo='MY')
        self.related_keywords = self.trendshow.related_queries()

    def rising(self):
        info = self.related_keywords[self.keyword[0]]['rising']
        info.rename({'query':'연관 검색어',
        'value':'가중치'},axis=1,inplace=True)
        return info

    def top(self):
        info = self.related_keywords[self.keyword[0]]['top']
        info.rename({'query':'연관 검색어',
        'value':'가중치'},axis=1,inplace=True)
        return info

    def trends(self):
        keyword_search_trend = self.trendshow.interest_over_time()
        keyword_search_trend.reset_index(inplace=True)
        return keyword_search_trend[['date',self.keyword[0]]]

# def main(keyword):
#     #영어로 검색, 에러 관련 파라미터 timeout, retries, backoff_factor
#     trendshow = TrendReq(hl='en-US', tz=360, timeout=(3,12), 
#                                 retries=1, backoff_factor=0.1)

#     #오늘부터 12달 전까지의 기록, today 3-m => 3달 전, geo = 지역
#     trendshow.build_payload(keyword, cat=0, timeframe='today 12-m', geo='MY')

#     #관련 검색어
#     related_keywords = trendshow.related_queries()
#     rising_related_keywords = related_keywords[keyword[0]]['rising']
#     top_related_keywords = related_keywords[keyword[0]]['top']

#     #기간별 검색 트렌드
#     keyword_search_trend = trendshow.interest_over_time()
#     keyword_search_trend.reset_index(inplace=True)
#     keyword_search_trend = keyword_search_trend[['date',keyword[0]]]
#     return rising_related_keywords,top_related_keywords,keyword_search_trend


if __name__ == '__main__':
    keyword = ['rice cooker']
    # main(keyword)
    test = GoogleTrend(keyword)
    print(test.rising())
