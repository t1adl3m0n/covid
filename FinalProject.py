
# coding: utf-8

# # Final Project
# 
# 
# For your final project, you will build a classifer for
# the **Backorder Prediction** dataset by following our
# operationalized machine learning pipeline.
# 
# ![AppliedML_Workflow IMAGE MISSING](../images/AppliedML_Workflow.png)
# 

# --- 
# 
# ## Data
# 
# Details of the dataset are located here:
# 
# Dataset (originally posted on Kaggle): https://www.kaggle.com/tiredgeek/predict-bo-trial
# 
# The files are accessible in the JupyterHub environment:
#  * `/dsa/data/all_datasets/back_order/Kaggle_Training_Dataset_v2.csv`
#  * `/dsa/data/all_datasets/back_order/Kaggle_Test_Dataset_v2.csv`
# 
# The data is used to predict of product when on Back Order.
#  
# **NOTE:** The training data file is 117MB.  
# <span style="background:yellow">You can easily **lock up a notebook** with bad coding practices.</span>  
# Please save you project early, and often, and use `git commits` to checkpoint your process.

# ## Exploration, Training, and Validation
# 
# You will examine the _training_ dataset and perform 
#  * **data preparation and exploratory data analysis**, 
#  * **anomaly detection / removal**,
#  * **dimensionality reduction** and then
#  * **train and validate 3 different models**.
# 
# Of the 3 different models, you are free to pick any estimator from scikit-learn 
# or models we have so far covered using TensorFlow.
# 
# ### Validation Assessment
# 
# Your first, intermediate, result will be an **assessment** of the models' performance.
# This assessement should be grounded within a 10-fold cross-validation methodology.
# 
# This should include the confusion matrix and F-score for each classifier.
# 

# ---
# 
# ## Testing
# 
# Once you have chosen your final model, you will need to re-train it using all the training data.
# 
# 
# --- 
# ##  Overview / Roadmap
# 
# **General steps**:
# 
# * Dataset carpentry & Exploratory Data Analysis
#   * Develop functions to perform the necessary steps, you will have to carpentry the Training and the Testing data.
# * Create 3 pipelines, each does:
#     * Anomaly detection
#     * Dimensionality reduction
#     * Model training/validation
# * Train chosen model full training data
# * Evaluate model against testing
# * Write a summary of your processing and an analysis of the model performance
# 
# 
# #### <span style="background:yellow">Note:</span> The use of sklearn Pipelines and FeatureUnion is optional.   Pipelines are strongly recommended!
# However, your three models should follow a readable path from data to cross-validation statistics.

# In[1]:


get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt

import os, sys
import itertools
import numpy as np
import pandas as pd


# ## Load dataset
# 
# **Description**
# ~~~
# sku - Random ID for the product
# national_inv - Current inventory level for the part
# lead_time - Transit time for product (if available)
# in_transit_qty - Amount of product in transit from source
# forecast_3_month - Forecast sales for the next 3 months
# forecast_6_month - Forecast sales for the next 6 months
# forecast_9_month - Forecast sales for the next 9 months
# sales_1_month - Sales quantity for the prior 1 month time period
# sales_3_month - Sales quantity for the prior 3 month time period
# sales_6_month - Sales quantity for the prior 6 month time period
# sales_9_month - Sales quantity for the prior 9 month time period
# min_bank - Minimum recommend amount to stock
# potential_issue - Source issue for part identified
# pieces_past_due - Parts overdue from source
# perf_6_month_avg - Source performance for prior 6 month period
# perf_12_month_avg - Source performance for prior 12 month period
# local_bo_qty - Amount of stock orders overdue
# deck_risk - Part risk flag
# oe_constraint - Part risk flag
# ppap_risk - Part risk flag
# stop_auto_buy - Part risk flag
# rev_stop - Part risk flag
# went_on_backorder - Product actually went on backorder. **This is the target value.**
# ~~~
# 
# **Note**: This is a real-world dataset without any processing.  
# There will also be warnings due to fact that the 1st column is mixing integer and string values.  
# The last column is what we are trying to predict.

# In[2]:


# Dataset location
DATASET = '/dsa/data/all_datasets/back_order/Kaggle_Training_Dataset_v2.csv'
assert os.path.exists(DATASET)

# Load and shuffle
dataset = pd.read_csv(DATASET).sample(frac = 1).reset_index(drop=True)
dataset.describe()


# ## Processing
# 
# In this section, goal is to figure out:
# 
# * which columns we can use directly,  
# * which columns are usable after some processing,  
# * and which columns are not processable or obviously irrelevant (like product id) that we will discard.
# 
# Then process and prepare this dataset for creating a predictive model.

