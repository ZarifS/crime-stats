#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd 
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
denver_data = pd.read_csv("../datasets/denver-data.csv") 
# Preview the first 5 lines of the loaded data 
denver_data.head(5)


# In[3]:


# Drop uneeded columns from dataset
new_denver_data = denver_data.drop(['INCIDENT_ID', 'OFFENSE_ID', 'OFFENSE_CODE', 
                                    'OFFENSE_CODE_EXTENSION', 'OFFENSE_TYPE_ID',
                                    'OFFENSE_CATEGORY_ID', 'FIRST_OCCURRENCE_DATE',
                                    'LAST_OCCURRENCE_DATE', 'REPORTED_DATE',
                                    'GEO_X', 'GEO_Y', 'DISTRICT_ID',
                                    'PRECINCT_ID', 'IS_CRIME', 'IS_TRAFFIC'
                                   ], axis=1)
new_denver_data.head(5)


# In[18]:


# Renaming the columns here
data = new_denver_data.rename(columns={"INCIDENT_ADDRESS": "location_name", "NEIGHBORHOOD_ID": "neighborhood",
                                      "GEO_LON": "longitude", "GEO_LAT": "latitude"}, errors="raise")
data.head(20)


# In[19]:


print('Total number of rows, including duplicates:', data.shape[0])


# In[20]:


# Dropping our duplicate location_name rows here
data.drop_duplicates(subset ="location_name", inplace = True) 
print('Total number of rows, without duplicates:', data.shape[0])


# In[21]:


data.head(5)


# In[23]:


# Here we are adding Denver to city for the entire dataset
data['city'] = ['Denver' for i in range(data.shape[0])]
data.head(5)


# In[25]:


# Create a unique id per row in the database for location_key
import uuid
location_key = []
for i in range(data.shape[0]):
    id = uuid.uuid4() 
    location_key.append(id)
print(len(location_key))


# In[27]:


# Add location_key into dataframe
data['location_key'] = location_key
data.head(5)


# In[28]:


cols = data.columns.tolist()
print(cols)


# In[29]:


# Here we shift the order of the columns so it goes id, name, neighborhood, city, long, lat - to match sql table.
new_cols = [cols[5], cols[0], cols[3], cols[4], cols[1], cols[2]]
data = data[new_cols]
data.head(5)


# In[30]:


# Finally here we convert the dataframe to a csv file to store in our repo
denver_address_csv = data.to_csv(r'./denver-address.csv', index = None, header=True)

