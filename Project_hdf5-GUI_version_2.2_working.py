# -*- coding: utf-8 -*-
"""
@Name : Project_HDF5_Version_1.2_running
@author: Avichal Malhotra
@Time : Created on Mon Jan 30 2017 11:18:52 
Description :
This file can be used to create the datasets using the sensor names in the differtent data files.
Furthermore, The date-time stamp is converted to the unix format for the uniformity of the data.
Different datalists are created inorder to append to the datasets.
Using the duplicate indices, the duplicate values of the different sensors are deleted according to the nature of the value.

"""
"importing the different packages"
import h5py
from xml.dom import minidom
import pandas as pd
import glob
import time
import calendar
import math
import sys
from PyQt4 import QtGui, QtCore
import os
import pyqtgraph as pg
import numpy as np
from pandas import HDFStore,DataFrame

#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

#import csv
#from datetime import timedelta
import datetime
##import xmltodict
#from xml.dom.minidom import parse
#import xml.dom.minidom

import matplotlib.pyplot as plt


class Create_Values_Window(QtGui.QWidget):
    
    def __init__(self):
        # create GUI
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Create Values')
        self.setGeometry(50, 50, 325, 325)
          
        # vertical layout for widgets
        self.vbox_values = QtGui.QVBoxLayout(self)
        self.setLayout(self.vbox_values)            
    
        # Textbox for the steps defines for the user
        self.textbox_values = QtGui.QLineEdit('Step 1: Please select the Input HDF5 file to be integrated')
        self.textbox_values.move(20, 20)
        self.textbox_values.resize(280,40)
        self.textbox_values.setReadOnly(True)
        self.vbox_values.addWidget(self.textbox_values)
            
        
        # Create a label which displays the path to our chosen file
        self.lbl_input_hdf5 = QtGui.QLabel('No file selected')
        self.vbox_values.addWidget(self.lbl_input_hdf5)

        # Create a push button labelled 'Choose Input h5 file ' and add it to our layout
        self.btn_input_hdf5 = QtGui.QPushButton('Choose Input .h5 file', self)
        self.vbox_values.addWidget(self.btn_input_hdf5)
        
        
        self.button_tool_tip = QtGui.QToolButton(self)
      #  self.button_tool.setIcon('E:\Hdf5_GUI_new\Hdf5_GUI_new\Hdf5_GUI\pictures\info-512.png')
        self.button_tool_tip.setText("Info")
        self.button_tool_tip.setToolTip("""The selected format will be integrated from Raw Data as follows:\n
                                    1. Minute option will integrate the data for every minute time window.
                                    2. Hour option will integrate the data for every hour time window.
                                    3. Daily option will integrate the data for every day time window.""")
        self.vbox_values.addWidget(self.button_tool_tip)
        
        
        self.textbox_integration = QtGui.QLineEdit('Please select the integration format')
        self.textbox_integration.move(20,30)
        self.textbox_integration.resize(280,40)
        self.textbox_integration.setReadOnly(True)
        self.vbox_values.addWidget(self.textbox_integration)
        
        
        self.QCheckBox_minutes = QtGui.QCheckBox("Minute Integrate",self)
        self.QCheckBox_minutes.setGeometry(10,10,30,120)
        self.QCheckBox_minutes.move(20,20)
        self.vbox_values.addWidget(self.QCheckBox_minutes)    
        #self.QCheckBox_minutes.stateChanged.connect(self.minutes_integration)
        
        self.QCheckBox_hours = QtGui.QCheckBox("Hours Integrate",self)
        self.QCheckBox_hours.setGeometry(10,10,30,140)
        self.QCheckBox_hours.move(20,140)
        self.vbox_values.addWidget(self.QCheckBox_hours)    
       # self.QCheckBox_hours.stateChanged.connect(self.hours_integration)
        
        self.QCheckBox_days = QtGui.QCheckBox("Days Integrate",self)
        self.QCheckBox_days.setGeometry(10,10,30,140)
        self.QCheckBox_days.move(20,160)
        self.vbox_values.addWidget(self.QCheckBox_days)    
       # self.QCheckBox_days.stateChanged.connect(self.days_integration)
        
