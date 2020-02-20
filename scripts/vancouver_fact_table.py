#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
vancouver_data = pd.read_csv("./vancouver-parent_data.csv")
print(vancouver_data.shape[0])


# In[14]:


merged_date_data = pd.read_csv("../merged-datasets/merged-dates.csv")
print(merged_date_data.shape[0])

vancouver_address_data = pd.read_csv("./vancouver-address.csv")
print(vancouver_address_data.shape[0])

vancouver_crime_data = pd.read_csv("./vancouver-crime.csv")
print(vancouver_crime_data.shape[0])


# vancouver_date_data.head()


# In[15]:


vancouver_data.head(5)


# In[16]:


merged_date_data.head(5)


# In[18]:


vancouver_address_data.head(5)


# In[19]:


vancouver_crime_data.head(5)


# In[21]:


#MERGING VAN_DATA W/ VAN_DATE_DATA
new_van_data = pd.merge(vancouver_data, merged_date_data, how='left', left_on=['HUNDRED_BLOCK'], right_on = ['location_name'])


# In[23]:


new_van_data.head(5)


# In[24]:


# Removing all the other merged-date columns and only keeping location_key
new_van_data = new_van_data.iloc[:, :11]
new_van_data.head()


# In[26]:


#Adding Date Key
new_van_data = pd.merge(new_van_data, merged_date_data, how='left', left_on=['YEAR','MONTH', 'DAY'], right_on = ['year','month', 'day'])
new_van_data.head(5)


# In[28]:


# Getting rid of extra date attribute
new_van_data = new_van_data.iloc[:, :12]
new_van_data.head()


# In[29]:


# Confirm size of dataset is still the same as crime-dataset
new_van_data.shape[0]


# In[30]:


# Since the order of the crime-dataset and original dataset are the same, we can just concat the crime-dim info
new_van_data = pd.concat([new_van_data, vancouver_crime_data], axis=1)


# In[31]:


# Remove extra crime info
new_van_data = new_van_data.iloc[:, :13]
new_van_data.head()


# In[32]:


#Adding the is_nighttime column
#used this link for reference as to what was day and what was night: https://www.englishclub.com/vocabulary/time-day-night.htm
def is_nighttime(row):
    if row['HOUR'] >= 18 or row['HOUR'] <= 6:
        return 1
    else:
        return 0

new_van_data['is_nighttime'] = new_van_data.apply (lambda row: is_nighttime(row), axis=1)

new_van_data.head()


# In[33]:


# Output the types of crimes in dataset
new_van_data.TYPE.unique()


# In[34]:


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


# In[35]:


new_van_data.head(5)


# In[36]:


# Drop all uneeded columns
new_van_data = new_van_data.drop(['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'HUNDRED_BLOCK', 'NEIGHBOURHOOD', 'X', 'Y', 'TYPE'], axis=1)
new_van_data.head(5)


# In[37]:


# Export to CSV
new_van_data.to_csv('./vancouver_fact_table.csv', index=False)


# In[ ]:


# End

