import pandas as pd
import sqlite3

''' Check Crawling Datas '''

conn = sqlite3.connect('d:/Stocks/kospi91d.db') #Test용 KOSPI 3개월 DB
cur = conn.cursor()

path_kospi_stcd = 'D:/Stocks/Kospi_stockcd_20190203.csv' #Download from KRX
stock_data = pd.read_csv(path_kospi_stcd) # Load Kospi stocks codes
stock_code = stock_data[['종목코드']]

def check_price_datas(code):
    '''종목코드별 종합정보 Series화 function'''
    check_data = []
    table_name = "stp"+str(code)
    query = "SELECT * FROM "+str(table_name)
    original_data = pd.read_sql(sql=query, con=conn)
    original_data = original_data.set_index("index")
    original_data = original_data.sort_values(by=['날짜'], ascending=True) #내림차순 정렬

    check_data.append(original_data['날짜'].iloc[-1]) #시작일자
    check_data.append(original_data['날짜'].iloc[0]) #종료일자
    check_data_series = pd.Series(check_data)
    check_data_series = check_data_series.rename(str(code)) #Series.name rename
    describe_series = original_data['당일종가'].astype('int64').describe() #기본정보

    check_data_series = check_data_series.rename({0:"end", 1:"start"}) #index rename
    total_info_series = pd.concat([check_data_series, describe_series])

    return total_info_series

detail_info_df = pd.DataFrame()
for code in list(stock_code['종목코드']):
    try:
        stock_tinfo_series = check_price_datas(code)
        stock_tinfo_series = stock_tinfo_series.rename(str(code))
        detail_info_df = pd.concat([detail_info_df, stock_tinfo_series], axis=1)
    except:
        pass
    
#상세 테이블 정리
detail_info_df = detail_info_df.T #축 변경
column_sorting = ["start", "end", "count", "mean", "std", "min", "25%", "50%", "75%", "max"]
detail_info_df = detail_info_df[column_sorting]

#저장 파트
table_name = "chk00data"
detail_info_df.to_sql(name=table_name, con=conn, if_exists='replace')

#종합 정보 정리
total_check_list = []
total_check_list.append(len(detail_info_df.index)) #counting 종목코드
total_check_list.append(len(detail_info_df['start'].unique())) #counting 시작날짜
total_check_list.append(len(detail_info_df['end'].unique())) #counting 종료날짜

total_info_series = pd.Series(total_check_list) #making pd.Series
total_info_series = total_info_series.rename('total') #Series.name rename
total_info_series = total_info_series.rename({0:"st_cnt", 1:"unq_startdt", 2:"unq_enddt"}) #rename index

#저장 파트
table_name = "totalchk00data"
total_info_series.to_sql(name=table_name, con=conn, if_exists='replace')

print("Done.")

conn.close() #sqlite3 연결 종료문