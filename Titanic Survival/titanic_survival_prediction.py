# -*- coding: utf-8 -*-
"""titanic-survival-prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/152tr4DxwrikK9ZTsFgaA0t0ETWMobNuo
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
# %matplotlib inline
sns.set()

df_train=pd.read_csv("/kaggle/input/titanic/train.csv")
df_train.head()

df_train.isna().sum()

"""### Age and Cabin has null value, embarked has 2 null values"""

df_train.info()

df_test=pd.read_csv("/kaggle/input/titanic/test.csv")
df_test.head()

"""### Data Exploration and Data Visualization"""

df_test.info()

df_test.isna().sum()

df_train.describe()

df_test.describe()

df_train.shape,df_test.shape

df_train.describe(include=['O'])

"""### Emabarked has more ***S*** so we can replace null value in Embarked with ***S***"""

survival=df_train[df_train['Survived']==1]
dead=df_train[df_train['Survived']==0]
print("Survival rate: %i (%.1f%%)"%(len(survival),float(len(survival)/len(df_train))*100.0))
print("Mortality rate : %i (%.1f%%)"%(len(dead),float(len(dead)/len(df_train))*100.0))

def bar_chart(feature):
    survived=df_train[df_train['Survived']==1][feature].value_counts()
    dead=df_train[df_train['Survived']==0][feature].value_counts()
    df=pd.DataFrame([survived,dead])
    df.index=['Survived','Dead']
    df.plot(kind='bar',stacked=True,figsize=(10,5))

df_train.groupby('Sex').Survived.value_counts()

df_train[['Sex','Survived']].groupby(['Sex'], as_index=False).mean()

bar_chart('Sex')

"""#### Survival rate for female is more and mortality rate is more for male"""

df_train[['Pclass','Survived']].groupby(['Pclass'], as_index=False).mean()

bar_chart('Pclass')

sns.factorplot('Sex','Survived',hue='Pclass',size=4, aspect=2,data=df_train)

sns.factorplot('Pclass','Survived',hue='Sex',col='Embarked',data=df_train)

"""#### 1 Pclass has more survival than othe Pclass"""

df_train[['Embarked','Survived']].groupby(['Embarked'], as_index=False).mean()

bar_chart('Embarked')

"""#### ppl Embarked from S port has both survival as Dead cases """

df_train['SibSp'].value_counts()

df_train[['SibSp','Survived']].groupby(['SibSp'], as_index=False).mean()

bar_chart('SibSp')

sns.barplot(x='SibSp',y='Survived',ci=None, data=df_train)

df_train['Parch'].value_counts()

bar_chart('Parch')

"""## Finding Age correlation with other features"""

fig = plt.figure(figsize=(15,5))
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)

sns.violinplot(x='Embarked',y='Age',hue='Survived',data=df_train,ax=ax1)
sns.violinplot(x='Pclass',y='Age',hue='Survived', data=df_train,ax=ax2)
sns.violinplot(x='Sex',y='Age',hue='Survived',data=df_train,ax=ax3)

data=[df_train,df_test]
for dataset in data:
    dataset['Title']=dataset['Name'].str.extract('([A-Za-z]+)\.',expand=False)

df_train['Title'].value_counts()

title_mapping={'Mr': 0,'Miss': 1,'Mrs': 2,'Master' : 3,'Dr': 3,'Rev': 3,'Mlle': 3,'Col': 3,'Major': 3,
               'Ms': 3,'Lady': 3,'Don': 3,'Capt': 3,'Sir': 3,'Jonkheer': 3,'Countess': 3, 'Mme': 3}
for dataset in data:
    dataset['Title']= dataset['Title'].map(title_mapping)

len(df_test[df_test['Title']==3])

df_train.head()

df_train['Age'].fillna(df_train.groupby('Title')['Age'].transform('median'), inplace=True)
df_test['Age'].fillna(df_test.groupby('Title')['Age'].transform('median'), inplace=True)

facet = sns.FacetGrid(df_train,hue='Survived',aspect=4)
facet.map(sns.kdeplot,'Age',shade=True)
facet.set(xlim=(0,df_train['Age'].max()))
facet.add_legend()
plt.show()

"""#### Will explore FacetGrid with different limits"""

facet = sns.FacetGrid(df_train,hue='Survived',aspect=4)
facet.map(sns.kdeplot,'Age',shade=True)
facet.add_legend()
plt.xlim(0,20)

