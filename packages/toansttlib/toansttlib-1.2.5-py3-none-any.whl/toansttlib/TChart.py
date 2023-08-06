import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import ntpath
import numpy as np
import math
import matplotlib as mpl

markers = ['o','s','*','x','.','d','^','+','_','.']
lines = ['-','--','-.',':']
def fmta(i=-2):
	global fmti;
	if i == -1:
		fmti =i
	fmti+=1;
	return fmt(fmti);
def fmt(i): return markers[i%len(markers)] + lines[i%len(lines)]

def DrawSubFigure_SimpleLine(ax,x,ys,title='',x_title='',y_title='', is_log=0,smooth1=0,smooth2=0,titlefontsize=10,markersize=3,linewidth=1):
    ls = []
    for y in ys:
        if smooth1==0 or smooth2==0:
            l,=ax.plot(x, y, fmta(), markersize=markersize,linewidth=linewidth)
        else:
            l,=ax.plot(x, savgol_filter(y,smooth1,smooth2), fmta(), markersize=markersize,linewidth=linewidth)
        ls.append(l)
    if is_log==1: ax.set_xscale('log')
    if title !='': ax.set_title(title, fontsize=titlefontsize)
    if x_title!='': ax.set_xlabel(x_title, fontsize=titlefontsize-1)
    if y_title!='': ax.set_ylabel(y_title, fontsize=titlefontsize-1)
    return ls

def DrawSubFigure_Line(ax,dfs,x_label,y_label,title='',x_title='',y_title='', is_log=0,smooth1=0,smooth2=0,yscale=1.0):
    fmta(-1);#ax=axs[0,0];
    ls = []
    for i in dfs:
        if smooth1==0 or smooth2==0:
            l,=ax.plot(x, i[y_label]*yscale, fmta(), markersize=markersize,linewidth=linewidth)
        else:
            l,=ax.plot(i[x_label], savgol_filter(i[y_label]*yscale,smooth1,smooth2), fmta(), markersize=markersize,linewidth=linewidth)
        ls.append(l)
    if is_log==1: ax.set_xscale('log')
    if title !='': ax.set_title(title, fontsize=titlefontsize)
    if x_title!='': ax.set_xlabel(x_title, fontsize=titlefontsize-1)
    if y_title!='': ax.set_ylabel(y_title, fontsize=titlefontsize-1)
    return ls
def DrawSubFigureLog_Line(ax,dfs,x_label,y_label,title='',x_title='',y_title='', is_log=0,smooth1=0,smooth2=0,yscale=1.0):
    fmta(-1);#ax=axs[0,0];
    ls = []
    xx=0
    for i in dfs:
        xx= i[x_label]
        x = [int(math.log(ii)/math.log(2)) for ii in i[x_label]]
        if smooth1==0 or smooth2==0:
            l,=ax.plot(x, i[y_label]*yscale, fmta(), markersize=markersize,linewidth=linewidth)
        else:
            l,=ax.plot(i[x_label], savgol_filter(i[y_label]*yscale,smooth1,smooth2), fmta(), markersize=markersize,linewidth=linewidth)
        ls.append(l)
    labels = [item.get_text() for item in ax.get_xticklabels()]
    print(labels)
    labels[1] =2
    for i in range(len(xx)):
        labels[i+2] = xx[i]
    ax.set_xticklabels(labels)
    if title !='': ax.set_title(title, fontsize=titlefontsize)
    if x_title!='': ax.set_xlabel(x_title, fontsize=titlefontsize-1)
    if y_title!='': ax.set_ylabel(y_title, fontsize=titlefontsize-1)
    return ls