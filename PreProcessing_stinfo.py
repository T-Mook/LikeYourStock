import pandas as pd
import sqlite3

conn = sqlite3.connect('d:/Stocks/kospi91d.db') #Test용 KOSPI 91일 DB
cur = conn.cursor()

table_name = "stp267850"
query = "SELECT * FROM "+str(table_name) #267850는 이미 중복이 확인되었던 종목이다.

price_data = pd.read_sql(sql=query, con=conn)
price_data = price_data.set_index("index")

#sorting, del duplicates and resorting
price_data = price_data.sort_values(by=['날짜'], ascending=True)
price_data = price_data.drop_duplicates()
price_data = price_data.sort_values(by=['날짜'], ascending=False) #현 DB에 맞춰서 ascending bool값 전달
price_data = price_data.reset_index(drop=True)

price_data.rename(columns={"전일종가":"전일대비"}, inplace=True)

price_data.to_sql(name=table_name, con=conn, if_exists='replace')