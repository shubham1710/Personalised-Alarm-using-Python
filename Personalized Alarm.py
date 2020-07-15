#!/usr/bin/env python
# coding: utf-8

# In[6]:


#Importing the required packages
import datetime
import os
import time
import random
import csv
from pygame import mixer
import pandas as pd
import numpy as np

# Getting the current path of the script
path = os.getcwd()

# Setting up the alarm path
alarm_path = path + '\Alarm_Tunes'

# If no directory present, create one.
if not os.path.isdir(alarm_path):
    os.makedirs(alarm_path)

# Ask user to add some alarm tunes to the folder.
while len(os.listdir(alarm_path))==0:
    print("No Alarm Tunes Present. Please add some tunes to the folder before proceeding.")
    confirm = input("Have you added songs? Press Y or N:\t")
    if(confirm=="Y"):
        print("Good! Let's continue!")
        continue
    else:
        continue

def List_diff(list1, list2): 
    return (list(set(list1) - set(list2)))


# If no csv file, create the lists with parameters as zero
if not os.path.isfile("tune_parameters.csv"):
    tune_list = os.listdir(alarm_path)
    tune_time = [60]*len(tune_list)
    tune_counter = [1]*len(tune_list)
    tune_avg = [60]*len(tune_list)
    tune_prob_rev = [1/len(tune_list)]*len(tune_list)
    tune_prob = [1/len(tune_list)]*len(tune_list)

# If csv file is present, read from csv file
else:
    tune_df = pd.read_csv("tune_parameters.csv")
    tune_list_os = os.listdir(alarm_path)
    tune_list = list(tune_df['Tunes'])
    tune_diff = List_diff(tune_list_os, tune_list)
    tune_time = list(tune_df['Delay Times'])
    tune_counter = list(tune_df['Count'])
    tune_avg = list(tune_df['Average'])
    tune_prob_rev = list(tune_df['Reverse Probability'])
    tune_prob = list(tune_df['Probability'])
    
    for i in range(0,len(tune_diff)):
        tune_list.append(tune_diff[i])
        tune_time.append(60)
        tune_counter.append(1)
        tune_avg.append(60)
        tune_prob_rev.append(0.1)
        tune_prob.append(0.1)
    
    avg_sum = sum(tune_avg)
    
    for i in range(0,len(tune_prob_rev)):
        tune_prob_rev[i] = 1 - tune_avg[i]/avg_sum
    
    avg_prob = sum(tune_prob_rev)
    
    for i in range(0,len(tune_prob)):
        tune_prob[i] = tune_prob_rev[i]/avg_prob


# Verify whether time entered is correct or not.
def verify_alarm(hour,minute,seconds):
    if((hour>=0 and hour<=23) and (minute>=0 and minute<=59) and (seconds>=0 and seconds<=59)):
        return True
    else:
        return False

# Asking user to set alarm time and verifying whether true or not.
while(True):
    hour = int(input("Enter the hour in 24 Hour Format (0-23):\t"))
    minute = int(input("Enter the minutes (0-59):\t"))
    seconds = int(input("Enter the seconds (0-59):\t"))
    if verify_alarm(hour,minute,seconds):
        break
    else:
        print("Error: Wrong Time Entered! Please enter again!")

# Converting the alarm time to seconds
alarm_sec = hour*3600 + minute*60 + seconds

# Getting current time and converting it to seconds
curr_time = datetime.datetime.now()
curr_sec = curr_time.hour*3600 + curr_time.minute*60 + curr_time.second

# Calculating the number of seconds left for alarm
time_diff = alarm_sec - curr_sec

#If time difference is negative, it means the alarm is for next day.
if time_diff < 0:
    time_diff += 86400

# Displaying the time left for alarm
print("Time left for alarm is %s" % datetime.timedelta(seconds=time_diff))

# Sleep until the time at which alarm rings
time.sleep(time_diff)

print("Alarm time! Wake up! Wake up!")

# Choose a tune based on probability
tune_choice_np = np.random.choice(tune_list, 1, tune_prob)
tune_choice = tune_choice_np[0]

# Getting the index of chosen tune in list
tune_index = tune_list.index(tune_choice)

# Play the alarm tune
mixer.init()
mixer.music.load(alarm_path+"/"+tune_choice)
mixer.music.play()

# Asking user to stop the alarm
input("Press ENTER to stop alarm")
mixer.music.stop()

# Finding the time of stopping the alarm
time_stop = datetime.datetime.now()
stop_sec = time_stop.hour*3600 + time_stop.minute*60 + time_stop.second

# Calculating the time delay
time_delay = stop_sec - alarm_sec

# Updating the values
tune_time[tune_index] += time_delay
tune_counter[tune_index] += 1
tune_avg[tune_index] = tune_time[tune_index] / tune_counter[tune_index]

new_avg_sum = sum(tune_avg)

for i in range(0,len(tune_list)):
    tune_prob_rev[i] = 1 - tune_avg[i] / new_avg_sum
    
new_avg_prob = sum(tune_prob_rev)
    
for i in range(0,len(tune_list)):
    tune_prob[i] = tune_prob_rev[i] / new_avg_prob
    

#Create the merged list of all six quantities
tune_rec = [[[[[[]]]]]]

for i in range (0,len(tune_list)):
    temp=[]
    temp.append(tune_list[i])
    temp.append(tune_time[i])
    temp.append(tune_counter[i])
    temp.append(tune_avg[i])
    temp.append(tune_prob_rev[i])
    temp.append(tune_prob[i])
    tune_rec.append(temp)

tune_rec.pop(0)

#Convert merged list to a pandas dataframe
df = pd.DataFrame(tune_rec, columns=['Tunes','Delay Times','Count','Average','Reverse Probability','Probability'],dtype=float)

#Save the dataframe as a csv (if already present, will overwrite the previous one)
df.to_csv('tune_parameters.csv',index=False)


# In[ ]:




