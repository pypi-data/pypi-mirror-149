import os
import pandas as pd
import copy
from datetime import date
import numpy as np

class TTable:
    def __init__(self):
        self.df_lists = {}
    def __pad_dict_list(self,dict_list, padel):
        lmax = 0
        for lname in dict_list.keys():
            lmax = max(lmax, len(dict_list[lname]))
        for lname in dict_list.keys():
            ll = len(dict_list[lname])
            if  ll < lmax:
                dict_list[lname] += [padel] * (lmax - ll)
        return dict_list
    def AddValue(self,sheetname, colname, value ):
        if sheetname in self.df_lists:
            if colname in self.df_lists[sheetname]:
                self.df_lists[sheetname][colname].append(value);
            else :
                self.df_lists[sheetname][colname] = [value]
        else :
            self.df_lists[sheetname] ={}
            if colname in self.df_lists[sheetname]:
                self.df_lists[sheetname][colname].append(value);
            else :
                self.df_lists[sheetname][colname] = [value]
    def SaveToExcel(self, filename,rownames = None):
        df_lists2 = copy.deepcopy(self.df_lists )
        sheet_names = [dict for dict in df_lists2 ] 
        col_names = [list(df_lists2[key].keys()) for key in sheet_names ] 

        
        #Padding empty values
        for name in sheet_names:
            list1 = df_lists2[name]
            self.__pad_dict_list(list1,'')
        #end padding
        df = [pd.DataFrame(df_lists2[i], columns =  col_names[sheet_names.index(i)]) for i in sheet_names]
        if rownames != None:
            name_rules = {i: rownames[i] for i in range(len(rownames)) }
            for i in range(len(df_lists2)):
                    df[i] = df[i].rename(index=name_rules)
        with pd.ExcelWriter(filename + '_'+str(date.today())+ '.xlsx') as writer: 
            for i in range(len(df_lists2)):
                df[i].to_excel(writer,sheet_name=sheet_names[i])

    def SaveToExcelFolder(self,folder, filename,rownames = None):
        if folder!='':
            if not os.path.exists(folder):
                os.makedirs(folder)
            filename = folder + "/" + filename
        self.SaveToExcel(filename,rownames)

    #def SetupSheetAndColum(self, sheetnames, colnames):
    #    self.df_lists = {}
    #    for i in sheetnames:
    #        self.df_lists[i] = {}
    #        for j in colnames:
    #            self.df_lists[i][j] = []
    def AddAColum(self,sheetname,colname,values):
        for val in values:
            self.AddValue(sheetname,colname,val)
    def MergeToMutipleSheetsExcel(self, list_of_file_tuple,colname_x, COLNAMES,colname_x_values=[]   ):
        if len(colname_x_values)<=0:
            colname_x_values = list_of_file_tuple[0][0][colname_x] 
        for i in COLNAMES:
            self.AddAColum(i,colname_x,colname_x_values)
            for j in list_of_file_tuple:
                col = j[0][i]
                self.AddAColum(i,j[1], col )
    def MergeToSingleSheetExcel(self, list_of_file_tuple,colname_x, COLNAMES,colname_x_values=None   ):
        for i in COLNAMES:
            if colname_x_values==None:
                colname_x_values = list_of_file_tuple[0][0][colname_x] 
            self.AddValue("full",colname_x,i)
            for j in list_of_file_tuple: self.AddValue("full",j[1], "" )
            self.AddValue("full",colname_x, colname_x )
            for j2 in list_of_file_tuple: self.AddValue("full",j2[1], j2[1] )
            self.AddAColum("full",colname_x,colname_x_values);  
            self.AddValue("full",colname_x,"Average"); self.AddValue("full",colname_x,"")
            for j in list_of_file_tuple:
                col = j[0][i]
                self.AddAColum("full",j[1], col )
                #print(type(col))
                self.AddValue("full",j[1], np.mean(col) );self.AddValue("full",j[1], "" )
    def DropRows(self, colname, values):
        sheet0 = self.df_lists[list(self.df_lists.keys())[0]][colname]
        for value in values:
            index = sheet0.index(value)
            for sheet in self.df_lists.values():
                for col in sheet.values():
                    col.pop(index)
    def AddAverageRow(self):
        keys_sheet =  self.df_lists.keys()
        for key_sheet in keys_sheet:
            sheet = self.df_lists[key_sheet]
            keys_col =  sheet.keys()
            for key_col in keys_col:
                col = sheet[key_col]
                if type(col[0]) == str: average = 'Average'
                else :average = np.nanmean(col)
                self.AddValue(key_sheet,key_col,average) 
    def AddAverageCol(self):
        keys_sheet =  self.df_lists.keys()
        for key_sheet in keys_sheet:
            sheet = self.df_lists[key_sheet]
            n =  len(sheet[list(sheet.keys())[0]])
            averages=[]
            for i in range(n):
                row = self.GetARowByIndex(key_sheet,i)
                averages.append(np.nanmean( row))
            self.AddAColum(key_sheet,'Average',averages)
    def GetARowByIndex(self, sheetname, index, remove_nonnumber=True ):
        sheet = self.df_lists[sheetname]
        row = [col[index] for col in sheet.values()]
        if remove_nonnumber:
            row = [i for i in row if type(i) != str ]
        return row
            


