from github import Github
from github import Auth
import os
import time
import pickle
import pandas as pd
import datetime

def repoInfoExtract(name, auth, g, logger):
    start = time.time()
    reponame = name.rstrip()
    logger.info(reponame + " repoInfoExtract")
    repofolder = "repos/" + reponame.replace("/", "_")
    repotext = repofolder + "/text"
    if not os.path.exists("repos"):
        os.mkdir("repos")
    if not os.path.exists(repofolder):
        os.mkdir(repofolder)
    if not os.path.exists(repotext):
        os.mkdir(repotext)
    repo = g.get_repo(reponame)
    infoName = repo.name
    infoDescription = repo.description
    infoLanguage = repo.language
    try:
        infoLicense = repo.license.name
    except:
        infoLicense = "None"
    infoHTML = repo.html_url
    
    filename = infoName + ".txt"
    path = os.path.join(repofolder, filename.replace(" ", "_"))
    f = open(path, "w", encoding='utf-8')
    f.write(infoName)
    f.write("\n")
    f.write(infoDescription)
    f.write("\n")
    f.write(infoLanguage)
    f.write("\n")
    f.write(infoLicense)
    f.write("\n")
    f.write(infoHTML)
    f.close()
    end = time.time()
    logger.info(f'total time: {end-start}')
    logger.info("--------------------------")