from github import Github
from github import Auth
import os
import time
import pickle
import pandas as pd
import datetime

def contributorsExtract(name, auth, g, logger):
    start = time.time()
    reponame = name.rstrip()
    logger.info(reponame + " contributorsExtract")
    repofolder = "repos/" + reponame.replace("/", "_")
    repotext = repofolder + "/text"
    if not os.path.exists("repos"):
        os.mkdir("repos")
    if not os.path.exists(repofolder):
        os.mkdir(repofolder)
    if not os.path.exists(repotext):
        os.mkdir(repotext)
    repo = g.get_repo(reponame)
    contributors = repo.get_contributors()
    
    fields = ["Name", "Commits"]
    csvFile = pd.DataFrame(columns=fields)
    for user in contributors:
        name = user.login
        commits = user.contributions
        csvFile.loc[len(csvFile)] = ([name, commits])
    startCSV = time.time()
    csvFile.to_csv(repotext + "/Contributors.csv", index=False)
    end = time.time()
    logger.info(f'csv time: {end-startCSV}')   
    end = time.time()
    logger.info(f'total time: {end-start}')
    logger.info("--------------------------")