#        self.QCheckBox_select_all = QtGui.QCheckBox("Select All",self)
#        self.QCheckBox_select_all.setGeometry(10,10,30,140)
#        self.QCheckBox_select_all.move(20,160)
#        self.vbox_values.addWidget(self.QCheckBox_select_all)    
#        self.QCheckBox_days.stateChanged.connect(self.select_all)

 
        # Create a push button labelled "Select All" and add it to our layout
        self.btn_select_all = QtGui.QPushButton("Select All", self)
        self.vbox_values.addWidget(self.btn_select_all) 
 
        # Create a push button labelled 'Integrate' and add it to our layout
        self.btn_integrate = QtGui.QPushButton('Integrate', self)
        self.vbox_values.addWidget(self.btn_integrate) 
        
        # Create a push button labelled 'Integrate' and add it to our layout
        self.btn_mainwindow = QtGui.QPushButton('Main Window', self)
        self.vbox_values.addWidget(self.btn_mainwindow) 
        
        # Create a push button labelled 'Integrate' and add it to our layout
        self.btn_exit = QtGui.QPushButton('Exit Application', self)
        self.vbox_values.addWidget(self.btn_exit) 
        
        # Create a push button labelled 'Integrate' and add it to our layout
        self.btn_graphs = QtGui.QPushButton('Plot Graphs', self)
        self.vbox_values.addWidget(self.btn_graphs) 
        
        
        
        
        # Connect the clicked signal to the get_input_file handler
        self.connect(self.btn_input_hdf5, QtCore.SIGNAL('clicked()'), self.get_input_hdf5_file)
        
        # Connect the clicked signal to the integrate
        self.connect(self.btn_integrate, QtCore.SIGNAL('clicked()'), self.integrate)

        # Connect the clicked signal to the integrate
        self.connect(self.btn_select_all, QtCore.SIGNAL('clicked()'), self.select_all)        
        
         # Connect the clicked signal to the main_window
        self.connect(self.btn_mainwindow, QtCore.SIGNAL('clicked()'), self.main_window)
        
         # Connect the clicked signal to the exit
        self.connect(self.btn_exit, QtCore.SIGNAL('clicked()'), self.exit_app)
            
         # Connect the clicked signal to the plot_graphs
        self.connect(self.btn_graphs, QtCore.SIGNAL('clicked()'), self.plot_graphs)
        
        #self.group_minute_integration= ''
        
    
    def get_input_hdf5_file(self):
        """
        Handler called when 'Choose the input HDF5 file' is clicked
        """
        
        self.input_h5 = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
        if self.input_h5:
            self.lbl_input_hdf5.setText(self.input_h5)
            self.textbox_values.setText('Step 2 : Please select the Time format')
        else:
            self.lbl_input_hdf5.setText('No file selected')   
    
    def integrate(self):    
        """
        Handler called when 'Integration' is clicked
        """        
        self.file_selected_to_integrate = h5py.File(self.input_h5, 'a') 
        print(self.input_h5)
        #group_minute_integration = file_selected_to_integrate.create_group("Minute Integration Data Group") 
   #     print(file_selected_to_integrate.keys())
   
   
 #       "Check if the Minute Checkbox is selected"
        if self.QCheckBox_minutes.isChecked()==True:
            e = "Minutely Group Exists"
            node = '/Minute Data Group'
            if node in self.file_selected_to_integrate.keys():
                self.file_selected_to_integrate[node]
                print(e)
            else:
                self.group_minute_integration = self.file_selected_to_integrate.create_group("Minute Data Group")
            self.minutes_integration()              
                                    
 #       """Check if the Hourly Checkbox is selected"""    
        if self.QCheckBox_hours.isChecked()==True:
         #   
            e = "Hourly Group Exists"
            node = '/Hourly Data Group'
            if node in  self.file_selected_to_integrate.keys():
                self.file_selected_to_integrate[node]
                print(e)
            else:
                self.group_hour_integration = self.file_selected_to_integrate.create_group("Hourly Data Group")
            self.hours_integration()
            
#         "Check if the Daily Checkbox is selected"     
        if self.QCheckBox_days.isChecked()==True:
          #  
            e = "Daily Group Exists"
            node = '/Daily Data Group'
            if node in self.file_selected_to_integrate.keys():
                self.file_selected_to_integrate[node]
                print(e)
            else:
                self.group_day_integration = self.file_selected_to_integrate.create_group("Daily Data Group")
            self.days_integration()
        
        self.file_selected_to_integrate.close()    
            
    def minutes_integration(self):
        """
        Handler called when 'Minutes Integration' is clicked
        """
        minutes=[]         
        with h5py.File(self.input_h5,'a') as hdf:

            item_raw_data = hdf["Raw Data Groups"]
            group_minute= hdf["Minute Data Group"]
            for self.datasets_minutes in item_raw_data:
            
                minutes.append(self.datasets_minutes)
                value=[]
                time_data=[]
                time_stamps_readable=[]
                for values in item_raw_data[self.datasets_minutes]:
                    time_data.append(values[0])
                    value.append(values[1])
                
                for times in time_data:    
                    temp = datetime.datetime.fromtimestamp(times).strftime('%Y-%m-%d %H:%M:%S')
                    time_stamps_readable.append(temp)    
                df_minute = pd.DataFrame(
                                  {#'Time': time_data,
                                   'Sensor_Value': value,
                                   'Temp': time_stamps_readable
                                  })
                df_minute['Temp'] = pd.to_datetime(df_minute['Temp'])
                df_minute.index = df_minute['Temp']
                #del df['Temp']
                
                df_minute = df_minute.sort_index(axis=0)
                
                self.df2_minutes= pd.DataFrame()
                self.df2_minutes["Sensor Value"] = df_minute.Sensor_Value.resample('T').bfill()
                time_read_minutes = self.df2_minutes.index.values.tolist()
                self.df2_minutes["Time"]=time_read_minutes

                e_minute = "Minutely Dataset "+self.datasets_minutes+" exists"
                node_minute = "Minute_data_"+self.datasets_minutes
                if node_minute in group_minute:
                    group_minute[node_minute]
                    print(e_minute)
                else:
                    self.datasensors_minutes= group_minute.create_dataset("Minute_data_"+self.datasets_minutes, data= self.df2_minutes)                  
               
            
            
    
    def hours_integration(self):
        """
        Handler called when 'Hours Integration' is clicked
        """
        hours=[]         
        with h5py.File(self.input_h5,'a') as hdf:

            item_hours = hdf["Raw Data Groups"]
            group_hours= hdf["Hourly Data Group"]
            for self.datasets_hours in item_hours:
            
                hours.append(self.datasets_hours)
                value=[]
                time_data=[]
                time_stamps_readable=[]
                for values in item_hours[self.datasets_hours]:
                    time_data.append(values[0])
                    value.append(values[1])
                
                for times in time_data:    
                    temp = datetime.datetime.fromtimestamp(times).strftime('%Y-%m-%d %H:%M:%S')
                    time_stamps_readable.append(temp)    
                df_hours = pd.DataFrame(
                                  {#'Time': time_data,
                                   'Sensor_Value': value,
                                   'Temp': time_stamps_readable
                                  })
                df_hours['Temp'] = pd.to_datetime(df_hours['Temp'])
                df_hours.index = df_hours['Temp']
                #del df['Temp']
                df_hours = df_hours.sort_index(axis=0)

                self.df2_hours= pd.DataFrame()
                self.df2_hours["Sensor Value"] = df_hours.Sensor_Value.resample('H').bfill()
                time_read_hours = self.df2_hours.index.values.tolist()
                self.df2_hours["Time"]=time_read_hours
                
               
                
                e_hours = "Hourly Dataset "+self.datasets_hours+" exists"
                node_hour = "Hourly_data_"+self.datasets_hours
                if node_hour in group_hours:
                    group_hours[node_hour]
                    print(e_hours)
                else:
                    self.datasensors_hours= group_hours.create_dataset("Hourly_data_"+self.datasets_hours, data= self.df2_hours)                  
               
                
              #  print(self.df2_hours)   

       
    def days_integration(self):
        """
        Handler called when 'Days Integration' is clicked
        """


        days=[]         
        with h5py.File(self.input_h5,'a') as hdf:

            item_days = hdf["Raw Data Groups"]
            group_days = hdf["Daily Data Group"]
            for self.datasets_days in item_days:
            
                days.append(self.datasets_days)
                value=[]
                time_data=[]
                time_stamps_readable=[]
                for values in item_days[self.datasets_days]:
                    time_data.append(values[0])
                    value.append(values[1])
                
                for times in time_data:    
                    temp = datetime.datetime.fromtimestamp(times).strftime('%Y-%m-%d %H:%M:%S')
                    time_stamps_readable.append(temp)    
                df_days = pd.DataFrame(
                                  {#'Time': time_data,
                                   'Sensor_Value': value,
                                   'Temp': time_stamps_readable
                                  })
                df_days['Temp'] = pd.to_datetime(df_days['Temp'])
                df_days.index = df_days['Temp']

                df_days = df_days.sort_index(axis=0)

                self.df2_days= pd.DataFrame()
                self.df2_days["Sensor Value"] = df_days.Sensor_Value.resample('D').bfill()
                time_read_days = self.df2_days.index.values.tolist()
                self.df2_days["Time"]=time_read_days

                e_days = "Daily Dataset "+self.datasets_days+" exists"
                node_days = "Daily_data_"+self.datasets_days
                if node_days in group_days:
                    group_days[node_days]
                    print(e_days)
                else:
                    self.datasensors_days= group_days.create_dataset("Daily_data_"+self.datasets_days, data= self.df2_days)                  
 

        
    def select_all(self):        
        """
        Handler called when 'All the check boxes have to selected' is clicked
        """
            
        self.QCheckBox_minutes.setChecked(True) 
        self.QCheckBox_hours.setChecked(True)
        self.QCheckBox_days.setChecked(True)
     #   self.textbox_integration.setText('Minutes, Hours and Days selected')
    

            
    def main_window(self):    
        """
        Handler called when 'Main Window' is clicked
        """  
        #Create_Graphs_Window.close()
        self.mainwindow = Window()
        self.mainwindow.show()
        #QtGui.QMainWindow.closeEvent()


        
    def exit_app(self):
        """
        Handler called when the Exit button is clicked 
        """
        choice = QtGui.QMessageBox.question(self, '',
                                            "Do you want to quit?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Ready to quit")
            QtCore.QCoreApplication.instance().quit()
         #   sys.exit()
        else:
            pass
    
             
    def plot_graphs(self):    
        """
        Handler called when 'Plot Graphs' is clicked
        """       
        self.create_graphs = Create_Graphs_Window(Calender)
        self.create_graphs.show()
  
        


