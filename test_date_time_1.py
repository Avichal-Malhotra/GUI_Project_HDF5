# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 16:14:23 2017

@author: User
"""
import glob
import pandas as pd



path =r'G:\Python_Packages\HDF5_GUI_Version_1.2\HDF5_GUI_Version_1.2 - Kopie\Hdf5_GUI\Input_Data_2' # use your path
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    #df['Datum Uhrzeit']= df[['Datum', 'Uhrzeit']].apply(lambda x: ''.join(x), axis=1)#df.Datum.str.cat(df.Uhrzeit)
    df['Datum Uhrzeit'] = df[['Datum','Uhrzeit']].apply(lambda x : '{} {}'.format(x[0],x[1]), axis=1)  
    df = df.drop('Datum', 1)
    df = df.drop('Uhrzeit', 1)
    list_.append(df)
    
frame = pd.concat(list_)
#frame['Datum Uhrzeit']=frame[[0]]+frame[[1]]# frame[['Datum', 'Uhrzeit']].apply(lambda x: ' '.join(x), axis=1)#df.Datum.str.cat(df.Uhrzeit)
#frame['Date Time'] = frame[['Date','Time']].apply(lambda x : '{} {}'.format(x[0],x[1]), axis=1)   