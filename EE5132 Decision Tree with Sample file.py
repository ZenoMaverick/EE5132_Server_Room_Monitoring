#!/usr/bin/env python
# coding: utf-8

# Import libraries

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split


# Import csv file

# In[2]:


df = pd.read_csv("Sample_Dataset.csv")


# In[3]:


df.head(10) #Show top 10 values from the top


# In[4]:


df.isnull().any() #Check for any null values in dataset


# In[5]:


df.dtypes #Check the variable types for our variables


# In[6]:


df.describe()


# Everything checks out. But temperature seems to have a minimum value of 0.0

# In[7]:


df['temperature'].plot.hist()


# Plotting a histogram for temperature, most of the values are above 25 degree celcius and 0 appears less frequently.

# In[8]:


X = df.iloc[:, :4] #Features
X


# In[9]:


Y = df.iloc[:, 4:] #Labels
Y


# Separated the features and labels from the dataframe. Now we can split the training and test sets.

# In[10]:


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size = 0.7)


# In[11]:


from sklearn.svm import SVC


# In[12]:


clf = SVC(C=1e4, kernel='rbf', random_state=100, gamma='scale',probability=True)
clf.fit(X_train, Y_train)
clf.score(X_test, Y_test)


# In[13]:


from sklearn.tree import DecisionTreeClassifier
from sklearn import tree


# In[14]:


clf2 = DecisionTreeClassifier()
clf2.fit(X_train, Y_train)
clf2.score(X_train, Y_train)


# In[15]:


tree.plot_tree(clf2)


# In[16]:


Example = [[300, 200, 27.0, 80.0]] #Dim
Example1 = [[500, 500, 24.0, 60.0]] #Normal
Example2 = [[100, 800, 22.0, 70.0]] #Bright


# In[17]:


def classifier (Data):
    Label = clf2.predict(Data)
    Label = Label[0] #Used this to get the int value from the 1D list
    Dict = {0: 'Dim', 1: 'Normal', 2: 'Bright'}
    Class = Dict.get(Label)
    print(Label, Class)


# In[18]:


classifier(Example)
classifier(Example1)
classifier(Example2)

