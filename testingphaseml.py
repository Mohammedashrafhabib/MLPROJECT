1# -*- coding: utf-8 -*-
"""TestingPhaseML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/181fU0SQVeBhHRWf7CfNsAowocitI69zT

# Imports & Read Data
"""

# Imports
from pydoc import describe
import sklearn
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from category_encoders import  LeaveOneOutEncoder as l1o
from sklearn.preprocessing import MultiLabelBinarizer
from pandas.io.formats.style_render import Subset
from sklearn import tree
from sklearn.metrics import confusion_matrix
from sklearn.metrics import multilabel_confusion_matrix
import joblib
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier,OneVsOneClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

svm=joblib.load("SVM(linear).pkl")
tree=joblib.load("tree_random_state=1334.pkl")
logistic=joblib.load("Logistic.pkl")
linear=joblib.load("lin.pkl")
forst=joblib.load("RandomForest(max_depth=16,random_state=49,max_features=4,criterion='entropy',n_estimators=700,min_samples_split=3,).pkl")
polyregsion=joblib.load("poly_regerssion[degree=2_random_state=453].pkl")
fillnalist=joblib.load("ToSaveList.pkl")
bodytype=joblib.load("body_typeLabelEncoder.pkl")
clubpostion=joblib.load("club_positionleave1out.pkl")
nationality=joblib.load("nationalityleave1out.pkl")
postions=joblib.load("positionsLabelEncoder.pkl")
prefered_foot=joblib.load("preferred_footLabelEncoder.pkl")
polyfeat=joblib.load("22PolynomialFeatures(degree=2).pkl")
fillnalist["club_join_date"]=fillnalist["club_join_date"].split('/')[2]#13/5/2001 
  
print(bodytype.classes_)
def applyFeatureEngineering(x):
  # Split "work_rate" into "work_rate_attack" and "work_rate_defense"
  x[['work_rate_attack','work_rate_defense']]=x['work_rate'].str.split('/ ',1,expand=True)
  x.drop('work_rate',axis=1,inplace=True)

  # Extract dates from columns "club_join_date" & "contract_end_year

  # Column "club_join_date"
  x['club_join_date']=x['club_join_date'].str.split('/',2,expand=True)[2]#13/5/2001 
  x=x.astype({'club_join_date':'float'})
  x['birth_date']=x['birth_date'].str.split('/',2,expand=True)[2]#13/5/2001 
  x=x.astype({'birth_date':'float'})
  # Column "contract_end_year"
  
  x=x.astype({'contract_end_year':'str'})
  x['contract_end_year']=x['contract_end_year'].apply(lambda z: '20'+z.split('-',2)[2] if (len(z)>4)else z)
  x=x.astype({'contract_end_year':'float'})
  print(x['contract_end_year'])
  # Loops over all position columns and adds the bonuses to the original score & fills nulls with mean of result
  # Ex: 62+2 --> 64
  # Assume mean = 61: null --> 61
  for i in range(x.columns.get_loc('LS'),x.columns.get_loc('RB')+1):
    x=x.astype({x.columns[i]:'str'})
    x[x.columns[i]]=x[x.columns[i]].apply(lambda z: int(z.split('+',2)[0])+int(z.split('+',2)[1])if(z!='nan'and len(z)>2)else z)
    x=x.astype({x.columns[i]:'float'})
    
    x[x.columns[i]].fillna(fillnalist[x.columns[i]],inplace=True)
    # Question: Why is the column casted to int then to float?
    x=x.astype({x.columns[i]:'int'})
    x=x.astype({x.columns[i]:'float'})
  return x

# Helper Functions