# In[3]:


dataset.info()


# ### Take samples and examine the dataset

# In[ ]:


dataset.iloc[:3]


# In[ ]:


dataset.iloc[:3,6:12]


# In[ ]:


dataset.iloc[:3,12:18]


# In[ ]:


dataset.iloc[:3,18:24]


# ### Drop columns that are obviously irrelevant or not processable

# In[5]:


# Add code below this comment  (Question #E8001)
# ---------------------------------- 
dataset.drop(['sku', 'sales_3_month', 'sales_6_month', 'sales_9_month',
       'min_bank' ], axis=1, inplace = True)
dataset.head()


# ### Find unique values of string columns
# 
# Now try to make sure that these Yes/No columns really only contains Yes or No.  
# If that's true, proceed to convert them into binaries (0s and 1s).
# 
# **Tip**: use [unique()](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.unique.html) function of pandas Series.
# 
# Example
# 
# ~~~python
# print('went_on_backorder', dataset['went_on_backorder'].unique())
# ~~~

# In[6]:


# All the column names of these yes/no columns
yes_no_columns = list(filter(lambda i: dataset[i].dtype!=np.float64, dataset.columns))
print(yes_no_columns)

# Add code below this comment  (Question #E8002)
# ----------------------------------
for column_name in yes_no_columns:
    mode = dataset[column_name].apply(str).mode()[0]
    print('Filling missing values of {} with {}'.format(column_name, mode))
    dataset[column_name].fillna(mode, inplace=True)


# You may see **nan** also as possible values representing missing values in the dataset.
# 
# We fill them using most popular values, the [Mode](https://en.wikipedia.org/wiki/Mode_%28statistics%29) in Stats.

# In[7]:


for column_name in dataset.columns:
    mode = dataset[column_name].apply(str).mode()[0]
    print('Filling missing values of {} with {}'.format(column_name, mode))
    dataset[column_name].fillna(mode, inplace=True)


# ### Convert yes/no columns into binary (0s and 1s)

# In[8]:


# Add code below this comment  (Question #E8003)
# ----------------------------------
for column_name in yes_no_columns:
    dataset[column_name] = dataset[column_name].apply(['Yes', 'No'].index)


# Now all columns should be either int64 or float64.

# ## Pipeline
# 
# In this section, design an operationalized machine learning pipeline, which includes:
# 
# * Anomaly detection
# * Dimensionality Reduction
# * Train a model
# 
# You can add more notebook cells or import any Python modules as needed.

# In[9]:


from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest

from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, chi2, f_classif, mutual_info_classif

from sklearn.pipeline import Pipeline, FeatureUnion

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix


# In[10]:


dataset.astype('float64').dtypes     


# In[11]:


X0 = np.array(dataset[dataset.went_on_backorder == 0].iloc[:,:-1].sample(n=np.sum(dataset.went_on_backorder == 0)))
X1 = np.array(dataset[dataset.went_on_backorder == 1].iloc[:,:-1].sample(n=np.sum(dataset.went_on_backorder == 1)))
X = np.vstack([X0, X1])
y = np.concatenate([np.zeros(len(X0)), np.ones(len(X1))])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print(X.shape, y.shape)


# ### Your 1st pipeline 
#   * Anomaly detection
#   * Dimensionality reduction
#   * Model training/validation

# ### Your 2nd pipeline
#   * Anomaly detection
#   * Dimensionality reduction
#   * Model training/validation

# ### Your 3rd pipeline
#   * Anomaly detection
#   * Dimensionality reduction
#   * Model training/validation

# In[ ]:



pipe_scale_pca_rf = Pipeline([
    ('scl', StandardScaler()),
    ('pca', PCA()),
    ('clf', RandomForestClassifier())])

pipe_scale_fa_rf = Pipeline([
    ('scl', StandardScaler()),
    ('fa', FactorAnalysis()),
    ('clf', RandomForestClassifier())])

pipe_scale_pca_svm = Pipeline([
    ('scl', StandardScaler()),
    ('pca', PCA()),
    ('clf', SVC())])

pipe_scale_fa_svm = Pipeline([
    ('scl', StandardScaler()),
    ('fa', FactorAnalysis()),
    ('clf', SVC())])

pipe_rf = Pipeline([('clf', RandomForestClassifier())])
    
param_range = [3,6,9]
estimators_range = [5, 25, 50]

grid_params_pca_rf = [{'pca__n_components': param_range,
                   'clf__criterion': ['gini', 'entropy'],
                   'clf__n_estimators': estimators_range,
                   'clf__max_depth': estimators_range}]

