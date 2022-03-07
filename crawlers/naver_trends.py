from PyNaver import Datalab
from datetime import datetime
from dateutil.relativedelta import relativedelta
# from config import get_secret



def main(keyword,NAVER_API_ID, NAVER_API_SECRET):
    
    # 네이버 데이터랩 API 세션 정의
    DL = Datalab(NAVER_API_ID, NAVER_API_SECRET)

    # 요청 파라미터 설정
    endDate = datetime.now().strftime("%Y-%m-%d")
    startDate = (datetime.now()-relativedelta(years=1)).strftime("%Y-%m-%d")
    timeUnit = 'month'
    device = ''
    ages = []
    gender = ''

    # 검색어 그룹 세트 등록하기
    keyword = {'keyword': {'groupName':keyword, 'keywords':[keyword]}}
    DL.add_keyword_groups(keyword['keyword'])

    # 결과 데이터를 DataFrame으로 조회하기
    df = DL.get_data(startDate, endDate, timeUnit, device, ages, gender)
    return df


if __name__ == '__main__':
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")
    keyword = '밥솥'
    main(keyword,NAVER_API_ID, NAVER_API_SECRET)