def encode_club_position(df):
    if (df['club_position'] == 'GK'):
        return 'GK'
    elif ((df['club_position'] == 'RB') | (df['club_position'] == 'LB') | (df['club_position'] == 'CB') | (df['club_position'] == 'LCB') | (df['club_position'] == 'RCB') | (df['club_position'] == 'RWB') | (df['club_position'] == 'LWB') ):
        return 'DF'
    elif ((df['club_position'] == 'LDM') | (df['club_position'] == 'CDM') | (df['club_position'] == 'RDM')):
        return 'DM'
    elif ((df['club_position'] == 'LM') | (df['club_position'] == 'LCM') | (df['club_position'] == 'CM') | (df['club_position'] == 'RCM') | (df['club_position'] == 'RM')):
        return 'MF'
    elif ((df['club_position'] == 'LAM') | (df['club_position'] == 'CAM') | (df['club_position'] == 'RAM') | (df['club_position'] == 'LW') | (df['club_position'] == 'RW')):
        return 'AM'
    elif ((df['club_position'] == 'RS') | (df['club_position'] == 'ST') | (df['club_position'] == 'LS') | (df['club_position'] == 'CF') | (df['club_position'] == 'LF') | (df['club_position'] == 'RF')):
        return 'ST'
    else:
        return df.club_position

def encode_positions(position):
   position = position[0]
   if (position == 'GK'):
        return 'pos_GK'
   elif ((position == 'RB') | (position == 'LB') | (position == 'CB') | (position == 'LCB') | (position == 'RCB') | (position == 'RWB') | (position == 'LWB') ):
      return 'pos_DF'
   elif ((position == 'LDM') | (position == 'CDM') | (position == 'RDM')):
      return 'pos_DM'
   elif ((position == 'LM') | (position == 'LCM') | (position == 'CM') | (position == 'RCM') | (position == 'RM')):
      return 'pos_MF'
   elif ((position == 'LAM') | (position == 'CAM') | (position == 'RAM') | (position == 'LW') | (position == 'RW')):
      return 'pos_AM'
   elif ((position == 'RS') | (position == 'ST') | (position == 'LS') | (position == 'CF') | (position == 'LF') | (position == 'RF')):
       return 'pos_ST'
   else:
       return 'pos_'+position

def applyLabelEncoding(x):
  ## columns "work_rate_attack" & "work_rate_defense"
  x["work_rate_attack"]= np.where(x["work_rate_attack"]=="High",2,np.where(x["work_rate_attack"]=="Low",0,1))
  x["work_rate_defense"]= np.where(x["work_rate_defense"]=="High",2,np.where(x["work_rate_defense"]=="Low",0,1))

  ## columns "club_position" & "body_type" & "preferred_foot" 
  label_encoder_classes=list(bodytype.classes_)
  x.loc[~x["body_type"].isin(label_encoder_classes),"body_type"]="Normal"
 # x.body_type=np.where(x.body_type==,'Normal',x.body_type )
  x.body_type=bodytype.transform(x.body_type)
  x.preferred_foot= prefered_foot.transform(x.preferred_foot)
 # x=Feature_Encoder(x,['body_type','preferred_foot'])
  x['preferred_foot_right']=x['preferred_foot']#have no order()
  x.drop('preferred_foot',axis=1,inplace=True)
  #x=Feature_Encoder(x,["national_team_position"])

  ## column "positions"
  first_pos = x['positions'].str.split(',', expand=True)[0]
  first_pos = pd.DataFrame(first_pos)
  x['positions'] = first_pos.apply(encode_positions, axis=1)
  x.positions=postions.transform(x.positions)
  #x = Feature_Encoder(x, ['positions'])


  # //////
  
  return x

def applyLeaveOneOutEncoding(x,y):
  ## Columns "nationality" & "club_team" & "positions" using leave one out encoding
  
  y.index=x.index
  # QUESTION: Why club_team twice?
  # x['club_team']=leave1out.fit_transform(x['club_team'],y)
  #x['club_team']=leave1out.fit_transform(x['club_team'],y)
  x['nationality']=nationality.transform(x['nationality'])
  #x['nationality']=leave1out.fit_transform(x['nationality'],y)
  # Column "club_position"
  
  x['club_position'] = x.apply(encode_club_position, axis = 1)
  x['club_position'] =clubpostion.transform(x['club_position'])
  #x['club_position']=leave1out.fit_transform(x['club_position'],y)
  #joblib.dump(leave1out, "club_positionleave1out.pkl")
  return x

