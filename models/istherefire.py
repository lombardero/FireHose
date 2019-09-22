import numpy as np
import pandas as pd
import os

# Loading data
PATH = os.getcwd() + '/data/fire_train_data.csv'
fires = pd.read_csv(PATH)
fires = fires[['temp','RH','wind', 'rain', 'cats']]

# Creating test & train data
X_fire = fires.drop(['cats'], axis=1)
y_fire = fires['cats']
from sklearn.model_selection import train_test_split
X_tr, X_tst, y_tr, y_tst = train_test_split(X_fire,y_fire,test_size = 0.3, random_state = 101)

# Creating & training model
from sklearn.svm import SVC
model_fireorno = SVC(probability = True, random_state = 101)
model_fireorno.fit(X_tr,y_tr)
pred_fire = model_fireorno.predict(X_tst)

#Defining functions
def predict_fire(temp, RH, wind, rain):
    input_df = pd.DataFrame(columns=[['temp','RH','wind', 'rain']], index = ['ipt'])
    input_df.loc['ipt','temp'] = temp
    input_df.loc['ipt','RH'] = RH
    input_df.loc['ipt','wind'] = wind
    input_df.loc['ipt','rain'] = rain
    return model_fireorno.predict(input_df)[0]
def confidence_fire(temp, RH, wind, rain):
    input_df = pd.DataFrame(columns=[['temp','RH','wind', 'rain']], index = ['ipt'])
    input_df.loc['ipt','temp'] = temp
    input_df.loc['ipt','RH'] = RH
    input_df.loc['ipt','wind'] = wind
    input_df.loc['ipt','rain'] = rain
    return model_fireorno.predict_proba(input_df)[0][1]