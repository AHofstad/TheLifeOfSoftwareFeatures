from pathlib import Path
import re
from github import Github
from github import Auth

auth = Auth.Token(
    #Git AUTH token
)
g = Github(auth=auth)

repo = g.get_repo("MarlinFirmware/Marlin")

pullRequestNumbersList = [27404]

for x in pullRequestNumbersList:
    pull = repo.get_pull(x)
    pullRequestName = pull.title
    pullRequestName = re.sub(r'[^\w_. -]', '_', pullRequestName)
    pullRequestNumber = "#" + str(x)
    
    pathToGitlog = Path( "repos/MarlinFirmware_Marlin/Features/" + pullRequestNumber + "/gitlog")
    pathToGitlog.mkdir(parents=True, exist_ok=True)
    
    createdAt = "Created: " + pull.created_at.strftime("%d-%m-%Y")
    mergedAt = "Merged: " + pull.merged_at.strftime("%d-%m-%Y")
    pullLine = "Pull: " + pullRequestNumber
    comments = "Comments: " + str(pull.comments)
    filesList = pull.get_files()
    
    with open("repos/MarlinFirmware_Marlin/Features/" + pullRequestNumber + "/" + pullRequestName + ".txt", "w") as f:
        f.write(createdAt + "\n")
        f.write(mergedAt + "\n")
        f.write(pullLine + "\n")
        f.write(comments + "\n")
        f.write("Files Changed:\n")
        for x in filesList:
            f.write(x.filename + "\n")
        f.write("\n")
        f.write("date: name (pull) (tag) (commit) (comment)\n")
        f.write(pull.merged_at.strftime("%d-%m-%Y") + ": " + pull.title + " (" + pullRequestNumber + ") ($NewFeature) (" + pull.merge_commit_sha + ")" )