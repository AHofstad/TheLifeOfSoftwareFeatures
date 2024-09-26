import subprocess
import os
from pathlib import Path
#Has to be placed in the root folder of the repository
#Requires a files.txt file containing all of the files that need to be checked
#Pull request number
pull = 0
Path("gitlogger/" + pull).mkdir(parents=True, exist_ok=True)

directory = os.fsencode("gitlogger/" + pull)
for file in os.listdir(directory):
    os.remove("gitlogger/" + pull + "/" + os.fsdecode(file))

input = open("files.txt", "r")
output = open("gitlogger/output.txt", "w")
lines = input.read().splitlines() 
for line in lines:
    print(line)
    splitLine = line.split("/")
    if len(splitLine) < 2:
        filename = splitLine[0].replace(".", "_")
    else:
        split1 = splitLine[-1]
        split2 = splitLine[-2]
        filename = split2 + "_" + split1.replace(".", "_")
        if os.path.exists("gitlogger/" + pull + "/" + filename + "_changes.txt"):
            if (len(splitLine)) < 3:
                filename = "other_" + filename
            else:
                split3 = splitLine[-3]
                filename = split3 + "_" + filename

    result = subprocess.run(["git", "--no-pager", "log", "-c", "-U10", line + ">", "gitlogger/" + pull + "/" + filename + "_changes.txt"], shell=True)
    # print(result)
    # input("Press Enter to continue...")
    # print(result.returncode)
    if result.returncode != 0:
        os.remove("gitlogger/" + pull + "/" + filename + "_changes.txt")
        if os.path.exists("gitlogger/" + pull + "/" + "OLD_" + filename + "_changes.txt"):
            filename = "other_" + filename
        subprocess.run(["git", "--no-pager", "log", "-c", "-U10", "--", line + ">", "gitlogger/" + pull + "/" + "OLD_" + filename + "_changes.txt"], shell=True)
        output.write(line + "\n")
        # input("Press Enter to continue...")