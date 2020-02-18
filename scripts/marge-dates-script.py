#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd 
denver_data = pd.read_csv("../denver-datasets/denver-date.csv") 
vancouver_data = pd.read_csv("../vancouver-datasets/vancouver-date.csv")


# In[3]:


denver_data.head(5)


# In[5]:


vancouver_data.head(5)


# In[6]:


denver_data = denver_data.rename(columns={"is_holiday": "is_american_holiday", "holiday_name": "american_holiday_name"}, errors="raise")
denver_data.head(5)


# In[7]:


vancouver_data = vancouver_data.rename(columns={"is_holiday": "is_canadian_holiday", "holiday_name": "canadian_holiday_name"}, errors="raise")
vancouver_data.head()


# In[8]:


# This merges the two datasets together
result = pd.merge(denver_data, vancouver_data, on=['year', 'month', 'day', 'day_of_week', 'is_weekend'])
result = result.drop(['date_key_x', 'date_key_y'], axis=1)
result.head()


# In[9]:


#add date_key
import uuid
date_keys = []
for i in range(result.shape[0]):
    id = uuid.uuid4() 
    date_keys.append(id)

result['date_key'] = date_keys

result.head()


# In[10]:


# Shift date_key to the first column
cols = result.columns.tolist()
newcols = [cols[9]] + cols[0:9]
result = result[newcols]
print(cols)


# In[10]:


result.head()


# In[11]:


print('Total number of rows with duplicates:', result.shape[0])


# In[13]:


result.drop_duplicates(subset=["year", "month","day"], inplace=True)
result.head()


# In[14]:


print('Total number of rows without duplicates:', result.shape[0])


# In[15]:


# Transfer data to csv file
result.to_csv(r'./merged-dates.csv', index = None, header=True)

