#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
vancouver_data = pd.read_csv("../datasets/vancouver-data.csv") 
# Preview the first 5 lines of the loaded data 
vancouver_data.head(5)


# In[2]:


# Drop uneeded columns from dataset
vancouver_data = vancouver_data.drop(['TYPE', 'HUNDRED_BLOCK', 'NEIGHBOURHOOD', 'X', 'Y', 'HOUR', 'MINUTE'], axis=1)
vancouver_data.head(5)


# In[3]:


#trying to get the day of the week attribute
import datetime
calender = { 0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday' }
days = vancouver_data['DAY'].values
months = vancouver_data['MONTH'].values
years = vancouver_data['YEAR'].values
days_of_the_week = []
for day, month, year in zip(days, months, years):
    day_of_week = calender[datetime.date(year, month, day).weekday()]
    days_of_the_week.append(day_of_week)
    


# In[4]:


#adding day_of_the_week attribute to the data frame
vancouver_data['day_of_week'] = days_of_the_week
vancouver_data.head()


# In[5]:


#adding weekend attribute to dataframe
is_weekend = []
for day in days_of_the_week:
    if day == 'Saturday' or day == 'Sunday':
        is_weekend.append(True)
    else:
        is_weekend.append(False)
vancouver_data['is_weekend'] = is_weekend
vancouver_data.head(5)


# In[6]:


#install the holidays needed; this library is included in requirements.txt


# In[7]:


#setting up the holidays dictionary for british columbia across the appropriate dates
import holidays
min_year_of_ds = vancouver_data['YEAR'].min()
max_year_of_ds = vancouver_data['YEAR'].max()
year_interval = [i for i in range(min_year_of_ds, max_year_of_ds+1, 1)]
bc_holidays = holidays.Canada(years=year_interval, prov='BC')


# In[8]:


#working on the is-holiday attribute and holiday_name attribute
is_holiday = []
holiday_name = []
for day, month, year in zip(days, months, years):
    is_holiday.append(datetime.date(year, month, day) in bc_holidays)
    if datetime.date(year, month, day) in bc_holidays:
        holiday_name.append(bc_holidays[datetime.date(year, month, day)])
    else:
        holiday_name.append(None)
vancouver_data['is_holiday'] = is_holiday
vancouver_data['holiday_name'] = holiday_name


# In[9]:


vancouver_data.head(15)


# In[10]:


#making sure dataframe column titles are all of the same heading
vancouver_data = vancouver_data.rename(columns={"MONTH": "month", "DAY": "day", "YEAR": "year"}, errors="raise")
vancouver_data.head(10)


# In[11]:


#add date_key
import uuid
date_keys = []
for i in range(vancouver_data.shape[0]):
    id = uuid.uuid4() 
    date_keys.append(id)

vancouver_data['date_key'] = date_keys


# In[12]:


#rearrange columns of the dataframe
cols = vancouver_data.columns.tolist()
new_cols = [cols[7]]
new_cols = new_cols + cols[0:7]
vancouver_data = vancouver_data[new_cols]
vancouver_data.head()


# In[13]:


# Finally here we convert the dataframe to a csv file to store in our repo
vancouver_date_csv = vancouver_data.to_csv(r'./vancouver-date.csv', index = None, header=True)


# In[ ]:


# End