class Calender(QtGui.QWidget):

   def __init__(self):
      super(Calender, self).__init__()

      self.initUI()
		
   def initUI(self):
	
      self.cal = QtGui.QCalendarWidget(self)
      self.cal.setGridVisible(True)
      self.cal.move(20, 20)
      self.cal.clicked[QtCore.QDate].connect(self.showDate)
	# Create a push button labelled 'Choose Input h5 file ' and add it to our layout
      self.btn_OK = QtGui.QPushButton('OK', self)
      self.btn_OK.move(20, 20)
  #    self.vbox_graphs.addWidget(self.btn_select_date)	
      self.lbl_date = QtGui.QLabel(self)
      self.date = self.cal.selectedDate()
      self.lbl_date.setText(self.date.toString())
      self.lbl_date.move(20, 200)
	
      
      # Connect the clicked signal to the exit
      self.connect(self.btn_OK, QtCore.SIGNAL('clicked()'), self.OK)        
      
      self.setGeometry(100,100,300,300)
      self.setWindowTitle('Calendar')
      self.show()
		
      
      
      
   def showDate(self):
	
      self.lbl_date.setText(self.date.toString())
   
   def OK(self):   
      return(self.cal.selectedDate())     
      
      
class Create_Graphs_Window(QtGui.QWidget):
    sensor_names = []
    
    def __init__(self, Calender):
        # create GUI
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Create Graphs')
        self.setGeometry(50, 50, 400, 400)
        
#        # a figure instance to plot on
#        self.figure = plt.figure()
#
#        # this is the Canvas Widget that displays the `figure`
#        # it takes the `figure` instance as a parameter to __init__
#        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
       # self.toolbar = NavigationToolbar(self.canvas, self)  
        # vertical layout for widgets
        self.vbox_graphs = QtGui.QVBoxLayout(self)
        self.setLayout(self.vbox_graphs)            
        
        
        
#        self.vbox_graphs.addWidget(self.toolbar)
#        self.vbox_graphs.addWidget(self.canvas)
       # layout.addWidget(self.button)
        
        # Textbox for the steps defines for the user
        self.textbox_graphs = QtGui.QLineEdit('Step 1: Select the input .h5 file')
        self.textbox_graphs.move(10, 10)
        self.textbox_graphs.resize(10,10)
        self.textbox_graphs.setReadOnly(True)
        self.vbox_graphs.addWidget(self.textbox_graphs)
        
#        # Create a label which displays the path to our chosen file
        self.lbl_input_hdf5 = QtGui.QLabel('No file selected')
        self.lbl_input_hdf5.move(20,200)
        self.vbox_graphs.addWidget(self.lbl_input_hdf5)
        
        # Create a push button labelled 'Choose Input h5 file ' and add it to our layout
        self.btn_input_hdf5 = QtGui.QPushButton('Choose Input .h5 file', self)
        self.btn_input_hdf5.move(20,20)
        self.vbox_graphs.addWidget(self.btn_input_hdf5)
       
