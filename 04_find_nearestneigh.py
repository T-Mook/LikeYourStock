import sqlite3
import matplotlib as mpl; mpl.use('TkAgg') #only for MAC OS 
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.neighbors import NearestNeighbors

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
sampleFetures = sampleFetures.cumsum(axis=1) #cumulative sum, 일자누적

#from dataframe to numpy
sampleNameNdarray = sampleName.values
sampleFeturesNdarray = sampleFetures.values

#Part1 : PCA
X = sampleFeaturesNdarray
pca = decomposition.PCA(n_components=10)
pca.fit(X)
XTrans = pca.transform(X)

#Part2 : NN
X_fit = XTrans[:-1]
X_test = XTrans[-1]
nn = NearestNeighbors(n_neighbors=5)
nn.fit(X_fit)

#Part3 : 입력 종목과 유사한 종목 찾기
nn_dist, nn_index = nn.kneighbors([X_test]) #2D array 입력

#Part3-1 : 시각화
for i in nn_index[0]:
    plt.subplot(2, 1, 2)
    plt.plot(X[i], label=str(sampleNameNdarray[i]))
    plt.title("X_fit")
    plt.legend(loc=3)
    print(str(i)+"is done.")
# 
    # plt.subplot(4, 1, 4)
    # plt.plot(XTrans[i], label=str(sampleNameNdarray[i]))
    # plt.title("X_fit_PCA")
    # plt.legend(loc=3)
    # print(str(i)+"is done.")
    
plt.subplot(2, 1, 1)
plt.plot(X[-1], label=str(sampleNameNdarray[-1]))
plt.title("X_test")
plt.legend(loc=3)

# plt.subplot(4, 1, 2)
# plt.plot(XTrans[-1], label=str(sampleNameNdarray[-1]))
# plt.title("X_test_PCA")
# plt.legend(loc=3)

plt.show()