import os
import re

dirPath = r"repos\MarlinFirmware_Marlin\Features"

dirs = [f for f in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, f))]

d = {}

for dir in dirs:
    values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    featurePath = r"repos\MarlinFirmware_Marlin\Features" + "\\" + dir
    file = [
        f
        for f in os.listdir(featurePath)
        if os.path.isfile(os.path.join(featurePath, f))
    ]
    fileOpen = open(featurePath + r"\\" + file[0], "r")
    for x in fileOpen:
        result = re.search(r"\(\$(.*)\) \(", x)
        if result:
            # print(result.group(1))
            if result.group(1) in d:
                d[result.group(1)] = d[result.group(1)] + 1
            else:
                d[result.group(1)] = 1
print(d)
with open(r"repos\MarlinFirmware_Marlin\Features\defects.txt", "w") as defectsFile:
    for key, value in d.items():
        defectsFile.write('%s:%s\n' % (key, value))
            # print(x)
        # for y in range(len(labelList)):
        #     if labelList[y].lower() in x.lower():
        #         values[y] += 1
