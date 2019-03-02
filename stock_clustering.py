import matplotlib as mpl; mpl.use('TkAgg') #only for MAC OS 
import matplotlib.pyplot as plt
#import mglearn
import sqlite3
import pandas as pd
from sklearn import decomposition

dataPathInMac = "/Users/tmook/documents/Projects/LikeYourStock/Stocks/ppkospi91d.db" #Mac 경로
dataPathInWin = "d:/Stocks/ppkospi91d.db"

conn = sqlite3.connect(dataPathInMac) #Preprocessed Raw data
cur = conn.cursor()

tableName = "tsnmp00"
query = "SELECT * FROM "+str(tableName)
sampleData = pd.read_sql(sql=query, con=conn)

#name, features로 쪼개기
sampleName = sampleData['종목코드']
sampleFetures = sampleData[sampleData.columns[1:]]
sampleNameNdarray = sampleName.values
sampleFeturesNdarray = sampleFetures.values

X = sampleFeturesNdarray

#part1 : PCA
pca = decomposition.PCA(n_components=6)
pca.fit(X)
XTrans = pca.transform(X)

#PCA check
for i in range(0, 5): # 전체는 X.shape[1]
    plt.subplot(2, 1, 1)
    plt.plot(X[i])
    plt.title("original")

    plt.subplot(2, 1, 2)
    plt.plot(XTrans[i])
    plt.title("After PCA")

plt.show()

conn.close() #sqlite3 연결 종료문