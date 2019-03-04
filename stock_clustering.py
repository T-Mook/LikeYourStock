import sqlite3
import matplotlib as mpl; mpl.use('TkAgg') #only for MAC OS 
import matplotlib.pyplot as plt
#import mglearn
import pandas as pd
from sklearn import decomposition

dataPathInMac = "/Users/tmook/documents/Projects/LikeYourStock/Stocks/ppkospi91d.db" #Mac 경로
dataPathInWin = "d:/Stocks/ppkospi91d.db"

conn = sqlite3.connect(dataPathInWin) #Preprocessed Raw data
cur = conn.cursor()

tableName = "tsnmp00"
query = "SELECT * FROM "+str(tableName)
sampleData = pd.read_sql(sql=query, con=conn)

#name, features로 쪼개기
sampleName = sampleData['종목코드']
sampleFetures = sampleData[sampleData.columns[1:]]
sampleFetures = sampleFetures.cumsum(axis=1) #cumulative sum, 일자누적

#from dataframe to numpy
sampleNameNdarray = sampleName.values
sampleFeturesNdarray = sampleFetures.values

#part1 : PCA
X = sampleFeturesNdarray
pca = decomposition.PCA(n_components=4)
pca.fit(X)
XTrans = pca.transform(X)

#PCA check
for i in range(0, 3): # 전체는 X.shape[1]
    plt.subplot(2, 1, 1)
    plt.plot(X[i], label=str(sampleNameNdarray[i]))
    plt.title("original")
    plt.legend(loc=3)

    plt.subplot(2, 1, 2)
    plt.plot(XTrans[i], label=str(sampleNameNdarray[i]))
    plt.title("After PCA")
    plt.legend(loc=3)

plt.show()

conn.close() #sqlite3 연결 종료문
