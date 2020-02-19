#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
denver_data = pd.read_csv("../datasets/denver-data.csv") 


# In[2]:


# Preview the first 5 lines of the loaded data 
denver_data.head(5)


# In[11]:


# Drop uneeded columns from dataset
data = denver_data.drop(['INCIDENT_ID', 'OFFENSE_ID', 'OFFENSE_CODE', 
                                    'OFFENSE_CODE_EXTENSION', 'OFFENSE_TYPE_ID',
                                     'GEO_X', 'GEO_Y', 'DISTRICT_ID',
                                    'PRECINCT_ID', 'IS_CRIME', 'IS_TRAFFIC', 'GEO_LON',
                                    'GEO_LAT', 'NEIGHBORHOOD_ID', 'INCIDENT_ADDRESS'], axis=1)
data.head(5)


# In[12]:


# Here we create a map to turn denver and vancouver crime granularity into the same level
# We basically map denvers more rich data into buckets that work for vancouver as well
crime_category_dict = {
                       'Break and Enter Commercial': 'Burglary',
                       'Break and Enter Residential/Other': 'Burglary',
                       'Homicide': 'Homicide',
                       'Mischief': 'Mischief',
                       'Offence Against a Person': 'Offence Against a Person',
                       'Other Theft': 'Theft',
                       'Theft from Vehicle': 'Theft from Vehicle',
                       'Theft of Bicycle': 'Theft', #assumptions: bicycles are not expensive enough
                       'Theft of Vehicle': 'Theft of Vehicle',
                       'Vehicle Collision or Pedestrian Struck (with Fatality)': 'Traffic Accident',
                       'Vehicle Collision or Pedestrian Struck (with Injury)': 'Traffic Accident',
                       'all-other-crimes': 'Other Crimes',
                       'larceny': 'Theft',
                       'theft-from-motor-vehicle': 'Theft from Vehicle',
                       'traffic-accident': 'Traffic Accident',
                       'drug-alcohol': 'Other Crimes', #Not sure about this one
                       'auto-theft': 'Theft of Vehicle',
                       'white-collar-crime': 'Other  Crimes', #ponzy scheme, wage fraud
                       'burglary': 'Burglary',
                       'public-disorder': 'Mischief',
                       'aggravated-assault': 'Offence Against a Person',
                       'other-crimes-against-persons': 'Offence Against a Person',
                       'robbery': 'Theft',
                       'sexual-assault': 'Offence Against a Person',
                       'murder': 'Homicide',
                       'arson': 'Mischief' #setting things on fire
                      }


# In[13]:


#add crime_key
import uuid
crime_keys = []
for i in range(data.shape[0]):
    id = uuid.uuid4() 
    crime_keys.append(id)

data['crime_key'] = crime_keys
data.head(5)


# In[14]:


# Map the crime type to the buckets we already came up with
new_type = []
for crime_type in data['OFFENSE_CATEGORY_ID'].values:
    new_type.append(crime_category_dict[crime_type])
data['crime_type'] = new_type
data.head(5)


# In[15]:


# Python program to convert time 
# from 12 hour to 24 hour format
# Source: https://www.geeksforgeeks.org/python-program-convert-time-12-hour-24-hour-format/
  
# Function to convert the date format 
def convert24(str1): 
      
    # Checking if last two elements of time 
    # is AM and first two elements are 12 
    if str1[-2:] == "AM" and str1[:2] == "12": 
        return "00" + str1[2:-2] 
          
    # remove the AM     
    elif str1[-2:] == "AM": 
        return str1[:-2] 
      
    # Checking if last two elements of time 
    # is PM and first two elements are 12    
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2] 
          
    else: 
          
        # add 12 to hours and remove PM 
        return str(int(str1[:2]) + 12) + str1[2:8] 


# In[16]:


data.head(10)


# In[17]:


# Here we turn the REPORTED_DATE into a normal timestamp - "HH:MM:SS" format.
# Splitting up date into Year, Month, Day, dataset has Month/Day/Year

date_values = data['REPORTED_DATE'].values

crime_report_times = []

for date in date_values:
    if date == '-':
        crime_report_times.append(None)
    else:
        date = date.split() # Split on whitespace -> we get [mm/dd/yy, hh:mm:ss, pm/am]
        # Add a extra 0 before any hours less than 10, so from 8:15 -> 08:15
        hours = date[1].split(':')
        if len(hours[0]) == 1:
            # Create the timestamp string
            timestamp = '0'+date[1] + ' ' + date[2]    
        else:
            timestamp = date[1] + ' ' + date[2] 

        # Convert into format
        timestamp = convert24(timestamp)
        crime_report_times.append(timestamp)
    
data['crime_report_time'] = crime_report_times


# In[10]:


data.head(5)


# In[18]:


# Here we turn the first_occurrence_date into a normal timestamp - "HH:MM:SS" format.
# Splitting up date into Year, Month, Day, dataset has Month/Day/Year
date_values = data['FIRST_OCCURRENCE_DATE'].values

crime_start_times = []

for date in date_values:
    date = date.split() # Split on whitespace -> we get [mm/dd/yy, hh:mm:ss, pm/am]
    
    # Add a extra 0 before any hours less than 10, so from 8:15 -> 08:15
    hours = date[1].split(':')
    if len(hours[0]) == 1:
        # Create the timestamp string
        timestamp = '0'+date[1] + ' ' + date[2]    
    else:
        timestamp = date[1] + ' ' + date[2] 
    
    # Convert into format
    timestamp = convert24(timestamp)
    crime_start_times.append(timestamp)
    
data['crime_start_time'] = crime_start_times


# In[19]:


data.head(10)


# In[21]:


# Replace all NaN values in the LAST_OCCURENCE_DATE column
data['LAST_OCCURRENCE_DATE'] = data['LAST_OCCURRENCE_DATE'].fillna('-')
data.head(5)


# In[22]:


# Here we turn the last_occurrence_date into a normal timestamp - "HH:MM:SS" format.
# Splitting up date into Year, Month, Day, dataset has Month/Day/Year

date_values = data['LAST_OCCURRENCE_DATE'].values

crime_end_times = []

for date in date_values:
    if date == '-':
        crime_end_times.append(None)
    else:
        date = date.split() # Split on whitespace -> we get [mm/dd/yy, hh:mm:ss, pm/am]
        # Add a extra 0 before any hours less than 10, so from 8:15 -> 08:15
        hours = date[1].split(':')
        if len(hours[0]) == 1:
            # Create the timestamp string
            timestamp = '0'+date[1] + ' ' + date[2]    
        else:
            timestamp = date[1] + ' ' + date[2] 

        # Convert into format
        timestamp = convert24(timestamp)
        crime_end_times.append(timestamp)
    
data['crime_end_time'] = crime_end_times


# In[23]:


data.head(5)


# In[ ]:


data.head(5)


# In[24]:


# Drop uneeded columns from dataset
data = data.drop(['OFFENSE_CATEGORY_ID', 'FIRST_OCCURRENCE_DATE', 'LAST_OCCURRENCE_DATE', 'REPORTED_DATE'], axis=1)
data.head(5)


# In[25]:


# Finally here we convert the dataframe to a csv file to store in our repo
denver_crime_csv = data.to_csv(r'./denver-crime.csv', index = None, header=True)


# In[ ]:


#End

