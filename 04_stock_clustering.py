import sqlite3
import matplotlib as mpl; mpl.use('TkAgg') #only for MAC OS 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn import decomposition

dataPathInMac = "/Users/tmook/documents/Projects/LikeYourStock/Stocks/ppkospi91d.db" #Mac 경로
dataPathInWin = "d:/Stocks/ppkospi91d.db"
dirSaveFigInMac = "/Users/tmook/documents/Projects/LikeYourStock/Stocks/"
dirSaveFigInWin = "d:/Stocks/"

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
sampleFeaturesNdarray = sampleFetures.values

#part1 : PCA
X = sampleFeaturesNdarray
pca = decomposition.PCA(n_components=4)
pca.fit(X)
XTrans = pca.transform(X)

# #PCA check
# for i in range(0, 3): # 전체는 X.shape[1]
#     plt.subplot(2, 1, 1)
#     plt.plot(X[i], label=str(sampleNameNdarray[i]))
#     plt.title("original")
#     plt.legend(loc=3)
# 
#     plt.subplot(2, 1, 2)
#     plt.plot(XTrans[i], label=str(sampleNameNdarray[i]))
#     plt.title("After PCA (n_components=4)")
#     plt.legend(loc=3)
# 
# plt.show()

kmeans = KMeans(n_clusters=4)
kmeans.fit(XTrans)

#check kmeans
kmUnique, kmUCounts, kmIndex  = np.unique(kmeans.labels_, return_counts=True, return_index=True)

print("Total Label Count:{}".format(len(kmeans.labels_)))
print("Unique Label:\n{}".format(kmUnique))
print("Unique Label Count:\n{}".format(kmUCounts))
print("Unique Index Name:\n{}".format(sampleNameNdarray[kmIndex]))
print("Cluster Label:\n{}".format(kmeans.labels_))

#서로 다른 모양의 차트를 확인
for stNum, o, p  in zip(sampleNameNdarray[kmIndex], X[kmIndex], XTrans[kmIndex]):
    plt.subplot(2, 1, 1)
    plt.plot(o, label=str(stNum))
    plt.title("original")
    plt.legend(loc=3)

    plt.subplot(2, 1, 2)
    plt.plot(p, label=str(stNum))
    plt.title("After PCA (n_components=4)")
    plt.legend(loc=3)

plt.savefig(dirSaveFigInWin+"clusterRepresentativeStock.png", dpi=300)

#서로 비슷한 모양의 차트를 확인
for i in range(0, 4):
    labelIndex = np.where(kmeans.labels_ == i) # 특정 값의 index값 return
    for v in labelIndex[0][:5]:
        plt.subplot(2, 1, 1)
        plt.plot(X[v], label=str(sampleNameNdarray[v]))
        plt.title("original")
        plt.legend(loc=3)
        
        plt.subplot(2, 1, 2)
        plt.plot(XTrans[v], label=str(sampleNameNdarray[v]))
        plt.title("After PCA (n_components=4)")
        plt.legend(loc=3)
        
    plt.savefig(dirSaveFigInWin+"label_"+str(i)+".png", dpi=300)
    plt.close()

conn.close() #sqlite3 연결 종료문