facet = sns.FacetGrid(df_train,hue='Survived',aspect=4)
facet.map(sns.kdeplot,'Age',shade=True)
facet.add_legend()
plt.xlim(20,40)

facet = sns.FacetGrid(df_train,hue='Survived',aspect=4)
facet.map(sns.kdeplot,'Age',shade=True)
facet.add_legend()
plt.xlim(40,60)

facet = sns.FacetGrid(df_train,hue='Survived',aspect=4)
facet.map(sns.kdeplot,'Age',shade=True)
facet.add_legend()
plt.xlim(60)

plt.figure(figsize=(10,8))
sns.heatmap(df_train.drop(['PassengerId'],axis=1).corr(), annot=True)

for dataset in data:
    dataset['Sex'] = dataset['Sex'].map({'female': 1, 'male': 0}).astype(int)

df_train.head()

for df in data:
    df['Embarked'] = df['Embarked'].fillna('S')
    df['Fare'] = df['Fare'].fillna(df_train.median())
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    
print (df_train[['FamilySize', 'Survived']].groupby(['FamilySize'], as_index=False).mean())

embarked_mapping={'S': 0, "Q" : 1, "C" : 2}
for df in data:
    df['Embarked'] = df['Embarked'].map(embarked_mapping)

df_train.head()

df_test.head()

df_test.isna().sum()

for df in data:
    df['Cabin'] = df['Cabin'].str[:1]

df_train.head()

Pclass1 = df_train[df_train['Pclass']==1]['Cabin'].value_counts()
Pclass2 = df_train[df_train['Pclass']==2]['Cabin'].value_counts()
Pclass3 = df_train[df_train['Pclass']==3]['Cabin'].value_counts()
df = pd.DataFrame([Pclass1, Pclass2, Pclass3])
df.index = ['1st class','2nd class', '3rd class']
df.plot(kind='bar',stacked=True, figsize=(10,5))

cabin_mapping={'A': 0,'B': 1,'C': 2,'D': 3,'E': 4,'F': 5,'G': 6,'T':7}
for df in data:
    df['Cabin'] = df['Cabin'].map(cabin_mapping)

df_train["Cabin"].fillna(df_train.groupby("Pclass")["Cabin"].transform("median"), inplace=True)
df_test["Cabin"].fillna(df_test.groupby("Pclass")["Cabin"].transform("median"), inplace=True)

df_train.head(1)

df_test.head(1)

useless_features=['Name','SibSp','Parch','Ticket','PassengerId']
train = df_train.drop(useless_features,axis=1)
test = df_test.drop(useless_features,axis=1)

target = train['Survived']
train = train.drop(['Survived'],axis=1)

train.shape, test.shape

"""# Modelling"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, VotingClassifier,AdaBoostClassifier,GradientBoostingClassifier

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression

from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier

from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

"""### KNeighbors Classifier"""

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
kfold = KFold(n_splits=10, shuffle=True, random_state=0)

clf = KNeighborsClassifier(n_neighbors=10)
score=cross_val_score(clf,train, target, scoring='accuracy', cv=kfold, n_jobs=1)
print(score)

round(np.mean(score)*100,2)

"""### Decision Tree classifier"""

clf = DecisionTreeClassifier()
score = cross_val_score(clf, train, target, cv=kfold, n_jobs=1, scoring='accuracy')
print(score)
round(np.mean(score)*100,2)

"""### RandomForestClassifier"""

clf = RandomForestClassifier()
score = cross_val_score(clf, train, target, cv=kfold, n_jobs=1, scoring='accuracy')
print(score)
round(np.mean(score)*100,2)

"""### Naive bayes"""

clf = GaussianNB()
score = cross_val_score(clf, train, target, cv=kfold, n_jobs=1, scoring = 'accuracy')
print(score)
round(np.mean(score)*100,2)

"""### Support Vector machines Classifier"""

clf = SVC()
score = cross_val_score(clf, train, target, cv=kfold, n_jobs=1, scoring='accuracy')
print(score)
round(np.mean(score)*100,2)

"""### Linear SVC"""

clf = LinearSVC()
score = cross_val_score(clf, train, target, cv=kfold, n_jobs=1, scoring ='accuracy')
print(score)
round(np.mean(score)*100,2)

"""### Logistic Regression"""

clf = LogisticRegression()
score = cross_val_score(clf, train, target, cv=kfold,n_jobs=1, scoring='accuracy')
print(score)
round(np.mean(score)*100,2)

"""### Perceptron"""

