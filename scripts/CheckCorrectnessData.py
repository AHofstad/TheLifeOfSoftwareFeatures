import os
import re


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

#Path to all the processed Features of Marlin
dirPath = "repos\MarlinFirmware_Marlin\Features"

dirs = [f for f in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, f))]

wrongLines = []

for folder in dirs:
    featurePath = dirPath + "\\" + folder
    file = [
        f
        for f in os.listdir(featurePath)
        if os.path.isfile(os.path.join(featurePath, f))
    ]
    fileOpen = open(featurePath + "\\" + file[0], "r")
    
    for x in fileOpen:
        if "date:" in x:
            break
    
    list
    
    for x in fileOpen:
        resultHash = re.search("\(([a-z0-9]{40})\)", x)
        if resultHash:
            resultLabel = re.search("\(\$.{4,15}\)", resultHash.string)
            if resultLabel:
                if resultLabel.group(0)[1:-1] not in labelList:
                    wrongLines.append(("Malformed Label", folder, x))
            else:
                wrongLines.append(("Label", folder, x))
        else:
            wrongLines.append(("Hash", folder, x))
    
print(wrongLines)

with open(dirPath + "\wrongLines.txt", "w") as f:
    for line in wrongLines:
        f.write(f"{line}\n")