#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import datetime
import csv, random, re, math, sys, os, webbrowser, shutil
import numpy as np

import matplotlib.pyplot as plt

import plotly.graph_objects as go

import seaborn as sn

from pivottablejs import pivot_ui

sn.set(rc = {'figure.figsize':(20,10)})
plt.rcParams["figure.figsize"] = (20,10)



def translateEntry(df,metaData,chemName,DEBUG=False):
    Entry = re.split(" |=",df[chemName])
    #EffectName = df["preferred name"].split(":")
    EffectName = [df["preferred name"][:3], df["preferred name"][3:]]
    Effect = [Entry[1],int(Entry[3])] # Effect that is being indexed, positive 1 or negative (not present) 0
    Mag = float(Entry[4][1:][:-1]) # magnitude of effect compared to nearest neighbours (other columns)
    AUC = float(Entry[6]) # Area Under Curve, measure for accuracy
    p_Val = float(Entry[8]) # p-value, confidence interval. Lower is better
    EffectName.append(int(Entry[3]))
    EffectName.append(Mag)
    EffectName.append(AUC)
    EffectName.append(p_Val)
    df.drop(chemName)
    if DEBUG:
        print(EffectName)
        print(Entry)
        print("--** Effect:{} -- Mag:{} -- AUC:{} -- P-Value:{} **--".format(Effect, Mag, AUC, p_Val))
    thresholdSimilarityVector = []
    thresholdSimilaritySum = 0
    for i,x in enumerate(df[2:]):
        mgkgday = re.findall('\d*\.?\d+',x) # Filter out thresholds in mg/kg/day (I assume mg compound to kg body weight per day)
        if len(mgkgday) ==  0: # no number detected
            mgkgday = 0.0
        else:
            mgkgday = float(mgkgday[0])
        mgkgday /= float(metaData.iloc[2][i+2]) # divide by similarity index; higher similarity means chemical/toxilogical fingerprint is more similar. Range will be bigger if more uncertainty
        thresholdSimilarityVector.append(mgkgday)
        thresholdSimilaritySum += mgkgday*Mag
    thresholdSimilarityVector.append(thresholdSimilaritySum)
    if DEBUG:
        print(thresholdSimilarityVector)
    return EffectName+thresholdSimilarityVector

def computeHealthIndex(fileName,DEBUG=False):
    genRAData = pd.read_csv("{}.csv".format(fileName), header=1)
    metaData = genRAData[:3]
    chemName = metaData.columns[1]
    genRAData = genRAData[3:]
    if DEBUG:
        print(metaData)
        print("Test translation:")
        translateEntry(genRAData.iloc[0],metaData,chemName,DEBUG=DEBUG)
        print(translateEntry(genRAData.iloc[random.randrange(len(genRAData))],metaData,chemName,DEBUG=DEBUG))
    healthIndexData = []
    effectLabels = []
    targetLabels = []
    for i in genRAData.iloc:
        healthIndexData.append(translateEntry(i,metaData,chemName))
        effectLabels.append(healthIndexData[-1][0])
        targetLabels.append(healthIndexData[-1][1])
    return healthIndexData ,list(set(effectLabels)), list(set(targetLabels)), metaData, chemName


# In[23]:


