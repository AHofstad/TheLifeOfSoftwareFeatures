# To append to a pickle file
from github import Github
from github import IssueComment
import pickle
import os
import re
import time
import csv
import pandas as pd


def extractPullRequests(name, contributorsList, logger):
    # To load from pickle file
    start = time.time()
    fields = [
        "Number",
        "Name",
        "Comments",
        "Merged",
        "State",
        "Labels",
        "Created",
        "Closed",
        "Commit",
        "Files",
        "Url",
    ]
    reponame = name.rstrip()
    logger.info(reponame + " extractPullRequests")
    repofolder = "repos/" + reponame.replace("/", "_")
    repofile = repofolder + "/pullrequest"
    filename = repofile + "/data.pickle"
    repotext = repofolder + "/text"
    data = []
    try:
        with open(filename, "rb") as fr:
            try:
                while True:
                    data.append(pickle.load(fr))
            except EOFError:
                pass
    except:
        logger.info("File not present")
        logger.info("--------------------------")

    if not os.path.exists(repofolder):
        os.mkdir(repofolder)
    if not os.path.exists(repofile):
        os.mkdir(repofile)
    if not os.path.exists(repotext):
        os.mkdir(repotext)

    csvFile = pd.DataFrame(columns=fields)
    logger.info(len(data))
    for items in data:
        startItem = time.time()
        pr = items["pr"]
        prCreated = pr.created_at
        if items["merged"]:
            prClosed = pr.merged_at
            prCommit = pr.merge_commit_sha
        elif items["state"] == "closed":
            prClosed = "Not Merged"
            prCommit = "Doesn't Exist"
        else:
            prClosed = "Not yet closed"
            prCommit = "Unknown"
    
        prNumber = items["number"]
        prTitle = pr.title.strip()
        if len(prTitle) < 100:
            pullrequest = (
                "#"
                + str(prNumber)
                + "_"
                + re.sub(r"[*'\"\\\/\<>:|?. ^]", "_", prTitle)
            )
        else:
            pullrequest = (
                "#"
                + str(prNumber)
                + "_"
                + re.sub(r"[*'\"\\\/\<>:|?. ^]", "_", prTitle[:100])
            )
        labelList = []
        for label in pr.labels:
            labelList.append(label.name)
        rowsPR = [
            prNumber,
            pullrequest,
            items["comments"],
            items["merged"],
            items["state"],
            labelList,
            prCreated,
            prClosed,
            prCommit,
            items["files"],
            items["url"],
        ]
        csvFile.loc[len(csvFile)] = rowsPR
        end = time.time()
    startCSV = time.time()
    csvFile.sort_values(by=["Number"], inplace=True)
    csvFile.drop_duplicates(subset=["Number"],inplace=True)
    csvFile.to_csv(repotext + "/pullResults.csv", index=False)
    end = time.time()
    logger.info(f"csv time: {end-startCSV}")
    end = time.time()
    logger.info(f"total time: {end-start}")
    logger.info("--------------------------")


def extractIssues(name, contributorsList, logger):
    # To load from pickle file
    start = time.time()
    fields = ["Number", "Name", "Comments", "State", "Labels", "Created", "Closed", "Url"]
    reponame = name.rstrip()
    logger.info(reponame + " extractIssues")
    repofolder = "repos/" + reponame.replace("/", "_")
    repofile = repofolder + "/issue"
    filename = repofile + "/data.pickle"
    repotext = repofolder + "/text"
    data = []
    try:
        with open(filename, "rb") as fr:
            try:
                while True:
                    data.append(pickle.load(fr))
            except EOFError:
                pass
    except:
        logger.info("File not present")
        logger.info("--------------------------")

    if not os.path.exists(repofolder):
        os.mkdir(repofolder)
    if not os.path.exists(repofile):
        os.mkdir(repofile)
    if not os.path.exists(repotext):
        os.mkdir(repotext)
    csvFile = pd.DataFrame(columns=fields)
    logger.info(len(data))
    for items in data:
        startItem = time.time()
        pr = items["pr"]
        prCreated = pr.created_at
        if items["state"] == "closed":
            prClosed = pr.closed_at
        else: 
            prClosed = "Not yet closed"
        prNumber = items["number"]
        prTitle = pr.title.strip()
        if len(prTitle) < 100:
            pullrequest = (
                "#"
                + str(prNumber)
                + "_"
                + re.sub(r"[*'\"\\\/\<>:|?. ^]", "_", prTitle)
            )
        else:
            pullrequest = (
                "#"
                + str(prNumber)
                + "_"
                + re.sub(r"[*'\"\\\/\<>:|?. ^]", "_", prTitle[:100])
            )
        labelList = []
        for label in pr.labels:
            labelList.append(label.name)
        rowsPR = [
            prNumber,
            pullrequest,
            items["comments"],
            items["state"],
            labelList,
            prCreated,
            prClosed,
            items["url"],
        ]
        csvFile.loc[len(csvFile)] = rowsPR
        end = time.time()
    startCSV = time.time()
    csvFile.sort_values(by=["Number"], inplace=True)
    csvFile.drop_duplicates(subset=["Number"],inplace=True)
    csvFile.to_csv(repotext + "/issueResults.csv", index=False)
    end = time.time()
    logger.info(f"csv time: {end-startCSV}")
    end = time.time()
    logger.info(f"total time: {end-start}")
    logger.info("--------------------------")
