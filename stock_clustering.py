import sqlite3
import pandas as pd
import sklearn

conn = sqlite3.connect('d:/Stocks/ppkospi91d.db') #Preprocessed Raw data
cur = conn.cursor()