grid_params_fa_rf = [{'fa__n_components': param_range,
                   'clf__criterion': ['gini', 'entropy'],
                   'clf__n_estimators': estimators_range,
                   'clf__max_depth': estimators_range}]

grid_params_rf = [{'clf__criterion': ['gini', 'entropy'],
                   'clf__n_estimators': estimators_range,
                   'clf__max_depth': estimators_range}]

grid_params_pca_svm = [{'pca__n_components': param_range,
                    'clf__kernel': ['linear', 'rbf'], 
                    'clf__C': param_range}]

grid_params_fa_svm = [{'fa__n_components': param_range,
                    'clf__kernel': ['linear', 'rbf'], 
                    'clf__C': param_range}]

jobs = -1

gs_pca_rf = GridSearchCV(estimator=pipe_scale_pca_rf,
                            param_grid=grid_params_pca_rf,
                            scoring='recall',
                            cv=5, 
                            n_jobs=jobs)

gs_fa_rf = GridSearchCV(estimator=pipe_scale_fa_rf,
                            param_grid=grid_params_fa_rf,
                            scoring='recall',
                            cv=5, 
                            n_jobs=jobs)

gs_pca_svm = GridSearchCV(estimator=pipe_scale_pca_svm,
                            param_grid=grid_params_pca_svm,
                            scoring='recall',
                            cv=5,
                            n_jobs=jobs)

gs_fa_svm = GridSearchCV(estimator=pipe_scale_fa_svm,
                            param_grid=grid_params_fa_svm,
                            scoring='recall',
                            cv=5,
                            n_jobs=jobs)

gs_rf = GridSearchCV(estimator=pipe_rf,
                            param_grid=grid_params_rf,
                            scoring='recall',
                            cv=5, 
                            n_jobs=jobs)

grids = [gs_pca_rf, gs_fa_rf, gs_pca_svm, gs_fa_svm, gs_rf]

grid_dict = {0: 'RF w/PCA', 1: 'RF w/FA', 2: 'SVM w/PCA', 3: 'SVM w/FA', 4: 'RF Only'}

print('Performing model optimizations...')
best_acc = 0.0
best_clf = 0
best_gs = ''
for idx, gs in enumerate(grids):
    print('\nEstimator: %s' % grid_dict[idx])	
    # Fit grid search	
    gs.fit(X_train, y_train)
    # Best params
    print('Best params: %s' % gs.best_params_)
    # Best training data accuracy
    print('Best training accuracy: %.3f' % gs.best_score_)
    # Predict on test data with best params
    y_pred = gs.predict(X_test)
    # Test data accuracy of model with best params
    print('Test set accuracy score for best params: %.3f ' % accuracy_score(y_test, y_pred))
    # Track best (highest test accuracy) model
    if accuracy_score(y_test, y_pred) > best_acc:
        best_acc = accuracy_score(y_test, y_pred)
        best_gs = gs
        best_clf = idx
print('\nClassifier with best test set accuracy: %s' % grid_dict[best_clf])


# ## Document the cross-validation analysis for the three models

# In[ ]:





# **<span style="background:yellow">Don't forget to share your chosen models and their cross-validation performance with the class on the dicussion board for module 8.</span>** 
# 
# ---
# 
# # Retrain a model using the full training data set
# 
# ## Train
# Use the full training data set to train the model.

# In[ ]:


# Add code below this comment  (Question #E8008)
# ----------------------------------
















# ### Save the trained model with the pickle library.

# In[ ]:


# Add code below this comment  (Question #E8009)
# ----------------------------------






# ### Reload the trained model from the pickle file
# ### Load the Testing Data and evaluate your model
# 
#  * `/dsa/data/all_datasets/back_order/Kaggle_Test_Dataset_v2.csv`

# In[ ]:


# Add code below this comment  (Question #E8010)
# ----------------------------------







# ## Test
# Test your new model using the testing data set.
#  * `/dsa/data/all_datasets/back_order/Kaggle_Test_Dataset_v2.csv`

# In[ ]:


from sklearn.metrics import accuracy_score, confusion_matrix

# Add code below this comment  (Question #E8011)
# ----------------------------------
















# ## Conclusion
# Write a summary of your processing and an analysis of the model performance  
# (Question #E8012)
# ----------------------------------















# ## Reflect
# 
# Imagine you are data scientist that has been tasked with developing a system to save your 
# company money by predicting and preventing back orders of parts in the supply chain.
# 
# Write a **brief summary** for "management" that details your findings, 
# your level of certainty and trust in the models, 
# and recommendations for operationalizing these models for the business.
# Write your answer here:  
# (Question #E8013)
# ----------------------------------















# # Save your notebook!
# ## Then `File > Close and Halt`
