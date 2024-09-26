import os
import pandas as pd

dirPath = r"repos\MarlinFirmware_Marlin\Features"

dirs = [f for f in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, f))]

for dir in dirs:
    featurePath = r"repos\MarlinFirmware_Marlin\Features" + "\\" + dir
    file = [
        f
        for f in os.listdir(featurePath)
        if os.path.isfile(os.path.join(featurePath, f))
    ]
    fileOpen = open(featurePath + r"\\" + file[0], "r")
    fileOpenTemp = open(featurePath + r"\\" + file[0][:-4] + "_Sorted.txt", "w")
    for x in fileOpen:
        fileOpenTemp.write(x)
        if "date: name (pull) (tag) (commit) (comment)" in x:
            break
    pulls = []
    for x in fileOpen:
        if x.strip():
            pulls.append([x[0:10],x])  
    df = pd.DataFrame(pulls, columns=["Date", "Text"])
    df["Date"] = pd.to_datetime(df["Date"],format="%d-%m-%Y")
    df.sort_values(by="Date", ascending=True, inplace=True)
    for ind in df.index:
        text = df["Text"][ind]
        text = text.rstrip()
        text = text + "\n"
        fileOpenTemp.write(text) # type: ignore
    fileOpen.close()
    fileOpenTemp.close()