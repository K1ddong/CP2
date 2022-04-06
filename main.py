from crypt import methods
from config_for_main import get_secret
from crawlers import shopee_crawler, naver_trends,naver_shopping_crawler,naver_ads_api,google_trends

import googletrans
import os

# #네이버 데이터랩 api
try:
    NAVER_API_ID = get_secret("NAVER_API_ID")
except:
    NAVER_API_ID = os.getenv("NAVER_API_ID")

try:
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")
except:
    NAVER_API_SECRET = os.getenv("NAVER_API_SECRET")

# #네이버 검색광고 api
try:
    API_KEY = get_secret("API_KEY")
except:
    API_KEY = os.getenv("API_KEY")

try:
    SECRET_KEY = get_secret("SECRET_KEY")
except:
    SECRET_KEY = os.getenv("SECRET_KEY")
try:
    CUSTOMER_ID = get_secret("CUSTOMER_ID")  
except:
    CUSTOMER_ID = os.getenv("CUSTOMER_ID")

'''
------------------------ 크롤링 --------------------------------
'''
'''
------------------------ 웹앱 --------------------------------
'''

from dash import html,dcc,dash_table as dt,Dash
from flask import Flask, redirect,render_template,request, url_for

# flask server 
application = Flask(__name__) 

# dash app with flask server 
dash_app1 = Dash(__name__, server=application, url_base_pathname='/dashapp1/')

dash_app1.layout = html.Div(
    # Header Message
    children=[
        html.H1(children="오류가 발생했습니다.",),
        html.P(
            children="다시 검색해주세요",
        )
    ]
)

# flask app
@application.route('/')
def index():
    return render_template("home.html")

