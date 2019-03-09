#importing libraries
import os
import sys
from datetime import datetime, date, time
import pytz
import numpy as np
import h5py
from scipy.signal import medfilt
from matplotlib import pyplot as plt
import pandas as pd


# ### Task 1:The file name starts with an 18 digit number, which is the UNIX time in nanoseconds. Using the python datetime library and pytz, convert this number to a python datetime object in both UTC and CERN local time.


all_files=os.listdir()
h5_file_name=""
for i in all_files:
    if(i.endswith(".h5")):
        h5_file_name=i
unix_time_seconds=float(h5_file_name[:18])*(10**-9)  #converting nanoseconds to seconds
date_time_object_utc=datetime.utcfromtimestamp(unix_time_seconds)
print("The data time object in UTC is",date_time_object_utc)
tz=pytz.timezone('Europe/Zurich')
date_time_object_cern=pytz.utc.localize(date_time_object_utc).astimezone(tz)
print("The data time object for Switzerland/CERN is",date_time_object_cern)


# ### Task 2:Use the h5py library to open the hdf file. The file is organized as a directory tree with groups and datasets. Write a program which explores all branches of the directory tree and identifies all of the datasets in the file. Your program should create a csv file which records the names of all of the groups and datasets, and includes the size, shape and type of data in each dataset.

filename = h5_file_name
f = h5py.File(filename, 'r')
all_data={}

#identifying and printing datasets
def visit_func(name,node):
    if(isinstance(node,h5py.Dataset)):
        try:
            datatype=node.dtype
        except Exception as e:
            datatype=str(e)
        all_data[name]=['dataset',node.size,node.shape,datatype]
    else:
        all_data[name]=['group','','','']
f.visititems(visit_func)
df = pd.DataFrame.from_dict(all_data,orient='index',
            columns=['TYPE','SIZE','SHAPE','DATA_TYPE'])
df.to_csv('data.csv', sep=',')


# ### In the hdf file, there is 2D image data stored as a 1D array in the dataset called "/AwakeEventData/XMPP-STREAK/StreakImage/streakImageData". The datasets "/AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight" and "/AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth" store information about the height and width of the image. Use numpy.reshape to convert the 1D array into a 2D image. Then, use scipy.signal.medfilt to filter the image. Finally, use matplotlib to display the image and save it as a png file.

name_image="AwakeEventData/XMPP-STREAK/StreakImage/streakImageData"
name_height="AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight"
name_width="AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth"
image_data=None
image_height=None
image_width=None

def visit_func(name,node):
    global image_data,image_height,image_width
    if(isinstance(node,h5py.Dataset)):
        if(name==name_image):
            image_data=node
        if(name==name_height):
            image_height=node
        if(name==name_width):
            image_width=node
f.visititems(visit_func)
image_data=np.array(image_data)
image_height=np.array(image_height)[0]
image_width=np.array(image_width)[0]
image_data,image_height,image_width
image_data=np.reshape(image_data,(image_height,image_width))
plt.title("Input image");
plt.imshow(image_data);
plt.show();
output_data=medfilt(image_data)
i=plt.imshow(output_data);
plt.title("Output image");
plt.show();
plt.imsave('output_image.png',output_data);