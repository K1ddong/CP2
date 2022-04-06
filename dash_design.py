from symtable import Symbol
from click import style
import pandas as pd

from crawlers import google_trends


google_rising = pd.read_csv('google_rising.csv')
google_top = pd.read_csv('google_top.csv')
shopee_item_info = pd.read_csv('shopee_item_info.csv')
keyword_search_volume = pd.read_csv('keyword_search_volume.csv')
top_10_related_keywords = pd.read_csv('top_10_related_keywords.csv')
naver_item_info = pd.read_csv('naver_item_info.csv')
naver_trend = pd.read_csv('naver_trend.csv')


import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, Dash
import plotly.graph_objects as go
import plotly.express as px


keyword = '밥솥'

#-------------------------전처리-------------------------

####---------함수------------###
def brand_from_title(title):
    brand = title.split(' ')[0]
    return brand

def strip_keyword(title):
    keyword = 'rice cooker'
    return title.replace(keyword, '').strip()



####---------네이버-----------###

naver_item_info['브랜드'] = naver_item_info['상품명'].apply(brand_from_title)
naver_avg_price = round(naver_item_info['가격(원)'].mean())
card_naver_avg_price = [
    dbc.CardHeader("네이버 top31 평균 가격"),
    dbc.CardBody([html.H3(f"{naver_avg_price} 원")])  
    ]

naver_min_price = round(naver_item_info['가격(원)'].min())
card_naver_min_price = [
    dbc.CardHeader("네이버 top31 최저 가격"),
    dbc.CardBody([html.H3(f"{naver_min_price} 원")])  
    ]

naver_max_price = round(naver_item_info['가격(원)'].max())
card_naver_max_price = [
    dbc.CardHeader("네이버 top31 최고 가격"),
    dbc.CardBody([html.H3(f"{naver_max_price} 원")])  
    ]



###-----------시각화 요소---------###
card_keyword = [
    dbc.CardHeader("검색 키워드"),
    dbc.CardBody([html.H3(f"{keyword}")])  
    ]
card_search_volume = [
    dbc.CardHeader("월간 검색량 (PC / 모바일)"),
    dbc.CardBody([html.H3(f"{keyword_search_volume.iloc[0][1]} / {keyword_search_volume.iloc[0][2]}")])  
    ]
card_click_volume = [
    dbc.CardHeader("클릭수 (PC / 모바일)"),
    dbc.CardBody([html.H3(f"{int(keyword_search_volume.iloc[0][3])} ({keyword_search_volume.iloc[0][5]}%) / {int(keyword_search_volume.iloc[0][4])} ({keyword_search_volume.iloc[0][6]}%)")])  
    ]

###검색 추이 그래프
graph_line_naver_search_trend = px.line(naver_trend, x = '날짜', 
                                                     y = keyword, 
                                                     title = '키워드 검색 추이')



###top 연관 검색어
graph_bar_naver_related_top = px.bar(top_10_related_keywords, x = '연관키워드',
                                                              y = ['월간검색수_모바일','월간검색수_PC'],
                                                              barmode='group',
                                                              title = 'top 10 연관 키워드 검색량')

naver_color = dict(zip(naver_item_info["브랜드"].unique(), px.colors.qualitative.G10))

graph_scatter_naver_item_price = px.scatter(naver_item_info, 
                                            x='가격(원)', 
                                            y='누적 리뷰수', 
                                            hover_name='상품명', 
                                            color='브랜드',
                                            color_discrete_map=naver_color, 
                                            symbol='브랜드',
                                            title='가격 분포').update_traces(marker_size=10)
graph_scatter_naver_item_price.update_layout(showlegend=False)

graph_pie_naver_brand_dist = px.pie(naver_item_info['브랜드'].value_counts(),
                                    values = naver_item_info['브랜드'].value_counts().values,
                                    names = naver_item_info['브랜드'].value_counts().index,
                                    color = naver_item_info['브랜드'].value_counts().index,
                                    color_discrete_map=naver_color,
                                    title = '브랜드 분포')

##----------------------------쇼피-----------------------------
###쇼피 최소, 평균, 최대 가격

shopee_item_info['브랜드'] = shopee_item_info['상품명'].apply(brand_from_title)