clf = Perceptron()
score = cross_val_score(clf, train, target, cv=kfold, n_jobs=1,scoring='accuracy')
print(score)
round(np.mean(score)*100,2)

"""### SGDClassifier"""

clf = SGDClassifier()
score = cross_val_score(clf, train, target, cv=kfold,n_jobs=1,scoring='accuracy')
print(score)
round(np.mean(score)*100,2)

"""### MLPClassifier"""

clf = MLPClassifier()
score = cross_val_score(clf, train,target,cv=kfold, n_jobs=1,scoring='accuracy')
print(score)
round(np.mean(score)*100,2)

"""### XGBClassifier"""

clf =XGBClassifier()
score = cross_val_score(clf, train ,target, cv=kfold, n_jobs =1, scoring='accuracy')
print(score)
round(np.mean(score)*100,2)

"""### LinearDiscriminantAnalysis"""

clf = LinearDiscriminantAnalysis()
score = cross_val_score(clf, train, target, cv=kfold, n_jobs=1, scoring='accuracy')
print(score)
round(np.mean(score)*100,2)

"""### QuadraticDiscriminantAnalysis"""

clf =QuadraticDiscriminantAnalysis()
score = cross_val_score(clf, train, target, cv=kfold, n_jobs=1, scoring='accuracy')
print(score)
round(np.mean(score)*100,2)

mean = train.Fare.mean()
test.Fare = test.Fare.fillna(mean)

test['Title']=test['Title'].fillna(0.0)

models = pd.DataFrame({'model' : ['KNeighbors Classifier','Decision Tree classifier','RandomForestClassifier','Naive bayes',
                        'Support Vector machine Classifier'
                        ,'Linear SVC', 'Logistic Regression','Perceptron','SGDClassifier','MLPClassifier','XGBClassifier',
                       'LinearDiscriminantAnalysis','QuadraticDiscriminantAnalysis'],
                       'accuracy' : [72.84,76.21,80.92,79.46,67.79,64.18,81.37,70.37,70.7,80.7,82.49,81.48,79.91]})

models.sort_values(by = 'accuracy',ascending=False)

models = list()

models.append(LogisticRegression())
models.append(DecisionTreeClassifier())
models.append(RandomForestClassifier())
models.append(SVC())
models.append(ExtraTreesClassifier())
models.append(GradientBoostingClassifier())
models.append(AdaBoostClassifier(DecisionTreeClassifier(),learning_rate=0.1))
models.append(KNeighborsClassifier())
models.append(XGBClassifier())
models.append(GaussianNB())
models.append(LinearSVC())
models.append(Perceptron())
models.append(SGDClassifier())
models.append(MLPClassifier())
models.append(LinearDiscriminantAnalysis())
models.append(QuadraticDiscriminantAnalysis())

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
kfold = KFold(n_splits=10, shuffle=True, random_state=0)

kfold = StratifiedKFold(n_splits=10)

cv_results = []
cv_names = []

for model in models :
    cv_results.append(cross_val_score(model, train, y =target, scoring = "accuracy", cv = kfold, n_jobs=4))
    cv_names.append(model.__class__.__name__)

cv_means = []
cv_std = []

for cv_result in cv_results:
    cv_means.append(cv_result.mean())
    cv_std.append(cv_result.std())
    

cv_res = pd.DataFrame({"CrossValMeans":cv_means,"CrossValerrors": cv_std,"Algorithm":cv_names})
plt.figure(figsize=(15,8))
g = sns.barplot("CrossValMeans","Algorithm",data = cv_res,orient = "h",**{'xerr':cv_std})
g.set_xlabel("Average Accuracy")
g = g.set_title("K-fold Cross validation average accuracy")

cv_res['Criterion'] = cv_res['CrossValMeans'] - cv_res['CrossValerrors']/2

cv_res.sort_values(by='Criterion', ascending=False)

"""### Hyper Parameter Tunning"""

from sklearn.model_selection import GridSearchCV

"""#### Tunning Logistic Regression"""

solvers = ['liblinear','newton-cg','lbfgs']
penalty = ['l2','l1','elasticnet']
c_values = np.logspace(-2,2,100)
grid = dict(solver=solvers, penalty=penalty, C=c_values)
grid_Search = GridSearchCV(estimator=LogisticRegression(), param_grid=grid, n_jobs=1 ,cv=kfold, scoring='accuracy')
grid_res = grid_Search.fit(train, target)
lr_best = grid_res.best_estimator_


# printing best parameters from gridsearch

