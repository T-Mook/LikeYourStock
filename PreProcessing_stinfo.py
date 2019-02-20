import pandas as pd
import sqlite3
import re

''' Preprocessing (with Normalizations) Datas '''

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
    raw_data = raw_data.sort_values(by=["날짜"], ascending=True)
    preprocessed_data = raw_data.drop_duplicates(["날짜"])
    preprocessed_data = preprocessed_data.drop(["전일종가"], axis=1)
    preprocessed_data = preprocessed_data.drop(["index"], axis=1)
    preprocessed_data = preprocessed_data.reset_index(drop=True)
    preprocessed_data = preprocessed_data.set_index("날짜")
    
    callcolumns = ['당일종가', '시가', '고가', '저가', '거래량'] 
    preprocessed_data = preprocessed_data[callcolumns].astype(dtype='int64') #dtype 변경

    #Normalization
    preprocessed_nml_data = preprocessed_data.pct_change(periods=1) #표준화, 전일대비 %로 바꿈
    preprocessed_nml_data = preprocessed_nml_data.dropna(axis=0, how='any')
    
    #Insert code column 
    preprocessed_data.insert(loc=0, column='종목코드', value=code)
    preprocessed_nml_data.insert(loc=0, column='종목코드', value=code)

    #Make new table with normalizaion and Time Series
    nmlprice_by_date = preprocessed_nml_data.copy(deep=False) #deep=True 시 원본과 복제간 data 연동됨
    nmlprice_by_date["날짜"] = nmlprice_by_date.index
    #nmlprice_by_date = nmlprice_by_date.reset_index(drop=True)
    try:
        nmlprice_by_date = nmlprice_by_date.pivot(index="종목코드", columns="날짜", values="당일종가")
    except:
        print(nmlprice_by_date.head())
        print(str(code))

    result_list = [preprocessed_data, preprocessed_nml_data, nmlprice_by_date]

    return result_list

nmldata_bystock_list = []
pattern_stcd = re.compile(r"\d{6}")
i = 0
for code in stock_code['종목코드']:
    '''Preprocessing raw data with Nomalization'''
    if pattern_stcd.match(code) != None:
        table_name1 = str('prestp'+str(code))
        table_name2 = str('nmlstp'+str(code))
    
        result_list = preprocessing_raw_pricedata(code)
        result_list[0].to_sql(name=table_name1, con=conn_save, if_exists="replace")
        result_list[1].to_sql(name=table_name2, con=conn_save, if_exists="replace")
        nmldata_bystock_list.append(result_list[2]) #list 인자로 종목별 dataframe 전달
      
        i += 1
        if i % 100 == 0:
            print(str(i) + " stocks are preprocessed.")
        else:
            pass
    else:
        print(str(code))

nmldata_bystock_df = pd.concat(nmldata_bystock_list, axis=0) #list 인자인 dataframe 합치기
nmldata_bystock_df = nmldata_bystock_df.fillna(0) #null to zero
nmldata_bystock_df.to_sql(name="tsnmp00", con=conn_save, if_exists="replace") #Time Sereis Normalization Price in Kospi(00)

print(str(i) + " stocks are preprocessed.")
print("Done.")

conn.close() #sqlite3 연결 종료문
conn_save.close()