@application.route('/search',methods=['POST','GET'])
def home():
    if request.method == 'GET':
        keyword = request.args.get("keyword")
    else:
        keyword = request.form['keyword']
    #키워드 번역
    translator = googletrans.Translator()
    keyword_en = str(translator.translate(keyword, src='ko', dest='en').text)

    #구글 검색 트렌드
    google = google_trends.GoogleTrend([keyword_en])
    ## 떠오르는 연관 키워드
    rising_related_keywords = google.rising()
    ## 상위 연관 키워드
    top_related_keywords = google.top()
    ## 키워드 검색 추이
    google_trend = google.trends()
    ### 월별로 축소
    google_trend = google_trend.reset_index().groupby(google_trend.reset_index()['date'].dt.to_period('M')).mean()
    google_trend.reset_index(inplace=True)

    ### 수치 정규화 (최대치 기준으로)
    df = google_trend[keyword_en]
    google_trend[keyword_en] = df/df.max() * 100 

    #쇼피 키워드 상품 정보
    # shopee_item_info = shopee_crawler.main(keyword_en)

    #네이버 키워드 상품 검색량, 연관 키워드 검색량
    keyword_search_volume,top_10_related_keywords= naver_ads_api.main(keyword,API_KEY, SECRET_KEY, CUSTOMER_ID)

    #네이버 키워드 상품 정보
    naver_item_info = naver_shopping_crawler.main(keyword)

    #네이버 키워드 검색 추이
    naver_trend = naver_trends.main(keyword,NAVER_API_ID, NAVER_API_SECRET)


    #네이버 구글 검색 추이 통합
    naver_trend[keyword_en] = google_trend[keyword_en]

    dash_app1.layout = html.Div(
    # Header Message
    children=[
        html.Div([html.H1(children=f'\'{keyword}\' 키워드 분석 결과')],style={
             'text-align':'center'}),
        html.Div([
        html.H3(
            children=f"네이버 \'{keyword}\' 키워드 검색량",
        ),
        dt.DataTable(
            keyword_search_volume.to_dict('records'),
            [{"name":i, "id":i} for i in keyword_search_volume.columns],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'},
            style_table={
                'maxHeight': '50ex',
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            # style cell
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '45px',
                'padding': '2px 22px',
                'whiteSpace': 'inherit',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            # style header
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'azure',
            },
            # style filter
            # style data
            style_data_conditional=[
                {
                    # stripped rows
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }],
        ),
        html.H3(
            children=f"네이버 \'{keyword}\' 키워드 연관 검색어 및 검색량",
        ),
        dt.DataTable(
            top_10_related_keywords.to_dict('records'),
            [{"name":i, "id":i} for i in top_10_related_keywords.columns],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'center'},
            style_table={
                'maxHeight': '50ex',
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            # style cell
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '45px',
                'padding': '2px 22px',
                'whiteSpace': 'inherit',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            # style header
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'azure',
            },
            # style filter
            # style data
            style_data_conditional=[
                {
                    # stripped rows
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }],
        ),
        ],style={'margin-bottom':'300px',
             'text-align':'center',
             'backgroundColor':"#dbe4f0 ",
             'border':"2px solid LightSteelBlue",
             'width':"70%",
             'display':"inline-block",
             'margin':"1em",
             'margin-left': '15%', 
             'margin-right': '15%'}),
        html.Div([
        html.H3(
            children=f"네이버 쇼핑 \'{keyword}\' 상품 상위 TOP30",
        ),
        dt.DataTable(
            naver_item_info.to_dict('records'),
            [{"name":i, "id":i} for i in naver_item_info.columns],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'center'},
            style_table={
                'maxHeight': '50ex',
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            # style cell
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '45px',
                'padding': '2px 22px',
                'whiteSpace': 'inherit',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            # style header
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'azure',
            },
            # style filter
            # style data
            style_data_conditional=[
                {
                    # stripped rows
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }],
        ),
        html.H3(
            children=f"쇼피 말레이시아 \'{keyword_en}\' 상품 상위 TOP50",
        ),
        dt.DataTable(
            naver_item_info.to_dict('records'),
            [{"name":i, "id":i} for i in naver_item_info.columns],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'center'},
            style_table={
                'maxHeight': '50ex',
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            # style cell
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '45px',
                'padding': '2px 22px',
                'whiteSpace': 'inherit',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            # style header
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'azure',
            },
            # style filter
            # style data
            style_data_conditional=[
                {
                    # stripped rows
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }],
        ),
        ],style={'margin-bottom':'300px',
             'text-align':'center',
             'backgroundColor':"#dbe4f0 ",
             'border':"2px solid LightSteelBlue",
             'width':"70%",
             'display':"inline-block",
             'margin':"1em",
             'margin-left': '15%', 
             'margin-right': '15%'}),
        html.Div([
        html.H3(
            children=f"네이버/구글(말레이시아) \'{keyword}\'/\'{keyword_en}\' 키워드 검색 추이"),
        # 그래프		
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": naver_trend["날짜"],
                        "y": naver_trend[keyword],
                        "type": "lines", "name":"naver"
                    },
                    {    
                        "x": naver_trend["날짜"],
                        "y": naver_trend[keyword_en],
                        "type": "lines", "name":"google"
                    },
                ],
                "layout": {"title":f"네이버/구글(말레이시아) \'{keyword}\'/\'{keyword_en}\' 키워드 검색 추이"},
            },
        ),
        ],style={'margin-bottom':'300px',
             'text-align':'center',
             'backgroundColor':"#dbe4f0 ",
             'border':"2px solid LightSteelBlue",
             'width':"70%",
             'display':"inline-block",
             'margin':"1em",
             'margin-left': '15%', 
             'margin-right': '15%'}),
        html.Div([
        html.H3(
            children=f"구글(말레이시아) \'{keyword_en}\'키워드의 떠오르는 연관 키워드",
        ),
        dt.DataTable(
            rising_related_keywords.to_dict('records'),
            [{"name":i, "id":i} for i in rising_related_keywords.columns],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'center'},
            style_table={
                'maxHeight': '50ex',
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            # style cell
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '45px',
                'padding': '2px 22px',
                'whiteSpace': 'inherit',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            # style header
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'azure',
            },
            # style filter
            # style data
            style_data_conditional=[
                {
                    # stripped rows
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }]
            # style filter
            # style data,
        ),
        html.H3(
            children=f"구글(말레이시아) \'{keyword_en}\'키워드의 상위 연관 키워드",
        ),
        dt.DataTable(
            top_related_keywords.to_dict('records'),
            [{"name":i, "id":i} for i in top_related_keywords.columns],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'center'},
            style_table={
                'maxHeight': '50ex',
                'overflowY': 'scroll',
                'width': '100%',
                'minWidth': '100%',
            },
            # style cell
            style_cell={
                'fontFamily': 'Open Sans',
                'textAlign': 'center',
                'height': '45px',
                'padding': '2px 22px',
                'whiteSpace': 'inherit',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            # style header
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'azure',
            },
            # style filter
            # style data
            style_data_conditional=[
                {
                    # stripped rows
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }]
        ),],style={'margin-bottom':'300px',
             'text-align':'center',
             'backgroundColor':"#dbe4f0 ",
             'border':"2px solid LightSteelBlue",
             'width':"70%",
             'display':"inline-block",
             'margin':"1em",
             'margin-left': '15%', 
             'margin-right': '15%'})
    ],
)

    return redirect('/dashapp1')





if __name__ == '__main__':
    # app.run_server(debug=True)
    application.debug = True
    application.run()    