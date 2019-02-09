import pandas as pd

stock_code = '005930'
page_num = '1'

target_url = ('http://finance.naver.com/item/sise_day.nhn?code='+ stock_code + '&page=' + str(page_num))
data = pd.read_html(target_url)
data = data[0]
data.columns = ['날짜', '당일종가', '전일종가', '시가', '고가', '저가', '거래량']

stprice_data = data.dropna(axis=0, how='any')
stprice_data = stprice_data.drop(stprice_data.index[0])
stprice_data = stprice_data.reset_index(drop=True)
stprice_data['날짜'] = pd.to_datetime(stprice_data['날짜'], format='%Y/%m/%d')

print(stprice_data.tail(n=30))