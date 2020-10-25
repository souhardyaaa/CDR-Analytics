# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 23:40:27 2020

@author: Souhardya
"""


# All imports for the project
import pandas as pd
import re
import numpy as np
import datetime
​
# All Function would be defined here
#  Function to seperate the date and time from column 9
def datetime_divider(data):
    for index in range (len(data)):
        if (re.match("^\d",str(data[index]))):
            regex = re.compile("\d{1,8}")
            a = regex.findall(str(data[index]))
            print(a)
            data[index ] = [ a[0] , a[1] ]
        else:
            data[index ] = [np.nan, np.nan]
    return data



# Function to convert the data in desired date format
def date_modifier(data):
    # data type of data is list
    # 20190620 should be converted to 2019-06-20
    for index in range(len(data)):
        if re.match("^\d", str(data[index])):
            year = str(data[index][:4])
            month = str(data[index][4:6])
            day = str(data[index][6:])
            data[index] = "-".join([year, month, day])
        else:
            data[index] =  np.nan 
    return data



# Function to convert the data in desired datetime format
def time_modifier(data):
    # Data type of data is list
    # 032717 should be converted into 03:27:17 AM
    for index in range(len(data)):
        data[index] = str(data[index])
        
        if re.match("^\d", data[index]):
            m = int(data[index][:2])
            mi = data[index][2:4]
            sec = data[index][4:]
            
            if m >=12:
                if m == 12:
                    hr = str(m)
                else:
                    hr = str(m-12)
                merd = "PM"
            else:
                if m == 0:
                    hr = str(12)
                else:
                    hr = data[index][:2]
                merd = "AM"
            
            data[index] = ":".join([hr, mi, sec]) + " " + merd
        else:
            data[index] = np.nan
    return data




def replace_simple_with_Standard_terminology(dataset):
    # This part replace the data with standard terminologies in col 5, 267, 312
    # Replacing String in the columns with standard Terminology
    dataset[5] = dataset[5].replace("Originating", "Outgoing")
    dataset[5] = dataset[5].replace("Terminating", "Incoming")
    dataset[267] = dataset[267].replace("Success", "Voice Portal")
    dataset[312] = dataset[312].replace("Shared Call Appearance", "Secondary Device")
    return dataset



def remove_Unwanted_data(data):
    # data type of data is list
    for index in range(len(data)):
        if data[index] == "Secondary Device" or data[index] =="Primary Device":
            continue
        else:
            data[index] = np.nan 
    return data




# This part sets all the services in one column 147
def combine_All_Services(data1, data2, data3):
    for index in range(len(data1)):
        if data1[index] is np.nan:
            
            if data2[index] is not np.nan and data3[index] is not np.nan:
                data1[index] = str(data2[index])+ "," + str(data3[index])
            
            elif data2[index] is not np.nan:
                data1[index] = data2[index]
            
            else:
                data1[index] = data3[index]
            
        else:
            continue
    return data1




# Convert data into a specific format
def call_time_fetcher(data):
    for index in range(len(data)):
        data[index] = str(data[index])
        if data[index]!="nan":
            year = data[index][:4]
            month = data[index][4:6]
            day = data[index][6:8]
            hours = data[index][8:10]
            minutes = data[index][10:12]
            seconds = str(round(float(data[index][12:])))
            if int(seconds) >= 60:
                seconds = int(seconds) -60
                minutes = int(minutes)+1 
            if int(minutes) >=60:
                hours = int(hours)+1
                minutes  = int(minutes) - 60 
            data[index] = f"{year}-{month}-{day} {hours}:{minutes}:{seconds}"
        else:
            data[index] = np.nan
    return data




def hourly_range(data):
    # Time column data is passed as a list
    # 03:27:17 AM'
    for index in range(len(data)):
        data[index] = str(data[index])
        if data[index]!="nan":
            if re.search("PM", data[index]):
                time_data =  re.findall("\d+", data[index])
                if time_data[0] != "12":
                    time_data = int(time_data[0]) + 12
                else:
                    time_data = time_data[0]
                
            else:
                time_data =  re.findall("\d+", data[index])
                if int(time_data[0]) == 12:
                    time_data = f"0{int(time_data[0]) - 12}"
                else:
                    time_data = time_data[0]
                
                
            data[index] = f"{time_data}:00 - {time_data}:59"
        else:
            data[index] = np.nan
    return data
​

​
​
def weekly_range(data):
    # Date column data is passed as a list
    # '2019-06-20' 
    for index in range(len(data)):
        data[index] = str(data[index])
        if data[index] != "nan":
            year, month, day = [int(x) for x in data[index].split("-")]
            result = datetime.date(year, month, day)
            data[index] = result.strftime("%A")
        else:
            data[index] = np.nan
    return data
​

​


# Main Code of your project 
​
'''
Domain Expert 
    
1. No column name   
   ( header = None )
    column no -  actual name
    1            serviceProvider
    5            direction
    9            startTime
    13           EndTime
    120          userId
    180          twoStageDialingDigits
    146          relatedCallId
    147          relatedCallIdReason
    267          vpDialingfacResult
    312          locationType
    345          userAgent
'''
​
​
dataset_name = 'raw_cdr_data.csv'
raw_cdr_data = pd.read_csv(dataset_name, header = None, low_memory = False )

#Calling funcs for Date
print(raw_cdr_data[9].tolist())
mydate, mytime = zip(*datetime_divider (raw_cdr_data[9].tolist() )  )
print(mydate)
print(mytime)
print(type(mydate))
print(type(mytime))
mydate = list(mydate)
print(type(mydate))
mytime = list(mytime)
print(type(mytime))
print(mydate)
print(mytime)

result_date = date_modifier(mydate)
print(result_date)



#Calling funcs for time

result_time = time_modifier(mytime)
print(result_time)


raw_cdr_data["date"] = result_date
print(raw_cdr_data["date"])

raw_cdr_data["date"].value_counts()

raw_cdr_data["time"] = result_time
print(raw_cdr_data["time"])


#Changing terminologies
raw_cdr_data[5].unique()
raw_cdr_data[267].unique()
raw_cdr_data[312].unique()

raw_cdr_data = replace_simple_with_Standard_terminology(raw_cdr_data)

raw_cdr_data[5].unique()
raw_cdr_data[267].unique()
raw_cdr_data[312].unique()


#Calling function to remove unwanted data from col 312

raw_cdr_data[312] = remove_Unwanted_data(raw_cdr_data[312].tolist())
raw_cdr_data[312].unique()




print(raw_cdr_data[147])
# Is the 147 column has missing data, then create the data from 312 and 267
raw_cdr_data[147] = combine_All_Services(raw_cdr_data[147].tolist(), raw_cdr_data[312].tolist(), raw_cdr_data[267].tolist())
    
print(raw_cdr_data[147])




# we have made temporary 2 columns to find duration
​
raw_cdr_data["starttime"] = pd.to_datetime(call_time_fetcher(raw_cdr_data[9].tolist()))
print(raw_cdr_data["starttime"])
# 2019-06-25 19:21:43
​
raw_cdr_data["endtime"] = pd.to_datetime(call_time_fetcher(raw_cdr_data[13].tolist()))
print(raw_cdr_data["endtime"])
# 2019-06-25 19:24:54
​
raw_cdr_data["duration"] =  (raw_cdr_data["endtime"] - raw_cdr_data["starttime"]).astype("timedelta64[m]")
print(raw_cdr_data["duration"])




# use the new columns created time and date
# Creates 1 hour range for 24 hours
raw_cdr_data["hourly_range"] = hourly_range(raw_cdr_data["time"].tolist())
print(raw_cdr_data["hourly_range"])
# 19:00 - 19:59
​
​
# Creates similary in Week ( Monday to Sunday )
raw_cdr_data["weekly_range"] = weekly_range(raw_cdr_data["date"].tolist())
print(raw_cdr_data["weekly_range"])
# Tuesday
​
# Remove columns not required
raw_cdr_data = raw_cdr_data.drop("time", axis=1)
    
# Save the transformed data in CSV format for further use
raw_cdr_data.to_csv("cdr_data.csv", index = None)
