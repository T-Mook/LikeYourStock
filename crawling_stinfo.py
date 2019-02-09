import pandas as pd
import datetime as dtime
import matplotlib.pyplot as plt
from matplotlib import style

path_kospi_stcd = 'D:/Stocks/Kospi_stockcd_20190203.csv' #Download from KRX

def read_stock_price_page(stock_code, page_num):
    '''
    네이버 주식시세 페이지에 접속하여 table을 dataframe으로 가져와서 정리
    '''
    target_url = ('http://finance.naver.com/item/sise_day.nhn?code='+ stock_code + '&page=' + str(page_num))
    page_data = pd.read_html(target_url)
    page_data = page_data[0]
    page_data.columns = ['날짜', '당일종가', '전일종가', '시가', '고가', '저가', '거래량']

    price_data = page_data.dropna(axis=0, how='any')
    price_data = price_data.drop(price_data.index[0])
    price_data = price_data.reset_index(drop=True)
    price_data['날짜'] = pd.to_datetime(price_data['날짜'], format='%Y/%m/%d')
    price_data.insert(loc=1, column='종목코드', value=stock_code)
    
    return price_data

def stock_price_pages_to_df(code, days_limit=30):
    '''
    오늘부터 days_limit 일수 만큼 이전 날짜 주가를 가져온다. 
    '''
    df_list_price = []
    page = 1
    while True:
        try:    
            data = read_stock_price_page(code, page)
            time_limit = dtime.datetime.now() - data['날짜'][0]  
            if time_limit.days > days_limit: break   
            else:
                df_list_price.append(data) #list 인자로 기간별 dataframe 전달
                page = page + 1
    
        except: break

    df_price = pd.concat(df_list_price, axis=0) #list 인자인 dataframe 합치기
    df_price = df_price.reset_index(drop=True)

    return df_price

stock_data = pd.read_csv(path_kospi_stcd) # Load Kospi stocks codes
stock_code = stock_data[['종목코드', '기업명']]

df_stprice_test = stock_price_pages_to_df(stock_code['종목코드'][0], days_limit=1200)
df_stprice_test.to_csv(path_or_buf='D:/Stocks/'+str(stock_code['기업명'][0])+'_sample.csv', encoding='utf-8')

print(df_stprice_test.head())
print(df_stprice_test.tail())

#for code in stock_code['종목코드'][:2]:
#    df_stprice = stock_price_pages_to_df(code, days_limit=10)

