import os
import os.path
import sys
from sys import platform
import random
import csv
from csv import writer
class TCSVResult():
    def __init__(self,name="noname"):
        self.fname = ""
        self.folder = "RESULT"
        self.name = name
        self.dicts = []
    def Add(self,name,val):
        self.dicts.append((name,val ))
    def AddVariableToPrint(self,name,val):
        self.dicts.append((name,val ))
    def WriteResultToCSV(self,file='',folder="RESULT",fname=""):
        self.fname = fname
        self.folder = folder
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        if file=='':
            file = self.folder+ '/' + self.name + self.fname + ".csv" 
        dicts = self.dicts
        try:
            if os.path.isfile(file)==False:
                colnames = [i[0] for i in dicts]
                self.append_list_as_row(file,colnames)
            vals = [i[1] for i in dicts]
            self.append_list_as_row(file,vals)
            print("Results are saved at:", file)
        except Exception  as ex:
            print('Cannot write to file ', file ,'', ex);
            self.WriteResultToCSV(file + str(random.randint(0,1000000)) + '.csv')

    def append_list_as_row(self,file_name, list_of_elem):
        with open(file_name, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(list_of_elem)