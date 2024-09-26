import os
import pandas as pd
import json

dirPath = "repos\MarlinFirmware_Marlin\Features"

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
fields = [
    "Pull",
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

csvFile = pd.DataFrame(columns=fields)

dirs = [f for f in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, f))]

for dir in dirs:
    values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    featurePath = r"repos\MarlinFirmware_Marlin\Features" + "\\" + dir
    file = [
        f
        for f in os.listdir(featurePath)
        if os.path.isfile(os.path.join(featurePath, f))
    ]
    fileOpen = open(featurePath + r"\\" + file[0], "r")
    for x in fileOpen:
        for y in range(len(labelList)):
            if labelList[y].lower() in x.lower():
                values[y] += 1
    rowsPD = [
        dir,
        values[0],
        values[1],
        values[2],
        values[3],
        values[4],
        values[5],
        values[6],
        values[7],
        values[8],
        values[9],
        values[10],
    ]

    csvFile.loc[len(csvFile)] = rowsPD

values = {
    "$NewFeature": sum(csvFile["$NewFeature"].tolist()), 
    "$BugFix": sum(csvFile["$BugFix"].tolist()),
    "$Enhancement": sum(csvFile["$Enhancement"].tolist()),
    "$Refactor": sum(csvFile["$Refactor"].tolist()),
    "$Revert": sum(csvFile["$Revert"].tolist()),
    "$Rework": sum(csvFile["$Rework"].tolist()),
    "$Cleanup": sum(csvFile["$Cleanup"].tolist()),
    "$Comment": sum(csvFile["$Comment"].tolist()), 
    "$Formatting": sum(csvFile["$Formatting"].tolist()),            
    "$Whitespace": sum(csvFile["$Whitespace"].tolist()),           
    "$Removal": sum(csvFile["$Removal"].tolist()), 
}

with open("commitCount.json", 'w') as fp:
    json.dump(values, fp, indent=4)

# print(values)
# fig, ax = plt.subplots()

# plt.bar(list(values.keys()), list(values.values()))

# plt.show()
csvFile["Sum"] = csvFile.sum(axis=1, numeric_only=True)
csvFile.sort_values(["Pull"], inplace=True)
csvFile.sort_values(["Sum"], ascending=False, inplace=True)
csvFile.to_csv("FeatureResults.csv", index=False)
csvFile.head(10).to_csv("FeatureResultsHead.csv", index=False)