#        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
#        self.setToolTip('Test')        
        
        
        self.button_tool = QtGui.QToolButton(self)
      #  self.button_tool.setIcon('E:\Hdf5_GUI_new\Hdf5_GUI_new\Hdf5_GUI\pictures\info-512.png')
        self.button_tool.setText("Info")
        self.button_tool.setToolTip("""The selected group will be plotted as follows:\n
                                    1. Minutely Data is ploted for the hour time window,i.e.\n
                                       +- 30 minutes to the time selected\n
                                    2. Hourly Data is ploted for the 24 hour time window,i.e.\n
                                       +- 12 hours to the time selected\n 
                                    3. Daily data is ploted for a week time window, i.e.\n
                                       +- 3 days to the day selected """)
        self.vbox_graphs.addWidget(self.button_tool)
        
            
        
        
        self.lbl_group_view = QtGui.QLabel('Select the group to be ploted.')
     #   self.lbl_group_view.move(20,200)
        #self.lbl_group_view.setToolTip('Avichal') 
        self.vbox_graphs.addWidget(self.lbl_group_view)
        
        
        
#        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
#        self.setToolTip('Test')        
                                    
        self.comboBox_groups = QtGui.QComboBox(self)
        self.comboBox_groups.setGeometry(30,75,350,50)
        self.comboBox_groups.move(30, 125)
       # self.comboBox_groups.setToolTip('Test')
        self.vbox_graphs.addWidget(self.comboBox_groups)
        
      
        
        self.lbl_sensor = QtGui.QLabel('Select the sensor to be ploted.')
    #    self.lbl_sensor.move(20,200)
        self.vbox_graphs.addWidget(self.lbl_sensor)

        
        
        self.comboBox_sensors = QtGui.QComboBox(self)
        self.comboBox_sensors.setGeometry(30,75,350,50)
        self.comboBox_sensors.move(30,170)
        self.vbox_graphs.addWidget(self.comboBox_sensors)
        
        
        self.lbl_sensor = QtGui.QLabel('Select the plot type.')
    #    self.lbl_sensor.move(20,200)
        self.vbox_graphs.addWidget(self.lbl_sensor)

        
        
        self.comboBox_plot_type = QtGui.QComboBox(self)
        self.comboBox_plot_type.setGeometry(30,75,350,50)
        self.comboBox_plot_type.move(30,170)
        self.vbox_graphs.addWidget(self.comboBox_plot_type)
        
        
        # Create a push button labelled 'Choose Input h5 file ' and add it to our layout
#        self.btn_select_date = QtGui.QPushButton('Select Date', self)
#        self.btn_select_date.move(20,40)
#        self.vbox_graphs.addWidget(self.btn_select_date)
#        
        
         # Create a push button labelled 'Integrate' and add it to our layout
        self.btn_mainwindow = QtGui.QPushButton('Main Window', self)
        self.vbox_graphs.addWidget(self.btn_mainwindow) 
        
        # Create a push button labelled 'Integrate' and add it to our layout
        self.btn_exit = QtGui.QPushButton('Exit Application', self)
        self.vbox_graphs.addWidget(self.btn_exit) 
        
        # Create a push button labelled 'Integrate' and add it to our layout
        self.btn_graphs = QtGui.QPushButton('Plot Graphs', self)
        self.vbox_graphs.addWidget(self.btn_graphs) 
       
 
        # Connect the clicked signal to the exit
        self.connect(self.btn_input_hdf5, QtCore.SIGNAL('clicked()'), self.get_input_hdf5_file)        
        
        # Connect the clicked signal to the exit
       # self.connect(self.btn_select_date, QtCore.SIGNAL('clicked()'), self.select_date)        
        
         # Connect the clicked signal to the main_window
        self.connect(self.btn_mainwindow, QtCore.SIGNAL('clicked()'), self.main_window)
            
         # Connect the clicked signal to the exit
        self.connect(self.btn_exit, QtCore.SIGNAL('clicked()'), self.exit_app)
            
         # Connect the clicked signal to the plot_graphs
        self.connect(self.btn_graphs, QtCore.SIGNAL('clicked()'), self.plot)
           
        

#  #  def select_date(self):
#        """
#        Handler called when 'Select Date' is clicked
#        """
#        self.select_date_view = Calender()
#        self.select_date_view.show()


        
    def get_input_hdf5_file(self):
        """
        Handler called when 'Choose the input HDF5 file' is clicked
        """
        
        self.input_h5 = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
        if self.input_h5:
            self.lbl_input_hdf5.setText(self.input_h5)
            self.textbox_graphs.setText('Step 2: Select the Sensor(s) to be viewed graphically.')
        else:
            self.lbl_input_hdf5.setText('No file selected')    
       
#        def group(self,item):
#            return(item)
            
        
        group_names=[]
        
        self.file_selected_to_plot = h5py.File(self.input_h5, 'a')
        self.comboBox_groups.addItem("Select Group")
        for groups in self.file_selected_to_plot.keys():
            group_names.append(groups)
        self.comboBox_groups.addItems(group_names)   
        
        self.comboBox_groups.activated.connect(self.fill_sensor)
        
        
    def fill_sensor(self): 
        sensorlist_raw_data=[]
        
        for i,sensors in enumerate(self.file_selected_to_plot[self.comboBox_groups.currentText()]):
            sensorlist_raw_data.append(sensors.split("_",2)[2])
        self.comboBox_sensors.addItems(sensorlist_raw_data)#.split("_",3)[1])
        self.comboBox_sensors.setCurrentIndex(0)
        self.comboBox_sensors.activated.connect(self.fill_date)
        
    def fill_date(self):
        plot_date = []
                
        
        if self.comboBox_groups.currentText() == "Minute Data Group":
            
            item = self.file_selected_to_plot["Minute Data Group"]
            name_minutes= "Minute_data_"+self.comboBox_sensors.currentText()
            print(name_minutes)
            #for value in self.file_selected_to_plot.keys():
            list_minutes = item[name_minutes]
            for values in list_minutes:
                for col in values:
                    plot_date.append(col)
                    print(col)
            print(plot_date)    
            #    self.comboBox_plot_type.addItems(plot_date)
        
        if self.comboBox_groups.currentText() == "Hourly Data Group":
            name_hours= "Hourly_data_"+self.comboBox_sensors.currentText()
            print(name_hours)    
            
            
    
        
        if self.comboBox_groups.currentText() == "Daily Data Group":
            name_days= "Daily_data_"+self.comboBox_sensors.currentText()
            print(name_days)    
            
                
            
        
        if self.comboBox_groups.currentText() == "Raw Data Groups":
            name_raw= "Raw_data_"+self.comboBox_sensors.currentText()
            print(name_raw)    
                
            
            
        
        #for value in self.comboBox_sensors.currentText():       
            

 
