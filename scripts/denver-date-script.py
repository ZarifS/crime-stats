#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
denver_data = pd.read_csv("../datasets/denver-data.csv") 
# Preview the first 5 lines of the loaded data 
denver_data.head(5)


# In[2]:


# Drop uneeded columns from dataset
data = denver_data.drop(['INCIDENT_ID', 'OFFENSE_ID', 'OFFENSE_CODE', 
                                    'OFFENSE_CODE_EXTENSION', 'OFFENSE_TYPE_ID',
                                    'OFFENSE_CATEGORY_ID', 'REPORTED_DATE',
                                    'GEO_X', 'GEO_Y', 'DISTRICT_ID', 'LAST_OCCURRENCE_DATE',
                                    'PRECINCT_ID', 'IS_CRIME', 'IS_TRAFFIC', 'GEO_LON',
                                    'GEO_LAT', 'NEIGHBORHOOD_ID', 'INCIDENT_ADDRESS'], axis=1)
data.head(5)


# In[3]:


# Splitting up date into Year, Month, Day, dataset has Month/Day/Year
date_values = data['FIRST_OCCURRENCE_DATE'].values

year = []
month = []
day = []
completeDay = []

for date in date_values:
    date = date.split() # Split on whitespace
    date = date[0] # Grab first portion which m/d/y
    completeDay.append(date)# Store the complete day to remove duplicates later
    date = date.split('/') # Split into m, d and y and turn into int
    month.append(int(date[0]))
    day.append(int(date[1]))
    year.append(int(date[2]))

data['year'] = year
data['month'] = month
data['day'] = day
data['completeDate'] = completeDay
data.head(5)


# In[4]:


print('Total number of rows, including duplicates:', data.shape[0])


# In[5]:


# Dropping our duplicate location_name rows here
data.drop_duplicates(subset ="completeDate", inplace = True) 
print('Total number of rows, without duplicates:', data.shape[0])


# In[6]:


data.head(5)


# In[7]:


# Drop uneeded columns again
data = data.drop(['FIRST_OCCURRENCE_DATE', 'completeDate'], axis=1)
data.head(5)


# In[8]:


#trying to get the day of the week attribute
import datetime
calender = { 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday' }
days = data['day'].values
months = data['month'].values
years = data['year'].values
days_of_the_week = []
for day, month, year in zip(days, months, years):
    day_of_week = calender[datetime.date(year, month, day).weekday()]
    days_of_the_week.append(day_of_week)


# In[9]:


#adding day_of_the_week attribute to the data frame
data['day_of_week'] = days_of_the_week
data.head(5)


# In[10]:


#adding weekend attribute to dataframe
is_weekend = []
for day in days_of_the_week:
    if day == 'Saturday' or day == 'Sunday':
        is_weekend.append(True)
    else:
        is_weekend.append(False)
data['is_weekend'] = is_weekend
data.head(5)


# In[ ]:


#install the holidays needed; this library is included in requirements.txt


# In[11]:


#setting up the holidays dictionary for colorado across the appropriate dates
import holidays
min_year_of_ds = data['year'].min()
max_year_of_ds = data['year'].max()
year_interval = [i for i in range(min_year_of_ds, max_year_of_ds+1, 1)]
co_holidays = holidays.US(years=year_interval, state='CO')


# In[13]:


#working on the is-holiday attribute and holiday_name attribute
is_holiday = []
holiday_name = []
for day, month, year in zip(days, months, years):
    is_holiday.append(datetime.date(year, month, day) in co_holidays)
    if datetime.date(year, month, day) in co_holidays:
        holiday_name.append(co_holidays[datetime.date(year, month, day)])
    else:
        holiday_name.append(None)
data['is_holiday'] = is_holiday
data['holiday_name'] = holiday_name
data.head(5)


# In[14]:


#add date_key
import uuid
date_keys = []
for i in range(data.shape[0]):
    id = uuid.uuid4() 
    date_keys.append(id)

data['date_key'] = date_keys
data.head(5)


# In[15]:


#rearrange columns of the dataframe
cols = data.columns.tolist()
new_cols = [cols[7]]
new_cols = new_cols + cols[0:7]
data = data[new_cols]
data.head()


# In[16]:


# Finally here we convert the dataframe to a csv file to store in our repo
denver_date_csv = data.to_csv(r'./denver-date.csv', index = None, header=True)


# In[ ]:


# End