def plotResult(table, df, FileNames):
    chemicals = []
    for i in FileNames:
        chemicals.append(i.split("_")[1])
    sn.heatmap(table, linewidths=.0).figure.savefig('Heatmap_All.png')

    fig = go.Figure(go.Bar(y=df[df.Formula == chemicals[0]]["positive targets decimal"].values, x=df[df.Formula == chemicals[0]]["Effectgroup"].values, text=chemicals[0]))
    for i in chemicals[1:]:
        fig.add_trace(go.Bar(y=df[df.Formula == i]["positive targets decimal"].values, x=df[df.Formula == i]["Effectgroup"], name=i))
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(height=800, width=3000,uniformtext_minsize=8, uniformtext_mode='hide', barmode='stack', xaxis={'categoryorder':'total descending'})
    fig.write_image("Chemicals-Effectgroup_bar.png")
    fig.show()


    TargetEffectLabels
    fig = go.Figure(go.Bar(y=df[df.Testgroup == TargetEffectLabels[0][0]]["positive targets decimal"].values, x=df[df.Testgroup == TargetEffectLabels[0][0]]["Effectgroup"].values, text=TargetEffectLabels[0][0]))
    for i in TargetEffectLabels[1:]:
        fig.add_trace(go.Bar(y=df[df.Testgroup == i[0]]["positive targets decimal"].values, x=df[df.Testgroup == i[0]]["Effectgroup"], name=i[0]))
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(height=800, width=3000,uniformtext_minsize=8, uniformtext_mode='hide', barmode='stack', xaxis={'categoryorder':'total descending'})
    fig.write_image("Testgroup-Effectgroup_bar.png")
    fig.show()



    fig = go.Figure(data=go.Scatter3d(
        x=df["Effectgroup"],
        y=df["Formula"],
        z=df['Testgroup'],
        text=df['positive targets decimal'],
        mode='markers',
        marker=dict(
            sizemode='diameter',
            sizeref=0.5,
            size=df['positive targets decimal'],
            color = df['total targets'],
            colorscale = 'Viridis',
            colorbar_title = 'decimal<br>targets',
            line_color='rgb(140, 140, 170)'
        )
    ))
    fig.update_layout(height=1000, width=2000,title='Effectgroup Vs testgroup Vs chemical, size denotes sum of positive targets, color denotes amount of targets')
    fig.write_image("3D_plot.png")
    fig.show()



    fig = go.Figure(go.Histogram2d(
            x=df["Effectgroup"],
            y=df["positive targets decimal"]
        ))
    fig.update_layout(height=1600, width=1600)
    fig.write_image("Effectgroup_score.png")
    fig.show()
    fig = go.Figure(go.Histogram2d(
            x=df["Testgroup"],
            y=df["positive targets decimal"]
        ))
    fig.write_image("Testgroup_score.png")
    fig.show()
    fig = go.Figure(go.Histogram2d(
            x=df["Formula"],
            y=df["positive targets decimal"]
        ))
    fig.write_image("Chemical_score.png")
    fig.show()


# In[25]:


def df_normalize(df):
    return df/df.max()

TargetEffectLabels = [["MGR"],["REP"],["DEV"],["CHR"],["SUB"],["SAC"]]
def TrackTargetEffectLabels(HID,Labels):
    for i in HID:
        for j,x in enumerate(Labels):
            if i[0] == x[0]:
                Labels[j].append(i[1][1:])
    for i,x in enumerate(Labels):
        TestType = x[0]
        x.remove(TestType)
        x.sort()
        Labels[i] = [TestType]+list(set(x))
    return Labels

def metaDataGenEffects(effectLabels, HID):
    metaDataHID = []
    for i,x in enumerate(effectLabels):
        Labs = [0,0,0,0,0]
        for j,y in enumerate(HID):
            if x == y[0]: # Is labeled similar
                Labs[0] += 1
                Labs[1] += y[2]
                Labs[2] += y[3]
                Labs[3] += y[-1]
                Labs[4]  = y[0]
        metaDataHID.append(Labs)
    return metaDataHID

def metaDataGenTargets(targetLabels, HID):
    metaDataHID = []
    for i,x in enumerate(targetLabels):
        Labs = [0,0,0,0,0,0]
        for j,y in enumerate(HID):
            if x == y[1]: # Is labeled similar
                Labs[0] += 1
                Labs[1] += y[2]
                Labs[2] += y[3]
                Labs[3] += y[-1]
                Labs[4]  = y[1]
                Labs[5]  = y[0] # But save testgroup data! so we get a very complete dataset :).
        metaDataHID.append(Labs)
    return metaDataHID

