from github import Github
from github import Auth
import os
import re
import time
import csv
import pickle
import pandas as pd
import datetime
import importData
import extractData
import contributorsRepo
import labelData
import repoInfo
import sys
import logging
import ast
from itertools import combinations

githublist = open("repos/githublist.txt", "r")
githublist = githublist.read()
githublist = githublist.split("\n")

info = True
contributors = True
importPullRequest = False
importIssue = False
extractPullRequest = False
extractIssue = False
labelFeatures = True
labelBugs = True

for name in githublist:
    reponame = name.rstrip()
    repofolder = "repos/" + reponame.replace("/", "_")
    repotext = repofolder + "/text"
    if not os.path.exists("repos"):
        os.mkdir("repos")
    if not os.path.exists(repofolder):
        os.mkdir(repofolder)
    if not os.path.exists(repotext):
        os.mkdir(repotext)
        
    bugLabels = open(repofolder + "/bug.txt", "r")
    bugLabels = bugLabels.read()
    bugLabels = bugLabels.split("\n")

    notBugLabels = open(repofolder + "/notbugs.txt", "r")
    notBugLabels = notBugLabels.read()
    notBugLabels = notBugLabels.split("\n")

    featureLabels = open(repofolder + "/feature.txt", "r")
    featureLabels = featureLabels.read()
    featureLabels = featureLabels.split("\n") 
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        filename=str(repotext + "/console.log"),
        filemode="w",
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    #Github Auth token
    auth = Auth.Token(
        #Github Token
    )
    g = Github(auth=auth)

    date = datetime.datetime(2024, 9, 1)

    logging.info(name)
    if info:
        logger = logging.getLogger("repoInfoExtract")
        repoInfo.repoInfoExtract(name, auth, g, logger)

    if contributors:
        logger = logging.getLogger("contributorsExtract")
        contributorsRepo.contributorsExtract(name, auth, g, logger)
    f = open(repotext + "/Contributors.csv")
    next(f)
    contributorsList = []
    for line in f:
        contributorsList.append(line.split(",")[0])

    if importPullRequest:
        logger = logging.getLogger("importPullRequests")
        importData.importPullRequests(name, auth, g, logger, date)
    if extractPullRequest:
        logger = logging.getLogger("extractPullRequests")
        extractData.extractPullRequests(name, contributorsList, logger)

    if importIssue:
        logger = logging.getLogger("importIssues")
        importData.importIssues(name, auth, g, logger, date)
    if extractIssue:
        logger = logging.getLogger("extractIssues")
        extractData.extractIssues(name, contributorsList, logger)

    if labelFeatures:
        logger = logging.getLogger("labelDataFeatures")
        labelData.labelDataFeatures(name, featureLabels, "pullrequest", logger)
        labelData.labelDataFeatures(name, featureLabels, "issue", logger)
    if labelBugs:
        logger = logging.getLogger("labelBugsFeatures")
        labelData.labelDataBugs(name, bugLabels, notBugLabels, "pullrequest", logger)
        labelData.labelDataBugs(name, bugLabels, notBugLabels, "issue", logger)

    g.close()
    log = logging.getLogger()
    for hdlr in log.handlers[:]:
        log.removeHandler(hdlr)