print('Best penalty : ',lr_best.get_params()['penalty'])
print('Best c_values : ',lr_best.get_params()['C'])
grid_res.best_score_

"""#### Tunnig Random Forest Classifier"""

max_feature=['sqrt','auto']
n_estimators = [10, 100, 1000]
min_samples_leaf = [2, 4]
min_samples_split = [5, 10]
max_depth = [int(x) for x in np.linspace(1, 20, num = 5)]

rf_param_grid=dict(n_estimators=n_estimators, max_features=max_feature,min_samples_split= min_samples_split,
              min_samples_leaf = min_samples_leaf, max_depth=max_depth
)
grid_Search_rfc = GridSearchCV(estimator=RandomForestClassifier(), param_grid=rf_param_grid, n_jobs=1 ,cv=kfold, scoring='accuracy')
grid_res_rfc = grid_Search_rfc.fit(train, target)
rfc_best = grid_res_rfc.best_estimator_


# printing best parameters from gridsearch

print('Best parameters : ',rfc_best.get_params())
grid_res_rfc.best_score_

"""#### Tunning Gradient Boosting Classifier"""

lr = [1, 0.25, 0.1, 0.05, 0.01] #eta value or lr
#the number of trees in the forest
n_estimators = [1, 2, 4,  32, 100, 150, 200,  300]
# how deep the built tree can be
max_depths = np.linspace(1, 32, 8, endpoint=True)

#minimum number of samples required to be at a leaf node.
min_samples_leafs =  np.linspace(0.1, 0.5, 4, endpoint=True)
#represents the number of features to consider when looking for the best split
max_features = [0.5, 0.3, 0.1]

GBC = GradientBoostingClassifier()
gb_param_grid = {'loss' : ["deviance"],
              'n_estimators' : n_estimators,
              'learning_rate': lr,
              'max_depth': max_depths,
              'min_samples_leaf': min_samples_leafs,
              'max_features': max_features
              }

gsGBC = GridSearchCV(GBC,param_grid = gb_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)

gsGBC.fit(train,target)

GBC_best = gsGBC.best_estimator_

print(GBC_best.get_params())


# Best score
gsGBC.best_score_

"""#### Tunning XGBoost Classifier"""

XGB = XGBClassifier()

#parameters
max_depth = [1,2,4,8,10]
min_child_weights = np.linspace(1,10,5,endpoint=True)
gamma = np.linspace(0.5,5, 5, endpoint = True)
subsample = np.linspace(0.5,1, 5, endpoint = True)
colsample_bytree = np.linspace(0.5, 1, 5, endpoint=True)


xgb_param_grid = {
    'min_child_weight': min_child_weights,
    'gamma': gamma,
    'subsample': subsample,
    'colsample_bytree': colsample_bytree,
    'max_depth': max_depth
}
gsXGB = GridSearchCV(estimator = XGB, 
                    param_grid = xgb_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4)

gsXGB.fit(train, target)

XGB_best = gsXGB.best_estimator_

print(GBC_best.get_params())

gsXGB.best_score_

"""## **Ensemble Modelling**"""

test.head()

test_survived_LR = pd.Series(lr_best.predict(test), name = 'LR')
test_survived_RFC = pd.Series(rfc_best.predict(test), name = 'RFC')
test_survived_XGB = pd.Series(XGB_best.predict(test), name = 'XGB')
test_survived_GBC = pd.Series(GBC_best.predict(test), name ='GBC')

print('test score LR:', grid_res.best_score_)
print('test score RFC:', grid_res_rfc.best_score_)
print('test score GBC:', gsGBC.best_score_)
print('test score XGB:', gsXGB.best_score_)

ensemble_results = pd.concat([test_survived_LR,test_survived_GBC, test_survived_XGB, test_survived_RFC],axis=1)


g= sns.heatmap(ensemble_results.corr(),annot=True)

VotingC = VotingClassifier(estimators=[('LR', lr_best), 
('GBC', GBC_best), ('XGB',XGB_best), ("RandomForest",rfc_best)], voting = 'soft', n_jobs =4)
VotingC.fit(train , target)

"""### Submission"""

test['Title']=test['Title'].replace('Mr',0.0)

test_Survived = pd.Series(VotingC.predict(test), name="Survived")
ids = pd.read_csv('../input/titanic/'+'test.csv')['PassengerId']

ids.head()

predictions = VotingC.predict(test)
output = pd.DataFrame({'PassengerId': ids, 'Survived': predictions})
output.to_csv('titanic_prediction.csv', index =False)
output.head()

