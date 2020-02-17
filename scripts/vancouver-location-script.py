#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd 
import math
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
vancover_data = pd.read_csv("../datasets/vancouver-data.csv") 
# Preview the first 5 lines of the loaded data 
vancover_data.head(5)


# In[5]:


# Drop uneeded columns from dataset
new_van_data = vancover_data.drop(['TYPE', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE'], axis=1)
new_van_data.head(5)


# In[6]:


# This is a function that converts a x,y into long and lat values and then returns it

def utmToLatLng(zone, easting, northing, northernHemisphere=True):
    if not northernHemisphere:
        northing = 10000000 - northing

    a = 6378137
    e = 0.081819191
    e1sq = 0.006739497
    k0 = 0.9996

    arc = northing / k0
    mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))

    ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))

    ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0

    cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
    cc = 151 * math.pow(ei, 3) / 96
    cd = 1097 * math.pow(ei, 4) / 512
    phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + cc * math.sin(6 * mu) + cd * math.sin(8 * mu)

    n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))

    r0 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
    fact1 = n0 * math.tan(phi1) / r0

    _a1 = 500000 - easting
    dd0 = _a1 / (n0 * k0)
    fact2 = dd0 * dd0 / 2

    t0 = math.pow(math.tan(phi1), 2)
    Q0 = e1sq * math.pow(math.cos(phi1), 2)
    fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24

    fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

    lof1 = _a1 / (n0 * k0)
    lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
    lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
    _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
    _a3 = _a2 * 180 / math.pi

    latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi

    if not northernHemisphere:
        latitude = -latitude

    longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

    return (latitude, longitude)


# In[7]:


# Number of rows in the dataset
print(new_van_data.shape[0])


# In[9]:


# Here we are sending all our x,y to get a list of corresponding lat and long
latitudes = []
longitudes = []
#longitude is the first result and latitude is the second
for i in range(0, len(new_van_data['Y'].values), 1000):
    latits = new_van_data['X'].values[i:i+1000]
    longits = new_van_data['Y'].values[i:i+1000]
    for x, y in zip(latits, longits):
        result = utmToLatLng(10, x, y)
        latitudes.append(result[0])
        longitudes.append(result[1])    
print(len(longitudes))


# In[10]:


# We set our long and lat values in our dataset
new_van_data['longitude'] = longitudes
new_van_data['latitude'] = latitudes
new_van_data.head(5)


# In[11]:


cols = new_van_data.columns.tolist()
print(cols)


# In[12]:


# We get rid of X,Y columns
new_cols = [cols[0], cols[1], cols[4], cols[5]]
new_data = new_van_data[new_cols]
new_data.head(5)


# In[13]:


# Renaming the columns here
data = new_data.rename(columns={"HUNDRED_BLOCK": "location_name", "NEIGHBOURHOOD": "neighborhood"}, errors="raise")
data.head(5)


# In[14]:


print('Total number of rows, including duplicates:', data.shape[0])


# In[15]:


# Dropping our duplicate location_name rows here
data.drop_duplicates(subset ="location_name", inplace = True) 
print('Total number of rows, without duplicates:',data.shape[0])


# In[16]:


data.head(5)


# In[17]:


# Here we are adding vancouver to city for the entire dataset
data['city'] = ['Vancouver' for i in range(data.shape[0])]
data.head(5)


# In[18]:


# Create a unique id per row in the database for location_key
import uuid
location_key = []
for i in range(data.shape[0]):
    id = uuid.uuid4() 
    location_key.append(id)
print(len(location_key))


# In[19]:


# Add location_key into dataframe
data['location_key'] = location_key
data.head(5)


# In[20]:


cols = data.columns.tolist()
print(cols)


# In[21]:


# Here we shift the order of the columns so it goes id, name, neighborhood, city, long, lat - to match sql table.
new_cols = [cols[5], cols[0], cols[1], cols[4], cols[2], cols[3]]
data = data[new_cols]
data.head(5)


# In[22]:


# Finally here we convert the dataframe to a csv file to store in our repo
vancouver_address_csv = data.to_csv(r'./vancouver-address.csv', index = None, header=True)