#        for i,date in enumerate(self.file_selected_to_plot[self.comboBox_sensors.currentText()]):
#            print(date)
#            plot_date.append(date)
#        
#            print(plot_date)
#        
#        self.comboBox_plot_type.addItems(plot_date)
#        


#        
#        for groups in self.file_selected_to_plot.keys():
#            print(groups)
#            for datasets in (groups):
#                print(datasets)        
#                print(smallgroups)
#                for datasets in smallgroups:
                
                #print(datasets)
                #date_for_plot.append(datasets)
                
       # print(date_for_plot)    
        
        
        #        for timestamp in self.file_selected_to_plot["Raw Data Groups"]:    
#        
#            time_tuple = time.gmtime(timestamp)      
#            dt_obj = datetime(*time_tuple[0:6])
#            date_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
#            date_for_plot.append(date_str)
#        self.comboBox_date.addItems(date_for_plot)
#        
        
    #    for timestamp in self.file_selected_to_plot["Raw Data Groups"][0]:    
#        
#            time_tuple = time.gmtime(timestamp)      
#            dt_obj = datetime(*time_tuple[0:6])
#            date_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
#            date_for_plot.append(date_str)
#        self.comboBox_date.addItems(date_for_plot)            
            #    def sensor_names(self):
#        """
#        Handler called when 'The h5 file is selected' 
#        """
#        self.file_selected_to_plot = h5py.File(self.input_h5, 'a')
#        for sensors in self.file_selected_to_plot["Raw Data Group"]:
#            self.sensorlist = sensors
#            print(sensors)
#            
    
    #def date_convert(self):
#        date_for_plot = []        
#        for groups in self.file_selected_to_plot["Raw Data Groups"]:
#            for datasets in groups[0]:
#                print(datasets)
#            
            
            
            
#            
#            time_tuple = time.gmtime(timestamp)      
#            dt_obj = datetime(*time_tuple[0:6])
#            date_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
#            date_for_plot.append(date_str)
#        self.comboBox_date.addItems(date_for_plot)            
         

        
    def plot(self):
        """
        Handler called when 'Main Window' is clicked
        """
        x = [1,2,3]#self.comboBox_sensors.itemData(self.comboBox_sensors.currentIndex())#
        y = [4,5,6]
        labels = {"left": ("Sensor value", ),
                 "bottom": ("Time", )}
        plotWidget = pg.plot(title="Sensor Values over Time",labels = labels)

        plotWidget.plot(x,y)#, pen=None, symbol='o')
#        plt.plot([1,2,3,4], [1,4,9,16], 'ro')
 #       plt.axis([0, 6, 0, 20])
  #      plt.show()

        
    def main_window(self):    
        """
        Handler called when 'Main Window' is clicked
        """  
        #Create_Graphs_Window.close()
        self.mainwindow = Window()
        self.mainwindow.show()
        #QtGui.QMainWindow.closeEvent()


        
    def exit_app(self):
        """
        Handler called when the Exit button is clicked 
        """
        choice = QtGui.QMessageBox.question(self, '',
                                            "Do you want to quit?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Ready to quit")
            QtCore.QCoreApplication.instance().quit()
         #   sys.exit()
        else:
            pass
            