shopee_avg_price = round(shopee_item_info['가격(RM)'].mean())
card_shopee_avg_price = [
    dbc.CardHeader("top50 평균 가격"),
    dbc.CardBody([html.H3(f"{shopee_avg_price} RM")])  
    ]

shopee_min_price = round(shopee_item_info['가격(RM)'].min())
card_shopee_min_price = [
    dbc.CardHeader("top50 최저 가격"),
    dbc.CardBody([html.H3(f"{shopee_min_price} RM")])  
    ]

shopee_max_price = round(shopee_item_info['가격(RM)'].max())
card_shopee_max_price = [
    dbc.CardHeader("top50 최고 가격"),
    dbc.CardBody([html.H3(f"{shopee_max_price} RM")])  
    ]
###쇼피 top50 기준 월 판매 시장 규모
shopee_item_info['월판매액'] = shopee_item_info['가격(RM)'] * shopee_item_info['판매량(월 평균)']
shopee_top50_monthly_market_size = int(shopee_item_info['월판매액'].sum())
card_shopee_monthly_market_size = [
    dbc.CardHeader("top50 상품 월 기준 시장규모"),
    dbc.CardBody([html.H3(f"{shopee_top50_monthly_market_size} RM")])
]

###쇼피 그래프 (가격대 스캐터, 브랜드 분포 파이)
mask = shopee_item_info['브랜드'].map(shopee_item_info['브랜드'].value_counts()) == 1
shopee_item_info['브랜드'] =  shopee_item_info['브랜드'].mask(mask, 'other')


shopee_color = dict(zip(shopee_item_info["브랜드"].unique(), px.colors.qualitative.G10))

graph_scatter_shopee_item_price = px.scatter(shopee_item_info, 
                                            x='가격(RM)', 
                                            y='판매량(월 평균)', 
                                            hover_name='상품명', 
                                            color='브랜드',
                                            color_discrete_map=shopee_color, 
                                            symbol='브랜드',
                                            title='가격 분포').update_traces(marker_size=10)
graph_scatter_shopee_item_price.update_layout(showlegend=False)

graph_pie_shopee_brand_dist = px.pie(shopee_item_info['브랜드'].value_counts(),
                                    values = shopee_item_info['브랜드'].value_counts().values,
                                    names = shopee_item_info['브랜드'].value_counts().index,
                                    color = shopee_item_info['브랜드'].value_counts().index,
                                    color_discrete_map=shopee_color,
                                    title = '브랜드 분포')

##-----------------------구글 키워드------------------------------------
google_top10 = google_top.sort_values(by='가중치',ascending=False).head(10)

###검색 추이 그래프
graph_line_google_search_trend = px.line(naver_trend, x = '날짜', 
                                                      y = 'Rice cooker', 
                                                      title = '키워드 검색 추이')



###top 연관 검색어
graph_bar_google_related_top = px.bar(google_top10, x = '연관 검색어',
                                                    y = '가중치',
                                                    title = 'top 10 연관 키워드 검색량')

google_keyword_related_words = google_top10['연관 검색어'].apply(strip_keyword).value_counts()

graph_pie_google_keyword_dist = px.pie(google_keyword_related_words,
                                    values = google_keyword_related_words.values,
                                    names = google_keyword_related_words.index,
                                    color = google_keyword_related_words.index,
                                    title = '연관 키워드 분포')
graph_pie_google_keyword_dist.update_traces(hoverinfo='label+percent', textinfo='value')


###rising 연관 검색어
graph_bar_google_related_rising = px.bar(google_rising, x = '연관 검색어',
                                                        y = '가중치',
                                                        title = '연관 검색어 검색 빈도')

