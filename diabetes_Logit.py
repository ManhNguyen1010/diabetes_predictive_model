#import releveant packages (required pre-loaded by cmd or anaconda)

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import statsmodels.api as sm
from torch.nn import functional as F
import torch
import warnings #to remove the warnings
warnings.filterwarnings('ignore')

#import and view the imported dataset
food = pd.read_csv(("../Downloads/diabetes.csv"))
print(food.head())

#Check for null entries(if any)
print("Null values (if any): ", food.isnull().values.any().sum())

#This dataset's variable values are in numerical format, so no conversion is needed
#Check whether the decision variable  is balanced  using seaborn category plot  

cat_plot = sns.catplot(x = "Diabetes_binary", data = food, kind = 'count', palette=sns.color_palette("RdBu", 10) )
cat_plot.set(xlabel = 'Diabetic?', ylabel = 'Number of People', xticklabels=['No', 'Yes'])
plt.show()

#Label the chosen  independent and dependent variables 
y = food['Diabetes_binary'] #Decision variable
x = food.drop(['Diabetes_binary'], axis=1)

#Divide the dataset into training and valid set 
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size= 0.2)


#use sklearn to implement logistic regression
modelLogistic = LogisticRegression()
modelLogistic.fit(x_train,y_train)

        
#print the regression coefficients
print("The intercept b0= ", modelLogistic.intercept_)

print("The coefficient b1= ", modelLogistic.coef_)


#Make prediction 
y_pred= modelLogistic.predict(x_test)

#Creating confusion matrix
ConfusionMatrix = confusion_matrix(y_test, y_pred)

#obtain True Positive, True Negative, False Positive and False Negative 
#print(classification_report(y_test, y_pred))

#Accuracy from confusion matrix
TP= ConfusionMatrix[1,1] #True positive
TN= ConfusionMatrix[0,0] #True negative
Total=len(y_test)
print("Accuracy from confusion matrix is ", (TN+TP)/Total)


#Confusion matrix plot with label settings
group_names = ['True Negative','False Positive','False Negative','True Positive']
group_counts = ['{0:0.0f}'.format(value) for value in ConfusionMatrix.flatten()]
group_percentages = ['{0:.2%}'.format(value) for value in ConfusionMatrix.flatten()/np.sum(ConfusionMatrix)]
labels = [f'{v1}\n{v2}\n{v3}' for v1, v2, v3 in zip(group_names,group_counts,group_percentages)]
labels = np.asarray(labels).reshape(2,2)
heat_map = sns.heatmap(ConfusionMatrix, annot=labels, fmt='', cmap= sns.color_palette("RdPu", 10))
heat_map.set_xlabel('Predicted')
heat_map.set_ylabel('Actual Values')
heat_map.tick_params(length=0, labeltop=True, labelbottom=False)
heat_map.xaxis.set_label_position('top')
heat_map.set_xticklabels(['Negative', 'Positive'])
heat_map.set_yticklabels(['Negative', 'Positive'], rotation=90, va='center')
plt.show()

#Using statsmodels package to obtian the model
x_train = sm.add_constant(x_train)
logit_model=sm.Logit(y_train,x_train)
result=logit_model.fit()
print(result.summary())


#Calculating Odds Ratios
odds_ratios = pd.DataFrame(
    {
        "Odd Ratios": result.params,
        "Lower CI": result.conf_int()[0],
        "Upper CI": result.conf_int()[1],
    }
)
odds_ratios = np.exp(odds_ratios)
print(odds_ratios)


