from click import style
import pandas as pd


google_rising = pd.read_csv('google_rising.csv')
google_top = pd.read_csv('google_top.csv')
shopee_item_info = pd.read_csv('shopee_item_info.csv')
keyword_search_volume = pd.read_csv('keyword_search_volume.csv')
top_10_related_keywords = pd.read_csv('top_10_related_keywords.csv')
naver_item_info = pd.read_csv('naver_item_info.csv')
naver_trend = pd.read_csv('naver_trend.csv')

google_rising,
google_top,
shopee_item_info,
keyword_search_volume,
top_10_related_keywords,
naver_item_info,
naver_trend

# import dash, dash_html_components as html, dash_table
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, Dash
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly          #(version 4.4.1)
import plotly.express as px


keyword = '밥솥'

app = Dash(external_stylesheets = [ dbc.themes.MINTY],)

card_keyword = [
    dbc.CardHeader("검색 키워드"),
    dbc.CardBody([html.H3(f"{keyword}")])  
    ]
card_pc_search_volume = [
    dbc.CardHeader("월간 검색량(PC) / 클릭률"),
    dbc.CardBody([html.H3(f"{keyword_search_volume.iloc[0][1]} / {keyword_search_volume.iloc[0][5]}%")])  
    ]
card_mobile_search_volume = [
    dbc.CardHeader("월간 검색량(모바일) / 클릭률"),
    dbc.CardBody([html.H3(f"{keyword_search_volume.iloc[0][2]} / {keyword_search_volume.iloc[0][6]}%")])  
    ]
graph_figure_naver_search_trend= {
                "data": [
                    {
                        "x": naver_trend["날짜"],
                        "y": naver_trend[keyword],
                        "type": "lines", "name":"naver"
                    }
                ],
                "layout": {"title":f"네이버 {keyword} 키워드 검색 추이"},
            }

bar_figure_naver_top10_related= {
                "data": [
                    {
                        "x": top_10_related_keywords['연관키워드'],
                        "y": top_10_related_keywords['월간검색수_모바일'],
                        "type": "bar", "name":"모바일"
                    },
                    {
                        "x": top_10_related_keywords['연관키워드'],
                        "y": top_10_related_keywords['월간검색수_PC'],
                        "type": "bar", "name":"PC"
                    }
                ],
                "layout": {"title":f"top10 연관 키워드 검색량"},
            }

table_naver_item = dash_table.DataTable(
    data = naver_item_info.to_dict('records'),
    columns = [{'id':c, 'name':c} for c in naver_item_info.columns],

    fixed_rows = {'headers':True},

    style_table = {'maxHeight':'450px'},

    style_header = {'backgroundColor':'rgb(20,100,20)',
                    'fontWeight':'bold',
                    'border':'4px solid white'},

    style_data_conditional = [

        {'if':{'row_index':'odd'},
            'backgroundColor':'rgb(224,224,224)',
            'fontSize':'15px'
        },

        {'if':{'row_index':'even'},
            'backgroundColor':'rgb(255,255,255)',
            'fontSize':'15px'
        }
    ],

    style_cell = {
        'textAlign':'center',
        'border':'0.5px solid gray',
        'whiteSpace':'normal'

    }
)

naver_keyword = dash_table.DataTable(
    data = keyword_search_volume.to_dict('records'),
    columns = [{'id':c, 'name':c} for c in keyword_search_volume.columns]
)

table = dash_table.DataTable(
    data = shopee_item_info.to_dict('records'),
    columns = [{'id':c, 'name':c} for c in shopee_item_info.columns],

    fixed_rows = {'headers':True},

    style_table = {'maxHeight':'450px'},

    style_header = {'backgroundColor':'rgb(20,100,20)',
                    'fontWeight':'bold',
                    'border':'4px solid white'},

    style_data_conditional = [

        {'if':{'row_index':'odd'},
            'backgroundColor':'rgb(224,224,224)',
            'fontSize':'15px'
        },

        {'if':{'row_index':'even'},
            'backgroundColor':'rgb(255,255,255)',
            'fontSize':'15px'
        }
    ],

    style_cell = {
        'textAlign':'center',
        'border':'4px solid white',
        'maxWidth':'50px',
        'whiteSpace':'normal'

    }
)

graph_scatter_naver_item_price = px.scatter(naver_item_info, x='가격(원)', y='누적 리뷰수', symbol='상품명')


app.layout = html.Div(id = 'parent_div', children = [
    html.Div(id = 'card', children = [
        dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Card(card_keyword, color = 'primary', outline = True)),
                dbc.Col(dbc.Card(card_pc_search_volume, color = 'info', inverse = True)),
                dbc.Col(dbc.Card(card_mobile_search_volume, color = 'info', inverse = True))
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
            dbc.Col(dcc.Graph(figure = graph_figure_naver_search_trend)),
            dbc.Col(dcc.Graph(figure = bar_figure_naver_top10_related))
            ]),
        ],style={'textAlign':'center',
                'whiteSpace':'normal'}, fluid = True),
    ]),
    html.Div(id = 'naver_item', children = [
        dbc.Container([
            dbc.Row([
                dbc.Col(table_naver_item)
            ])
        ],style={'maxWidth':'50%'})
    ]),
    html.Br(),
    html.Div(id = 'naver_keyword', children = [naver_keyword]),
    html.Br(),
    html.Div(id = 'shopee', children = [table]),
    html.Div(id = 'naver_item_price', children=[dcc.Graph(figure=graph_scatter_naver_item_price)])
    ])


if __name__ == '__main__':
    app.run_server(debug=True)