def metaDataReport(effectLabels,metaDataHID,md,label):
    print(md)
    FileName = "{}_{}_metadata.csv".format(label,md.columns[1])
    md.to_csv(FileName)
    Header = ["Effectgroup","total targets", "positive targets", "positive targets decimal", "weighted and averaged limit [mg/kg/day]"]
    with open(FileName, 'a', newline='') as f:
        Writer = csv.writer(f)
        Writer.writerow(Header)
        for i, x in enumerate(effectLabels):
            print("{} - total targets: {} - Targets positive: {} - Total targets decimal: {:.2f} - weighted and averaged limit {:.2f} [mg/kg/day]".format(x,metaDataHID[i][0],metaDataHID[i][1],metaDataHID[i][2],metaDataHID[i][3]))
            Writer.writerow([x]+metaDataHID[i])
        f.close()



def BatchReport(fileNames, filename, fcn="sum", viz = False, ext = False):
    Header = ["Formula","Name","total targets", "positive targets", "positive targets decimal", "weighted and averaged limit [mg/kg/day]","Effectgroup"]
    TargetEffectLabels = [["MGR"],["REP"],["DEV"],["CHR"],["SUB"],["SAC"]]
    MetaBlobs = []
    analogBlobs = []
    TargetBlobs = []
    compoundNames = []
    for label in fileNames:
        #label = "genra_O3"
        HID, effectLabels, targetLabels, md, Compound = computeHealthIndex(label)#Ozone
        compoundNames.append(Compound)
        metaDataHID = metaDataGenEffects(effectLabels, HID)
        metaDataHIDt = metaDataGenTargets(targetLabels,HID)
        metaDataReport(effectLabels,metaDataHID,md,label)
        TargetEffectLabels = TrackTargetEffectLabels(HID,TargetEffectLabels)
        TargetBlobs.append(metaDataHIDt)
        MetaBlobs.append(metaDataHID)
        analogBlobs.append(md)

    with open("{}_Meta.csv".format(filename), "w", newline='') as f:
        Writer = csv.writer(f)
        Writer.writerow(Header)
        for i,Blob in enumerate(MetaBlobs):
            for lines in Blob:
                print(lines)
                Writer.writerow([fileNames[i].split("_")[1],compoundNames[i]]+lines)
        f.close()

    with open("{}_Target.csv".format(filename), "w", newline='') as f:
        Writer = csv.writer(f)
        Header.append("Testgroup")
        Writer.writerow(Header)
        for i,Blob in enumerate(TargetBlobs):
            for lines in Blob:
                print(lines)
                Writer.writerow([fileNames[i].split("_")[1],compoundNames[i]]+lines)
        f.close()
    df = pd.read_csv("Batch_Report_Target.csv")#Read the just made file back into DF to use pivottables
    nan_value = float("NaN")
    df.replace("", nan_value, inplace=True)
    df.replace(nan_value, 0,  inplace=True)

    if ext:
        IDX = ['Effectgroup']
        IDY = ['Formula',"Testgroup"]
    else:
        IDX = ['Formula']
        IDY = ['Testgroup']

    if fcn == "sum":
        table = pd.pivot_table(df, values='positive targets decimal', index=IDX,columns=IDY, aggfunc=np.sum)
    elif fcn == "avg":
        table = pd.pivot_table(df, values='positive targets decimal', index=IDX,columns=IDY, aggfunc=np.average)
    else:
        table = pd.pivot_table(df, values='positive targets decimal', index=IDX,columns=IDY, aggfunc=np.mean)
    table.replace("", nan_value, inplace=True)
    table.replace(nan_value, 0,  inplace=True)
    table = df_normalize(table)
    table.to_csv("AEI_Norm.csv")
    if viz:
         print("visualizing dataset")
         plotResult(table, df, fileNames)
    return MetaBlobs, TargetBlobs, analogBlobs, table, df

# One gas GenRA file analysis
def OneGas(Filename="genra_O3"):
    label = Filename
    HID, effectLabels, targetLabels, md = computeHealthIndex(label)#Ozone
    metaDataHID = metaDataGenEffects(effectLabels, HID)
    metaDataHIDt = metaDataGenTargets(targetLabels,HID)
    metaDataReport(effectLabels,metaDataHID,md,label)
    TargetEffectLabels = TrackTargetEffectLabels(HID,TargetEffectLabels)


