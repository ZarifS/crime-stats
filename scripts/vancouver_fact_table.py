#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
vancouver_data = pd.read_csv("./vancouver-parent_data.csv")
print(vancouver_data.shape[0])


# In[2]:


vancouver_date_data = pd.read_csv("./vancouver-date.csv")
print(vancouver_date_data.shape[0])

vancouver_address_data = pd.read_csv("./vancouver-address.csv")
print(vancouver_address_data.shape[0])

vancouver_crime_data = pd.read_csv("./vancouver-crime.csv")
print(vancouver_crime_data.shape[0])


# vancouver_date_data.head()


# In[3]:


vancouver_data.head(5)


# In[4]:


vancouver_date_data.head(5)


# In[5]:


#SAMPLE TEST
# sample_van_data = vancouver_data.iloc[0:5]
# sample_date_data = vancouver_date_data.iloc[0:5]
# new_van_data_sample = pd.merge(sample_van_data, sample_date_data, how='left', left_on=['YEAR','MONTH', 'DAY'], right_on = ['year','month', 'day'])
# new_van_data_sample.head()


# In[6]:


#MERGING VAN_DATA W/ VAN_DATE_DATA
new_van_data = pd.merge(vancouver_data, vancouver_date_data, how='left', left_on=['YEAR','MONTH', 'DAY'], right_on = ['year','month', 'day'])


# In[7]:


#TEST
# new_van_data.loc[(new_van_data['YEAR'] == 2019) & (new_van_data['MONTH'] == 5) & (new_van_data['DAY'] == 5)]


# In[8]:


new_van_data.head()

new_van_data = new_van_data.iloc[:, :11]
new_van_data.head()


# In[9]:


#Adding Address Key
new_van_data = pd.concat([new_van_data, vancouver_address_data], axis=1)
new_van_data.head()


# In[10]:


new_van_data = new_van_data.iloc[:, :12]
new_van_data.head()


# In[11]:


new_van_data = pd.concat([new_van_data, vancouver_crime_data], axis=1)


# In[12]:


new_van_data = new_van_data.iloc[:, :13]
new_van_data.head()


# In[13]:


#Adding the is_nighttime column
#used this link for reference as to what was day and what was night: https://www.englishclub.com/vocabulary/time-day-night.htm
def is_nighttime(row):
    if row['HOUR'] >= 18 or row['HOUR'] <= 6:
        return 1
    else:
        return 0

new_van_data['is_nighttime'] = new_van_data.apply (lambda row: is_nighttime(row), axis=1)

new_van_data.head()


# In[14]:


# Output the types of crimes in dataset
new_van_data.TYPE.unique()


# In[15]:


# Add a new column for is_traffic and is_fatal
is_fatal = []
is_traffic = []
for crime_type in new_van_data['TYPE']:
    if crime_type == 'Homicide' or crime_type == 'Vehicle Collision or Pedestrian Struck (with Fatality)':
        is_fatal.append(1)
    else: is_fatal.append(0)
    if crime_type == 'Vehicle Collision or Pedestrian Struck (with Fatality)' or crime_type == 'Vehicle Collision or Pedestrian Struck (with Injury)':
        is_traffic.append(1)
    else: is_traffic.append(0)

new_van_data['is_fatal'] = is_fatal
new_van_data['is_traffic'] = is_traffic


# In[16]:


new_van_data.head(5)


# In[17]:


# Drop all uneeded columns
new_van_data = new_van_data.drop(['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'HUNDRED_BLOCK', 'NEIGHBOURHOOD', 'X', 'Y', 'TYPE'], axis=1)
new_van_data.head(5)


# In[19]:


new_van_data.to_csv('./vancouver_fact_table.csv', index=False)

