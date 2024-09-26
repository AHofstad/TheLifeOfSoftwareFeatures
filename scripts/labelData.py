#To append to a pickle file
from github import Github
from github import IssueComment
import pickle
import os
import re
import time
import csv
import pandas as pd
import ast

def labelDataFeatures(name, labelList, type, logger):
    start = time.time()
    reponame = name.rstrip()
    logger.info(reponame + " labelDataFeatures")
    repofolder = "repos/" + reponame.replace("/", "_")
    repofile = repofolder + "/" + type
    repotext = repofolder + "/text"
    if not os.path.exists("repos"):
        os.mkdir("repos")
    if not os.path.exists(repofolder):
        os.mkdir(repofolder)
    if not os.path.exists(repofile):
        os.mkdir(repofile)
    if not os.path.exists(repotext):
        os.mkdir(repotext)    
        
    if type == "pullrequest":
        csvFile = pd.read_csv(repotext + "/pullResults.csv")
    else:
        csvFile = pd.read_csv(repotext + "/issueResults.csv")
    csvFile['Labels'] = csvFile['Labels'].apply(lambda x: ast.literal_eval(x))
    labeledData = csvFile[csvFile["Labels"].str.len() != 0]
    finalData = []
    for index, row in labeledData.iterrows():
        found = False
        for label in row["Labels"]:
            for labels in labelList:
                if labels in label.lower():
                    finalData.append(row)
                    found = True
                    break
            if found:
                break        
    finalData = pd.DataFrame(finalData)
    startCSV = time.time()
    if type == "pullrequest":
        finalData.to_csv(repotext + "/pullFeatures.csv", index=False)
        mergedFeaturesPD = finalData[finalData.Merged == True]
        mergedFeaturesPD.to_csv(repotext + "/pullMergedFeatures.csv", index=False)
        notMergedFeaturesPD = finalData[finalData.Merged != True]
        notMergedFeaturesPD.to_csv(repotext + "/pullNotMergedFeatures.csv", index=False)
        labeledData.to_csv(repotext + "/pullLabeled.csv", index=False)
        mergedDataPD = csvFile[csvFile.Merged == True]
        mergedDataPD.to_csv(repotext + "/pullMerged.csv", index = False)
        nonMergedDataPD = csvFile[csvFile.Merged != True]
        nonMergedDataPD.to_csv(repotext + "/pullNotMerged.csv", index = False)
    else:
        finalData.to_csv(repotext + "/issueFeatures.csv", index=False)
        labeledData.to_csv(repotext + "/issueLabeled.csv", index=False)

    end = time.time()
    logger.info(f'csv time: {end-startCSV}')   
    end = time.time()
    logger.info(f'total time: {end-start}')
    logger.info("--------------------------")
    
def labelDataBugs(name, labelList, notLabelList, type, logger):
    start = time.time()
    reponame = name.rstrip()
    logger.info(reponame + " labelDataBugs")
    repofolder = "repos/" + reponame.replace("/", "_")
    repofile = repofolder + "/" + type
    repotext = repofolder + "/text"
    if not os.path.exists("repos"):
        os.mkdir("repos")
    if not os.path.exists(repofolder):
        os.mkdir(repofolder)
    if not os.path.exists(repofile):
        os.mkdir(repofile)
    if not os.path.exists(repotext):
        os.mkdir(repotext)    
        
    if type == "pullrequest":
        csvFile = pd.read_csv(repotext + "/pullResults.csv")
    else:
        csvFile = pd.read_csv(repotext + "/issueResults.csv")
    csvFile['Labels'] = csvFile['Labels'].apply(lambda x: ast.literal_eval(x))
    labeledData = csvFile[csvFile["Labels"].str.len() != 0]
    finalData = []
    for index, row in labeledData.iterrows():
        found = False
        notBug = False
        for label in row["Labels"]:
            for notLabels in notLabelList:
                if notLabels in label.lower():
                    notBug = True
                    break
            if notBug:
                break
            for labels in labelList:
                if labels in label.lower():
                    finalData.append(row)
                    found = True
                    break
            if found:
                break        
    finalData = pd.DataFrame(finalData)
    startCSV = time.time()
    if type == "pullrequest":
        finalData.to_csv(repotext + "/pullBugs.csv", index=False)
    else:
        finalData.to_csv(repotext + "/issueBugs.csv", index=False)
    end = time.time()
    logger.info(f'csv time: {end-startCSV}')   
    end = time.time()
    logger.info(f'total time: {end-start}')
    logger.info("--------------------------")