class Window(QtGui.QWidget):
    """
    The HDF5 dataset file
    """

    def __init__(self):
        # create GUI
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('HDF5 data writer')
        self.setGeometry(50, 50, 500, 600)
          
        # vertical layout for widgets
        self.vbox = QtGui.QVBoxLayout(self)
        self.setLayout(self.vbox)        
        
        # Textbox for the steps defines for the user
        self.textbox = QtGui.QLineEdit('Step 1: Please select the Input Data folder')
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)
        self.textbox.setReadOnly(True)
        self.vbox.addWidget(self.textbox)
            
        
        # Create a label which displays the path to our chosen file
        self.lbl_input_folder = QtGui.QLabel('No file selected')
        self.vbox.addWidget(self.lbl_input_folder)

        # Create a push button labelled 'Choose Input Data Folder ' and add it to our layout
        self.btn_input_folder = QtGui.QPushButton('Choose Input Data Folder', self)
        self.vbox.addWidget(self.btn_input_folder)
        
        #Create label for displaying the output folder path
        self.lbl_output_folder = QtGui.QLabel('No file selected')
        self.vbox.addWidget(self.lbl_output_folder)

        # Create a push button labelled 'Choose Output Data Folder ' and add it to our layout
        self.btn_output_folder = QtGui.QPushButton('Choose Output Data Folder', self)
        self.vbox.addWidget(self.btn_output_folder)
        
        # Create a label for writing the name of the output file
        self.lbl_output_file = QtGui.QLabel('Enter the output file name')
        self.vbox.addWidget(self.lbl_output_file)
        
        # Create a textbox for writing the name of the output file
        self.textbox_h5_name = QtGui.QLineEdit('')
        self.textbox_h5_name.move(20, 20)
        self.textbox_h5_name.resize(280,300)
        self.vbox.addWidget(self.textbox_h5_name)
        self.textbox_h5_name.setPlaceholderText('Enter the name of the output HDF5 file.')
        
        # Create a label which displays the path to our chosen file
        self.lbl_xml = QtGui.QLabel('Select the input XML file')
        self.vbox.addWidget(self.lbl_xml)

        # Create a push button labelled 'choose' and add it to our layout
        self.btn_xml = QtGui.QPushButton('Choose the input XML file', self)
        self.vbox.addWidget(self.btn_xml)
        
        # Create a label which ask the user to select the Date and Time format
        self.lbl_Datum_Uhrzeit = QtGui.QLabel('Please select the Date and Time Format in Input Data')
        self.vbox.addWidget(self.lbl_Datum_Uhrzeit)
    
        # Create a label_1 for Date and Time Format
        self.label_Datum_Uhrzeit = QtGui.QLabel("",self) 
        self.label_Datum_Uhrzeit.setGeometry(10,10,600,200)
        self.label_Datum_Uhrzeit.move(50, 630)
        pixmap = QtGui.QPixmap('DatumUhrzeit\Datum_Uhrzeit.png')
        pixmap_resized_Datum_Uhrzeit = pixmap.scaled(280, 70, QtCore.Qt.KeepAspectRatio)
        self.label_Datum_Uhrzeit.setPixmap(pixmap_resized_Datum_Uhrzeit)
        self.vbox.addWidget(self.label_Datum_Uhrzeit)
        
        # Create a checkbox1 for the Date and Time Format(label_1) 
        self.QCheckBox1 = QtGui.QCheckBox("",self)
        self.QCheckBox1.setGeometry(10,10,30,320)
        self.QCheckBox1.move(20,650)
        self.vbox.addWidget(self.QCheckBox1)    
        self.QCheckBox1.stateChanged.connect(self.Datum_Uhrzeit)
        
        
        # Create a label_2 for Date and Time Format        
        self.label_DatumUhrzeit = QtGui.QLabel("",self) 
        self.label_DatumUhrzeit.setGeometry(500,100,600,200)
        self.label_DatumUhrzeit.move(300, 630)
        pixmap1 = QtGui.QPixmap('DatumUhrzeit\DatumUhrzeit.png')
        pixmap_resized_DatumUhrzeit = pixmap1.scaled(280, 70, QtCore.Qt.KeepAspectRatio)
        self.label_DatumUhrzeit.setPixmap(pixmap_resized_DatumUhrzeit)
        self.vbox.addWidget(self.label_DatumUhrzeit)
        
        # Create a checkbox2 for the Date and Time Format(label_2)
        self.QCheckBox2 = QtGui.QCheckBox("",self)
        self.vbox.addWidget(self.QCheckBox2) 
        self.QCheckBox2.move(275,650)
        self.QCheckBox2.stateChanged.connect(self.Datum_Uhrzeit)

        # Create a push button labelled 'Run' and add it to our layout
        self.btn_run = QtGui.QPushButton('Run', self)
        self.vbox.addWidget(self.btn_run)
        
         # Create a label which ask the user to select the Date and Time format
        self.lbl_check = QtGui.QLabel('Select the file to be checked')
        self.vbox.addWidget(self.lbl_check)
        
        self.textbox_check = QtGui.QLineEdit('Please select the file to be checked')
        self.textbox_check.move(20, 20)
        self.textbox_check.resize(280,40)
        self.textbox_check.setReadOnly(True)
        self.vbox.addWidget(self.textbox_check)
                
        #Create a push button to 'Check the values in the .h5 file'
        self.btn_check = QtGui.QPushButton('Check',self)
        self.vbox.addWidget(self.btn_check)
        
        #Create a push button to 'Create the time dependent values values in the .h5 file'
        self.btn_create_values = QtGui.QPushButton('Create Values',self)
        self.vbox.addWidget(self.btn_create_values)
        
        
        #Create a push button to 'Create the graphs for the values in the .h5 file'
        self.btn_create_graphs = QtGui.QPushButton('Create Graphs',self)
        self.vbox.addWidget(self.btn_create_graphs)
        
        
        # Create a push button labelled 'Exit' and add it to our layout
        self.btn_exit = QtGui.QPushButton('Exit', self)
        self.vbox.addWidget(self.btn_exit)
        
        #Opens a dialog when the process is complete
        self.msg1 = QtGui.QMessageBox()
        self.msg1.setIcon(QtGui.QMessageBox.Information)
        self.msg1.setText("Complete")
               
        
        # Connect the clicked signal to the get_input_file handler
        self.connect(self.btn_xml, QtCore.SIGNAL('clicked()'), self.get_input_filename)
        
        # Connect the clicked signal to the get_input_foldername handler
        self.connect(self.btn_input_folder, QtCore.SIGNAL('clicked()'), self.get_input_data_folder)
        
        # Connect the clicked signal to the get_input_foldername handler
        self.connect(self.btn_output_folder, QtCore.SIGNAL('clicked()'), self.get_output_data_folder)
        
        # Connect the text change signal is the text s changed within the file name editor
        self.connect(self.textbox_h5_name, QtCore.SIGNAL('textChanged(const QString &)'), self.text_status)
        
        # Connect the clicked signal to the RUN handler
        self.connect(self.btn_run, QtCore.SIGNAL('clicked()'), self.run)
        self.connect(self.btn_run, QtCore.SIGNAL('clicked()'), self.text)
        
         # Connect the clicked signal to Check handler
        self.connect(self.btn_check, QtCore.SIGNAL('clicked()'), self.check_h5)
        self.connect(self.btn_check, QtCore.SIGNAL('clicked()'), self.text_check) 
        
        # Connect the clicked signal to Create values handler
        self.connect(self.btn_create_values, QtCore.SIGNAL('clicked()'), self.create_values)
        
        # Connect the clicked signal to Create Graphs handler
        self.connect(self.btn_create_graphs, QtCore.SIGNAL('clicked()'), self.create_graphs)
        
        # Connect the clicked signal to EXIT handler
        self.connect(self.btn_exit, QtCore.SIGNAL('clicked()'), self.close_application)
        

        
    def get_input_filename(self):
        """
        Handler called when 'Choose the input XML file' is clicked
        """
        
        self.fname_xml = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
        if self.fname_xml:
            self.lbl_xml.setText(self.fname_xml)
            self.textbox.setText('Step 5 : Please select the Date and Time Format')
        else:
            self.lbl_xml.setText('No file selected')
            
          
    def get_input_data_folder(self):
        """
        Handler called when 'Choose the input data folder' is clicked
        """

        self.input_foldername = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        
        if self.input_foldername:
            self.lbl_input_folder.setText(self.input_foldername)
            self.textbox.setText('Step 2: Please select the Output Data folder')
        else:
            self.lbl_input_folder.setText('No file selected')
            
            
            
    def get_output_data_folder(self):
        """
        Handler called when 'Choose the Output data folder ' is clicked
        """

        self.output_foldername = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        
        if self.output_foldername:
            self.lbl_output_folder.setText(self.output_foldername)
            self.textbox.setText('Step 3: Please name the file')
        else:
            self.lbl_output_folder.setText('No file selected')        
      
            
    def text_status(self):
        """
        Handler called when the text of the output file name is given 
        """
        self.lbl_output_file.setText(self.textbox_h5_name.text()+'_(XML Project Name).h5')
        self.textbox.setText('Step 4 : Choose the input XML file')
    
             
    def Datum_Uhrzeit(self):
        """
        Handler called when the Date and Time format is chosen 
        """
        if self.QCheckBox2.isChecked():
            self.textbox.setText('Step 6: Hit Run!!')
        else:
            self.textbox.setText('Step 6: Hit Run!!')
          

            
    def close_application(self):
        """
        Handler called when the Exit button is clicked 
        """
        choice = QtGui.QMessageBox.question(self, '',
                                            "Do you want to quit?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Ready to quit")
            QtCore.QCoreApplication.instance().quit()
         #   sys.exit()
        else:
            pass
    
        
    def text(self):
        """
        Handler called when the file is completed and the final run time is shown 
        """        
        self.start_time = time.time()
        self.textbox.setText('Complete in '+"%s seconds" % (time.time() - self.start_time)+'. '+ self.textbox_h5_name.text()+'.h5 file created!!!')
        self.showdialog()
    
    def text_check(self):
        """
        Handler called when the file is completed and the final run time is shown 
        """        
        self.start_time = time.time()
        self.textbox.setText('File checked in complete in '+"%s seconds" % (time.time() - self.start_time))
        self.showdialog_check()    
        
    def showdialog(self):
        """
        Handler called when the file run is complete! 
        """
        self.message = QtGui.QMessageBox.information(self, "Information", "Complete!")
    
    def showdialog_check(self):
        """
        Handler called when the file run is complete! 
        """
        self.message = QtGui.QMessageBox.information(self, "Information","Checking Complete!")
             
    def create_values(self):
        """
        Handler called when the values are to be created! 
        """        
        self.create_values_Window = Create_Values_Window()
        self.create_values_Window.show()
        
        
        
        
    def create_graphs(self):
        """
        Handler called when the graphs are to be created!  
        """    
        self.create_graphs_Window = Create_Graphs_Window(Calender)
        self.create_graphs_Window.show()
        
    
        
    def check_h5(self):
        
        self.count_in_good_range=0
        self.count_in_plausible_range=0
        self.count_not_in_range = 0
        self.count_total_values_checked = 0
        self.count_nan=0
        self.percentage_correct_values=0
        self.dir_path = os.getcwd()+'\check_csv'
        #print(self.dir_path)
        self.filename_h5 = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
       # filename=self.filename_h5.split("/")[-1]
        #print(filename)
        #dir = os.path.dirname(filename)
        if not os.path.exists(os.getcwd()):
            os.makedirs(os.getcwd())
            #print(os.getcwd())
        if self.filename_h5:
            self.lbl_check.setText(self.filename_h5)
            self.textbox.setText('Checking the selected file...')

            df = pd.read_csv(self.dir_path+r'\testRoutineValues_V2.csv', header =0, delimiter=';')
            #print(self.dir_path)
            Sensorname = df.Sensorname.tolist()
            #print(Sensorname)
            Minimum_good = df.good_min.tolist()
            Maximum_good = df.good_max.tolist()
            Minimum_plausible = df.plausible_min.tolist()
            Maximum_plausible = df.plausible_max.tolist()
            
          #  Minimum = df.Min.tolist()
           # Maximum = df.Max.tolist()

           
            value_without_last_reference=[]
            value_without_number=[]
            list_of_the_datasets = []
            index_of_the_datasets = []
            file_selected_h5 = h5py.File(self.filename_h5, 'r')
            item = file_selected_h5["Raw Data Groups"]

            for datasets in item:
               # for datasets in raw:
                list_of_the_datasets.append(datasets)
                index_of_the_datasets.append(list_of_the_datasets.index(datasets))
                
                value_without_number.append(datasets.split("_",1)[1])
                #print(value_without_number)    
            for key in value_without_number:    
                value_without_last_reference.append(key.rsplit("_", 1)[0])
                 
                
            for sensor_name in value_without_last_reference:

                if sensor_name in Sensorname:
                    #print(sensor_name)
                    Range_for_good_check = range(Minimum_good[Sensorname.index(sensor_name)], Maximum_good[Sensorname.index(sensor_name)])
                    Range_for_plausible_check = range(Minimum_plausible[Sensorname.index(sensor_name)], Maximum_plausible[Sensorname.index(sensor_name)])
                    for datasets_raw in item:
                        for entry in item[datasets_raw] :

                            if math.isnan(entry[1])== True:
                                self.count_nan+=1
                                self.count_total_values_checked+=1
                            
                            elif entry[1] in Range_for_good_check:
                                self.count_in_good_range+=1
                                self.count_total_values_checked+=1
                            
                            elif entry[1] in Range_for_plausible_check:
                                self.count_in_plausible_range+=1
                                self.count_total_values_checked+=1
                        
                            elif entry[1] not in Range_for_plausible_check:
                                self.count_not_in_range+=1
                                self.count_total_values_checked+=1
       

                else:
                    pass
            self.good_values = self.count_in_good_range+self.count_in_plausible_range    
            self.percentage_correct_values= (self.good_values/self.count_total_values_checked)*100         
            
            self.NAN = "Nan:"+str(self.count_nan)
            self.Not_in_range ="Not in Range:"+str(self.count_not_in_range)
            self.Range_good ="In good Range:"+str(self.count_in_good_range)
            self.Range_plausible = "In plausible Range:"+ str(self.count_in_plausible_range)
            self.Total = "Total Values :"+str(self.count_total_values_checked)
            self.Percentage = "Percentage of in range values:  "+ str(self.percentage_correct_values)
            
            file_selected_h5.close()
            
            self.textbox.setText('File checking completed in : ')
            self.textbox_check.setText(self.NAN+" \n "+self.Range_good+" \n "+self.Range_plausible+"\n"+self.Not_in_range+" \n "+self.Total+" \n "+self.Percentage)
            
            
        else:
            self.lbl_xml.setText('No file selected')
            self.textbox_check.setText('Please select the file to be checked')
            
        
    def run(self):   
        
        "Reading the XML file"

        xmldoc = minidom.parse(self.fname_xml) 
        self.itemlist = xmldoc.getElementsByTagName('node')
        

        
        "Getting the Project Name"
        self.project_name = self.itemlist[0].attributes['text'].value
        #print(self.project_name)
        #return(self.project_name)
        
        "Getting the number of Headers"
        self.header_number= len(self.itemlist)-1

        "Creating a new project"
        self.filename = self.textbox_h5_name.text()
        self.filepath = os.path.join(self.output_foldername, self.filename)
        file = h5py.File(self.filepath+'_'+self.project_name +'.h5','w')
        
        
        
        "Getting all the header names into a list"
        "Create the different groups with the header names"
        "Adding all the headers to the datasets"
        
        "Getting the number of Headers"
        self.textbox.setText('Running...')
        header_number= len(self.itemlist)-1
        
        header_names= []
        for i in range(1,header_number+1,1):
            header_names.append(self.itemlist[i].attributes['text'].value)
        
            
        #for s in self.itemlist:    
        #    print(s.attributes['text'].value)
        
        
        name = "DataList" 
        value = "[]" 
        for i in range(0, header_number,1):
            command_variable = ""
            command_variable = name + str(i) + " = " + value
            exec(command_variable)
     #       exec command_variable in globals(), locals()
            
        " This method changes the time in a particular format example: %d-%m-%Y %H:%M:%S"       
        def time_format():
            
            for entry in Time_A:
                time_tuple = time.strptime(entry, "%d-%m-%Y %H:%M:%S")
                timestamp = calendar.timegm(time_tuple)
                Time_list_utc.append(timestamp)

                
        " Reading the different files in the path given below"            
        path = self.input_foldername #r'' # use your path
        allFiles = glob.glob(path + "/*.csv")
        frame = pd.DataFrame()
        list_ = []
        Time_stamp=pd.DataFrame()
        Time_all=[]


        "Reading the files from the path"
        for file_ in allFiles:    
            df = pd.read_csv(file_,index_col=None, header=0, delimiter = ';')
            
            if self.QCheckBox1.isChecked():
                df['Datum Uhrzeit'] = df[['Datum','Uhrzeit']].apply(lambda x : '{} {}'.format(x[0],x[1]), axis=1)  
                df = df.drop('Datum', 1)
                df = df.drop('Uhrzeit', 1)
                list_.append(df)             
            else: 
                list_.append(df)
               
        
        "Appending the different entries into the list"    
        frame = pd.concat(list_)
        frame1=frame.set_index("Datum Uhrzeit")
        Time_A= frame1.index.values.tolist()
               
        "Using the method for time format conversion"
        Time_list_utc=[]
        time_format()
        
