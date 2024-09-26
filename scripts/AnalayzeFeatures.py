from github import Github
from github import Auth
import os
import pandas as pd
import re
import json
import datetime
from collections import Counter

auth = Auth.Token(
    #Github token
)
g = Github(auth=auth)

repo = g.get_repo("MarlinFirmware/Marlin")

#Date done collecting data

dateDone = datetime.datetime(2024, 8, 9)

#All labels matched together with a number for array indexing

labelDict = {
    "($NewFeature)": 0,
    "($BugFix)" : 1,
    "($Enhancement)": 2,
    "($Refactor)": 3,
    "($Revert)": 4,
    "($Rework)": 5,
    "($Cleanup)": 6,
    "($Comment)": 7,
    "($Formatting)": 8,
    "($Whitespace)": 9,
    "($Removal)": 10
}

#All labels in list Form

labelList = [
    "$NewFeature",
    "$BugFix",
    "$Enhancement",
    "$Refactor",
    "$Revert",
    "$Rework",
    "$Cleanup",
    "$Comment",
    "$Formatting",
    "$Whitespace",
    "$Removal"
]

ListUn = ["($Whitespace)", "($Comment)", "($Formatting)", "($Cleanup)"]
ListIm = ["($BugFix)", "($Enhancement)", "($Refactor)", "($Revert)", "($Rework)"]

#Path to all the processed Features of Marlin

dirPath = r"repos\MarlinFirmware_Marlin\Features"

dirs = [f for f in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, f))]

#List containing a tuple of the Hash and its Label
hashesLabel = []
#Dictionary containing the Hash and the commit message
hashesStringDict = {}
#Dictionary containing the feature and all the commits associated with it
featureHashDict = {}
#Dictionary containing the feature and its information
featureInfoDict = {}
#Dictionary containing all the features and the commit times and label
featureCommitTimeDict = {}  

for folder in dirs:
    print(folder)
    pull = repo.get_pull(int(folder[1:]))
    featurePath = r"repos\MarlinFirmware_Marlin\Features" + "\\" + folder
    file = [
        f
        for f in os.listdir(featurePath)
        if os.path.isfile(os.path.join(featurePath, f))
    ]
    print(file)
    fileOpen = open(featurePath + "\\" + file[1], "r")
    hashList = []
    createdAt = fileOpen.readline()[9:].strip()
    mergedAt = fileOpen.readline()[7:].strip()
    createdAt = datetime.datetime.strptime(createdAt, "%d-%m-%Y")
    mergedAt = datetime.datetime.strptime(mergedAt, "%d-%m-%Y")
    timePassed = (mergedAt-createdAt).days
    fileOpen.readline()
    comments = int(fileOpen.readline()[10:])
    filesChanged = -2
    for x in fileOpen:
        if "date:" in x:
            break
        filesChanged += 1    
    
    featureCommitTimeList = []
    
    commits = 0
    commitsUn = 0
    commitsIm = 0
    for x in fileOpen:
        
        resultHash = re.search(r"\(([a-z0-9]{40})\)", x)
        if resultHash:
            commits += 1
            resultLabel = re.search(r"\(\$.{4,15}\)", resultHash.string)
            if resultLabel.group(0) == "($NewFeature)":
                newHash = resultHash.group(0)[1:-1]
            if resultLabel.group(0) in ListUn:
                commitsUn +=1
            else:
                commitsIm +=1
            date = str(datetime.datetime.strptime(resultHash.string[:10], "%d-%m-%Y"))[:10]
            featureCommitTimeList.append((date, resultLabel.group(0)))
            resultString = str(re.search(r".+?(?=\(\$)", resultHash.string).group(0).strip())
            hashesLabel.append((resultHash.group(1), resultLabel.group(0)))
            hashList.append((resultHash.group(0), resultLabel.group(0)))
    featureCommitTimeDict[folder] = featureCommitTimeList
    timeSinceChange = (dateDone - datetime.datetime.strptime(featureCommitTimeDict[folder][-1][0], "%Y-%m-%d")).days
    featureInfoDict[folder] = (newHash, str(createdAt)[:10], str(mergedAt)[:10], timePassed, comments, filesChanged, commits, commitsIm, commitsUn, pull.additions, pull.deletions, pull.additions-pull.deletions, timeSinceChange)
    featureHashDict[folder] = hashList

featureInfoPD = pd.DataFrame.from_dict(featureInfoDict, orient="index", columns=["Hash", "Created", "Merged", "DifferenceCAndM", "Comments", "FilesChanged", "Commits", "CommitsIm", "CommitsUn", "Additions", "Deletions", "TotalChange", "LastChange"])
featureInfoPD = featureInfoPD.sort_values("TotalChange", ascending=False)
featureInfoPD.to_csv("FeatureInfo.csv", index_label="Pull")

featureCommitTimePD = pd.DataFrame.from_dict(featureCommitTimeDict, orient="index")
featureCommitTimePD.to_csv("FeatureCommitTime.csv", index_label="Pull")

with open("featureCommitTime.json", 'w') as fp:
    json.dump(featureCommitTimeDict, fp, indent=4)

#Dictionary containing the hashes of the commits and the features it is present in together with its label
hashFeatureDict = {}

for x in featureHashDict:
    for y in featureHashDict[x]:
        if y[0][1:-1] in hashFeatureDict:
            featurelist = hashFeatureDict[y[0][1:-1]]
            featurelist.append((x, y[1]))
            hashFeatureDict[y[0][1:-1]] = featurelist
        else: 
            featurelist = []
            featurelist.append((x, y[1]))
            hashFeatureDict[y[0][1:-1]] = featurelist
            
with open("featureHash.json", 'w') as fp:
    json.dump(featureHashDict, fp, indent=4)
            
with open("hashFeature.json", 'w') as fp:
    json.dump(hashFeatureDict, fp, indent=4)

sortedHashes = Counter(hashesLabel)

hashDict = {}
for x in hashesLabel:
    if x[0] in hashDict:
        values = hashDict[x[0]]
        values[labelDict[x[1]]] = values[labelDict[x[1]]] + 1
        hashDict[x[0]] = values
    else:
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        values[labelDict[x[1]]] += 1
        hashDict[x[0]] = values
    

hashesPD = pd.DataFrame.from_dict(hashDict, orient="index", columns=labelList)
hashesPD["TotalCount"] = hashesPD.sum(axis=1)
hashesPD = hashesPD.sort_values("TotalCount", ascending=False)
hashesPD.to_csv("HashesResults.csv", index_label="Hash")

hashesMultipleLabels = []
for x in hashDict:
    if sum(1 for n in hashDict[x] if n != 0) > 1:
        hashesMultipleLabels.append(x)
    
hashesFilteredPD = hashesPD.filter(items=hashesMultipleLabels, axis=0).sort_values("TotalCount", ascending=False)
hashesFilteredPD.to_csv("HashesResultsMultipleLabels.csv", index_label="Hash")