import sqlite3
import matplotlib as mpl; mpl.use('TkAgg') #only for MAC OS 
import matplotlib.pyplot as plt
import pandas as pd

from sklearn import decomposition
from sklearn.neighbors import NearestNeighbors

dataPathInMac = "/Users/tmook/documents/Projects/LikeYourStock/Stocks/ppkospi91d.db" #Mac 경로
dataPathInWin = "d:/Stocks/ppkospi91d.db"

conn = sqlite3.connect(dataPathInWin) #Preprocessed Raw data
cur = conn.cursor()

def Quickly_SetDetach(X):
    X_fit = X[:-1] #for NN train
    X_test = X[-1] #for NN test
    return_list = [X_fit, X_test]
    return return_list

def two_list_compare_scoring(target, sample):
    diff_set = list(set(target) - set(sample)) # 원본 NN 인덱스, PCA 후 NN 인덱스 차집합
    score = (len(target) - len(diff_set)) / len(target)
    return [score, list(diff_set)]

def Scoring_PCA_before_NN(X, n_components, n_neighbors):
    result_list = []
    origin_nn_index_list = []
    pca_nn_index_list = []
    pca_var_list = []
    nn_var_list = []
    for v in range(int(n_components)+1)[1:]:
        for w in range(int(n_neighbors)+1)[1:]:
            pca_var_list.append(int(v))
            nn_var_list.append(int(w))
            
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
            print("----------------------------")
            print("n_components: {}".format(str(v)))
            print("n_neighbors: {}".format(str(w)))
            print("Done.")
            print("----------------------------")
    
    #Part : Compare original index & pca index
    scoreboard = pd.DataFrame()
    for i in range(len(origin_nn_index_list)):
        before_list = list(origin_nn_index_list[i][0]) # 원본 PCA n_components(i+1개) NN 인덱스
        after_list = list(pca_nn_index_list[i][0]) # PCA 후 PCA n_components(i+1개) NN 인덱스
        score, diffset = two_list_compare_scoring(before_list, after_list)
        score_columns = ['pca_comp', 'nn_neigh', 'score', 'before_pca', 'after_pca', 'diffset']
        eachscore = pd.DataFrame(data=[[pca_var_list[i], nn_var_list[i], score, before_list, after_list, diffset]], columns=score_columns)
        scoreboard = scoreboard.append(eachscore)
        print("Scoring number : {}".format(str(i)))
    
    print("Scoring Done.")    
    return scoreboard

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

var_test_score = Scoring_PCA_before_NN(X, n_components=10, n_neighbors=10) # 뒤 두 개의 변수를 변경하면 된다.
var_test_score.to_excel("d:/Stocks/var_test_score.xlsx", encoding="UTF-8")
print(var_test_score)