#        "Time_Duplicates contains the index of the duplicate values on their second occurrence"
#        Time_duplicates = [i for i in range(len(Time_list_utc)) if not i == Time_list_utc.index(Time_list_utc[i])]
        
#        "All_time_duplicate_index contains the index of all the duplicate values in the list"
#        All_time_duplicate_index=[i for i, x in enumerate(Time_list_utc) if Time_list_utc.count(x) > 1]
        
        "Duplicate_tuples consists of the tuples of the duplicate indices into a list"
        Duplicate_tuples =[[Time_list_utc.index(Time_list_utc[i]),i] for i in range(len(Time_list_utc)) if not i == Time_list_utc.index(Time_list_utc[i])]
        #print(Duplicate_tuples)
        
        
        "Appending the time in UNIX format and the data according to the headers "
        for i in range(0,header_number,1):           
            eval('DataList'+str(i)+'').append(set(Time_list_utc))      
            eval('DataList'+str(i)+'').append(list(frame[header_names[i]]))
        
        "Creating the groups in the Project with the header names"        
        "Creating the dataset with the header names and appending the data into it"
        
        
        group_raw = file.create_group("Raw Data Groups")
        #group_time_stamps = file.create_group("Time Stamps Raw")    
        
        
        for i in range(header_number):
            d =(eval('DataList'+str(i)+''))
            "Dependencies to delete the duplicate values."
            for index in sorted(Duplicate_tuples, reverse = True):
                if math.isnan((d[1][index[0]])):
                    del d[1][index[0]] 
                else:
                    del (d[1][index[1]])               
            "List for converting the columns into rows"    
            x= list(map(list, zip(*d)))
            
        #    group_raw = file.create_group("Raw Data Groups")
            #group_sensors = group_raw.create_group("Raw_Data_"+header_names[i])
            dataset = group_raw.create_dataset(header_names[i], data= x) 
        Time_qwerty= (Time_list_utc)    
       # dataset_time= group_time_stamps.create_dataset("Time Stamps Raw data", data= Time_qwerty)

        file.close()
    
        
# If the program is run directly or passed as an argument to the python

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    gui = Window()
    gui.show()
    app.exec_()


