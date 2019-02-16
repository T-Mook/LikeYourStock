import pandas as pd
import sqlite3

''' Preprocessing Datas '''

#Load Stock Code from KRX csv file
path_kospi_stcd = 'D:/Stocks/Kospi_stockcd_20190203.csv' #Download from KRX
stock_data = pd.read_csv(path_kospi_stcd) # Load Kospi stocks codes
stock_code = stock_data[['종목코드']]

#Load from SQLite3 DB
conn = sqlite3.connect('d:/Stocks/kospi91d.db') #Test용 KOSPI 91일 DB
cur = conn.cursor() 
conn_save = sqlite3.connect('d:/Stocks/ppkospi91d.db') #Preprocessed Raw data
cur_save = conn_save.cursor()

def preprocessing_raw_pricedata(code):
    table_name = "stp"+str(code)
    query = "SELECT * FROM "+str(table_name) #267850는 이미 중복이 확인되었던 종목이다.
    raw_data = pd.read_sql(sql=query, con=conn)

    #sorting, del duplicates and resorting
    raw_data = raw_data.sort_values(by=['날짜'], ascending=True)
    preprocessed_data = raw_data.drop_duplicates()
    preprocessed_data = preprocessed_data.drop(["전일종가"], axis=1)
    preprocessed_data = preprocessed_data.drop(["index"], axis=1)
    preprocessed_data = preprocessed_data.reset_index(drop=True)
    preprocessed_data = preprocessed_data.set_index("날짜")
    
    callcolumns = ['당일종가', '시가', '고가', '저가', '거래량']
    preprocessed_data = preprocessed_data[callcolumns].astype(dtype='int64') #dtype 변경

    #Normalization
    preprocessed_nml_data = preprocessed_data.pct_change(periods=1) #표준화
    preprocessed_nml_data = preprocessed_nml_data.dropna(axis=0, how='any')
    
    #Insert code column 
    preprocessed_data.insert(loc=0, column='종목코드', value=code)
    preprocessed_nml_data.insert(loc=0, column='종목코드', value=code)

    result_list = [preprocessed_data, preprocessed_nml_data]

    return result_list

i = 0
for code in stock_code['종목코드'][:3]:
    '''Preprocessing raw data with Nomalization'''
    table_name1 = str('prestp'+str(code))
    table_name2 = str('nmlstp'+str(code))

    result_list = preprocessing_raw_pricedata(code)
    result_list[0].to_sql(name=table_name1, con=conn_save, if_exists = "replace")
    result_list[1].to_sql(name=table_name2, con=conn_save, if_exists = "replace")
    
    i += 1
    if i % 100 == 0:
        print(str(i) + " stocks are preprocessed.")
    else:
        pass

print(str(i) + " stocks are preprocessed.")
print("Done.")

conn.close() #sqlite3 연결 종료문
conn_save.close()