def ArgChecker(Args): # Argument checker; if boolean is put in dict, it is treated as a flag. Any other type will be treated as string.
    Dict = {"filename":"Batch_Report","viz":False,"pivot":"Batch_Report_Target.csv","fcn":"sum","piv":False,"help":False,"Run":False,"CopyExamples":False,"ext":False}
    for i in Args:
        i0 = i.split("=")
        if i0[0] in Dict.keys():
            if Dict[i0[0]] == False: # Boolean switch detector. If flag is detected, flip value in dict.
                 Dict[i0[0]] = True
            else: # i has been split at the = sign, so this will contain the arg.
                 Dict[i0[0]] =  i0[1] # If argument is not a boolean, it MUST contain an argument, and here we use pattern arg=value.
                 if(i0[0] == "pivot"):
                     Dict["piv"] = True
                 if(i0[0] == "filename"):
                     Dict["Run"] = True
        else:
            print("********** Error, didn't recognize {} ***********".format(i))
            print("possible arguments are:")
            for i in Dict.keys():
                print("arg:  {}  - {}".format(i,Dict[i]))
            print("********** try again ***********")
            break;
    return Dict

# Example Execution
def main():
    args = sys.argv
    Files = checkFolder(os.listdir())

    ControlDict = ArgChecker(args[1:])
    if ControlDict["CopyExamples"]:
        CopyExamples()
    if ControlDict["Run"] and not ControlDict["help"]:
        if len(Files) > 0:
            print("Running AEI")
            MetaBlobs, TargetBlobs, analogBlobs, PVTable, target_DF = BatchReport(Files,filename=ControlDict["filename"],viz=ControlDict["viz"],fcn=ControlDict["fcn"],ext=ControlDict["ext"])
        else:
             print("No suitable files found in this directory!")
    elif ControlDict["piv"] and not ControlDict["help"]:
        print("Pivot")
        PivotTable(ControlDict["pivot"])
    elif ControlDict["help"]:
        print("Run this script in a folder with genra_<chemical>.csv files.")
        print("Use the flags shown below to control the output")
        print("Argument fcn= sum, avg, med for the different normalization schemes")
        print("Argument pivot=file.csv flag to open a .html interactive pivot table in your browser. This works for any .csv with categorical data (text flags in rows)")
        print("Argument viz generates 6 graphs to aid in data analysis.")
        print("Argument Run runs the script with default filenames in the current folder.")
        print("Argument ext exports an extended dataformat which is not compatible with the AEI paraview macro.")
        print("possible arguments are:")
        for i in ControlDict.keys():
            print("arg:  {}  - {}".format(i,ControlDict[i]))
    # fileNames = ["genra_O3","genra_C10H16O2","genra_C8H14O","genra_CH3CHO","genra_C10H16","genra_N2","genra_CO2","genra_CH2O"]
    #compoundNames = ["Ozone","3-Isopropenyl-6-oxo-heptanal",etc..]# Will be loaded from metadata now.

def CopyExamples():
    List = ["AEI.py","genra_C10H16.csv","genra_CH2O.csv","genra_O3.csv"]
    script_dir = "/".join(__file__.split("/")[:-1]) # root dir where script resides, with example files
    directory_path = os.getcwd()
    for i in List:
        print("Copying:   {}/{}".format(script_dir,i))
        print("To:        {}/{}".format(directory_path,i))
        print("-"*20)
        shutil.copy("{}/{}".format(script_dir,i), "{}/{}".format(directory_path,i))

def checkFolder(F):
    NF = []
    for i in F:
        if i.split("_")[0] == "genra" and len(i.split("_")) == 2:
            NF.append(i.split(".")[0])
    return NF

def PivotTable(File):
    pivot_ui(pd.read_csv(File))
    directory_path = os.getcwd()
    webbrowser.open(directory_path+"/pivottablejs.html", new=2)

if __name__ == "__main__":
    print(("%s is being run directly" % __name__))
    try:
        main()
    except RuntimeError:
        print("Error")
        os._exit(os.EX_OK)
else:
    print("---\n{}\n---\nis being imported\n---".format(sys.argv[0]))