graph_table_google_related_top = go.Figure(data=[go.Table(
    header=dict(values=list(google_top10.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[google_top10['연관 검색어'], google_top10['가중치']],
               fill_color='lavender',
               align='left'))
                ])
graph_table_google_related_rising = go.Figure(data=[go.Table(
    header=dict(values=list(google_rising.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[google_rising['연관 검색어'], google_rising['가중치']],
               fill_color='lavender',
               align='left'))
                ])


#------------------------대시보드 레이아웃 ----------------------------------
app = Dash(external_stylesheets = [ dbc.themes.MINTY],)

app.layout = html.Div(id = 'parent_div', children = [
    html.Div(id = 'header',children = [html.H1(f'상품 키워드 검색/분석 결과')], 
                                        style = {'textAlign':'center',
                                                 'margin-top':'10px',
                                                 'margin-bottom':'10px'}),
    html.Hr(style = {'border':'1px'}),
    html.Div(id = 'naver_keyword', children = [
        html.H3('네이버 키워드 분석 결과 : ', style = {'margin-left':'65px',
                                              'margin-top':'30px',
                                              'margin-bottom':'30px'}),
        html.Div(id = 'card', children = [
            dbc.Container([
                dbc.Row([
                    dbc.Col(dbc.Card(card_keyword, color = 'info', outline = True)),
                    dbc.Col(dbc.Card(card_search_volume, color = 'info', outline = True)),
                    dbc.Col(dbc.Card(card_click_volume, color = 'info', outline = True))
                        ])],
                        style={'textAlign':'center',
                            'whiteSpace':'normal'},
                        fluid = False)
        ]),
        html.Br(),
        html.Div(id = 'graph', children = [
            dbc.Container([
            dbc.Row([
            # 그래프		
                # dbc.Col(dcc.Graph(figure = graph_figure_naver_search_trend)),
                # dbc.Col(dcc.Graph(figure = bar_figure_naver_top10_related))
                dbc.Col(dcc.Graph(figure = graph_line_naver_search_trend)),
                dbc.Col(dcc.Graph(figure = graph_bar_naver_related_top))
                ]),
            ],style={'textAlign':'center',
                    'whiteSpace':'normal',
                    'maxWidth':'100%',
                    'Display':'inline-block'}, fluid = True),
        ])]),
    html.Hr(style = {'border':'1px'}),
    html.Div(id = 'naver_product', children = [
        html.H3('네이버 상품 분석 결과 : ', style = {'margin-left':'65px',
                                                'margin-bottom':'30px'}),
        html.Div(id = 'naver_item_price_card', children = [
            dbc.Container([
                dbc.Row([
                    dbc.Col(dbc.Card(card_naver_min_price, color = 'info', outline = True)),
                    dbc.Col(dbc.Card(card_naver_avg_price, color = 'info', outline = True)),
                    dbc.Col(dbc.Card(card_naver_max_price, color = 'info', outline = True))
                    ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=graph_scatter_naver_item_price)),
                    dbc.Col(dcc.Graph(figure=graph_pie_naver_brand_dist))
                    ])
                ],
                        style={'textAlign':'center',
                            'whiteSpace':'normal'},
                        fluid = False)
        ])]),

    html.Br(),
    html.Hr(style = {'border':'1px'}),
    html.Div(id = 'shopee_product', children = [
        html.H3('쇼피 상품 분석 결과 : ', style = {'margin-left':'65px',
                                                'margin-bottom':'30px'}),
        html.Div(id = 'shopee_item_price_card', children = [
            dbc.Container([
                dbc.Row([
                    dbc.Col(dbc.Card(card_shopee_min_price, color = 'primary', outline = True)),
                    dbc.Col(dbc.Card(card_shopee_avg_price, color = 'info', outline = True)),
                    dbc.Col(dbc.Card(card_shopee_max_price, color = 'info', outline = True)),
                    dbc.Col(dbc.Card(card_shopee_monthly_market_size, color = 'info', outline = True))
                    ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=graph_scatter_shopee_item_price)),
                    dbc.Col(dcc.Graph(figure=graph_pie_shopee_brand_dist))
                    ])
                ],
                        style={'textAlign':'center',
                            'whiteSpace':'normal'},
                        fluid = False)
            ])]),
        
    html.Br(),
    html.Hr(style = {'border':'1px'}),
    html.Div(id = 'google_keyword', children =[
    html.H3('구글 키워드 분석 결과 : ', style = {'margin-left':'65px',
                                              'margin-bottom':'30px'}),
    html.Div(id = 'google_search', children = [
        dbc.Container([
            dbc.Row([
                dbc.Col(dcc.Graph(figure= graph_bar_google_related_top)),
                dbc.Col(dcc.Graph(figure= graph_pie_google_keyword_dist))
                ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure= graph_line_google_search_trend)),
                dbc.Col(dcc.Graph(figure= graph_table_google_related_rising)),
                ]),
            ],
                    style={'textAlign':'center',
                           'whiteSpace':'normal'}, fluid = False)]),
    ])], style = {'margin-top':'20px'})


if __name__ == '__main__':
    app.run_server(debug=True)