# Drop highly correlated features
def dropColumns(x,cols):
  x.drop(cols, axis=1, inplace=True)
def missingvalue(x):
  for i in x.columns:
    x[i].fillna(fillnalist[i],inplace=True)

ans=input("1:regression\2:classification||")
if ans=='1':
  
  data = pd.read_csv('player-tas-regression-test.csv')#Enter test file path
  data.dropna(axis=0,how='any', subset=['value'],inplace=True)
  #data = pd.read_csv('player-tas-regression-test.csv')#Enter test file path
  print(f"Data has {data.shape[0]} Rows and {data.shape[1]} Features")
  pd.set_option('display.min_rows',500)
  
  data=applyFeatureEngineering(data)
  data=applyLabelEncoding(data)
  y=data['value']
  x=data.drop('value', axis = 1,inplace=True)
  data=applyLeaveOneOutEncoding(data,y)
  
  to_drop = ['RCB', 'CB', 'LCB', 'LB', 'RWB', 'RDM', 'CDM', 'LDM', 'LWB', 'LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW', 'LAM', 'CAM', 'RAM','LM','LCM','CM','RM','GK_diving', 'GK_handling', 'GK_positioning', 'GK_reflexes', 'standing_tackle','sliding_tackle','ball_control','positioning','acceleration','traits',
            'tags','name','full_name','birth_date','id','height_cm','club_jersey_number','club_team' ,'tags','traits','national_team',
  'national_rating', 'national_team_position', 'national_jersey_number']
  dropColumns(data,to_drop)
  x=data
  missingvalue(x)
  print(x.columns)
  print(y.isna().sum())
  #print(fillnalist["club_join_date"])
 # fillnalist["club_join_date"]=fillnalist["club_join_date"].str.split('/',2,expand=True)[2]#13/5/2001 
  #x=x.astype({'club_join_date':'float'})
  print(x.club_join_date)
  
  ypred=linear.predict(x)
  print(y,ypred)
  print('Test MSE: ',metrics.mean_squared_error(y,ypred))
  print('Test R2 score: ', metrics.r2_score(y,ypred))
  
  ypred=polyregsion.predict(polyfeat.transform(x))
  
  print('Test MSE: ',metrics.mean_squared_error(y,ypred))
  print('Test R2 score: ', metrics.r2_score(y,ypred))
else:
  data = pd.read_csv('player-tas-classification-test.csv')#Enter test file path
  print(f"Data has {data.shape[0]} Rows and {data.shape[1]} Features")
  pd.set_option('display.min_rows',500)
  data=applyFeatureEngineering(data)
  data=applyLabelEncoding(data)
  y=data['PlayerLevel']
  x=data.drop('PlayerLevel', axis = 1,inplace=True)
  y= np.where(y=="S",5,np.where(y=="A",4,np.where(y=="B",3,np.where(y=="C",2,1))))
  y=pd.DataFrame(y)
  data=applyLeaveOneOutEncoding(data,y)
  x=data
  to_drop = ['RCB', 'CB', 'LCB', 'LB', 'RWB', 'RDM', 'CDM', 'LDM', 'LWB', 'LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW', 'LAM', 'CAM', 'RAM','LM','LCM','CM','RM','GK_diving', 'GK_handling', 'GK_positioning', 'GK_reflexes', 'standing_tackle','sliding_tackle','ball_control','positioning','acceleration','traits',
            'tags','name','full_name','birth_date','id','height_cm','club_jersey_number','club_team' ,'tags','traits','national_team',
  'national_rating', 'national_team_position', 'national_jersey_number',]
  dropColumns(data,to_drop)
  missingvalue(x)
  
  print('Test accuracy: ',svm.score(x,y))
  
  
  
  print('Test accuracy: ',tree.score(x,y))
  
  print('Test accuracy: ',logistic.score(x,y))
  
  
  
  
  print('Test accuracy: ',forst.score(x,y))