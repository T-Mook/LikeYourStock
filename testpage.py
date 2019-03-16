import sqlite3
import matplotlib as mpl; mpl.use('TkAgg') #only for MAC OS 
import matplotlib.pyplot as plt
import pandas as pd

from sklearn import decomposition
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
sampleFeaturesNdarray = sampleFetures.values
X = sampleFeaturesNdarray

def Quickly_SetDetach(X):
    X_fit = X[:-1] #for NN train
    X_test = X[-1] #for NN test
    return_list = [X_fit, X_test]
    return return_list

def Scoring_PCA_before_NN(X, n_components, n_neighbors):
    result_list = []
    origin_nn_index_list = []
    pca_nn_index_list = []
    for v in range(int(n_components)+1)[1:]:
        for w in range(int(n_neighbors)+1)[1:]:
            #Part : Original -> nn
            X_fit, X_test = Quickly_SetDetach(X)
            nn = NearestNeighbors(n_neighbors=w)
            nn.fit(X_fit)
            origin_nn_dist, origin_nn_index = nn.kneighbors([X_test]) # 원본 dist & index
            origin_nn_index_list.append(origin_nn_index)
            
            #Part : PCA -> nn
            pca = decomposition.PCA(n_components=v)
            pca.fit(X)
            XTrans = pca.transform(X)
            XTrans_fit, XTrans_test = Quickly_SetDetach(XTrans)
            nn = NearestNeighbors(n_neighbors=w)
            nn.fit(XTrans_fit)
            pca_nn_dist, pca_nn_index = nn.kneighbors([XTrans_test]) #2D array 입력
            pca_nn_index_list.append(pca_nn_index)

    #Part : Compare original index & pca index
    for v, w in range():
        # 비교 코드
                    
#Part3 : 스코어링 및 시각화
for i in nn_index[0]:
    plt.subplot(2, 1, 2)
    plt.plot(X[i], label=str(sampleNameNdarray[i]))
    plt.title("X_fit")
    plt.legend(loc=3)
    print(str(i)+"is done.")
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