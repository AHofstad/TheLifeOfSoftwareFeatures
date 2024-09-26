from github import Github
from github import Auth
import os
import time
import pickle
import pandas as pd
import datetime


def importPullRequests(name, auth, g, logger, date):
    start = time.time()
    reponame = name.rstrip()
    logger.info(reponame + " importPullRequests")
    repofolder = "repos/" + reponame.replace("/", "_")
    repofile = repofolder + "/pullrequest"
    repotext = repofolder + "/text"
    if not os.path.exists("repos"):
        os.mkdir("repos")
    if not os.path.exists(repofolder):
        os.mkdir(repofolder)
    if not os.path.exists(repofile):
        os.mkdir(repofile)
    if not os.path.exists(repotext):
        os.mkdir(repotext)
    repo = g.get_repo(reponame)
    pulls = repo.get_pulls(state="all")
    try:
        csvFile = pd.read_csv(repotext + "/pullResults.csv")
        csvExists = True
    except:
        csvExists = False
    pickleFile = open(repofile + "/data.pickle", "ab")
    length = pulls.totalCount
    logger.info(f"Total pulls: {length}")
    for idx, pr in enumerate(pulls):
        prCreated = pr.created_at
        prNumber = pr.number
        logger.info(
            f"{reponame} - {idx + 1}/{length} - {prNumber} - Created at: {prCreated} - Current time: {datetime.datetime.now()}"
        )
        date = date.replace(tzinfo=prCreated.tzinfo)
        print(idx)
        if prCreated < date:
            logger.info("Too old")
            break
        if csvExists and (prNumber in csvFile["Number"].values):
            logger.info("Already done may be outdated")
            continue

        files = []
        if pr.merged:
            try:
                commit = repo.get_commit(pr.merge_commit_sha)
                listFiles = commit.files
                for file in listFiles:
                    files.append(file.filename)
            except:
                files.append("commit doesn't exist")
        comments = pr.get_issue_comments().totalCount + pr.get_comments().totalCount
        prData = {
            "pr": pr,
            "number": prNumber,
            "comments": comments,
            "merged": pr.merged,
            "state": pr.state,
            "labels": pr.labels,
            "files": files,
            "url": pr.html_url,
        }
        pickle.dump(prData, pickleFile, protocol=pickle.HIGHEST_PROTOCOL)
    pickleFile.close()
    end = time.time()
    logger.info(f"total time: {end-start}")
    logger.info("--------------------------")


def importIssues(name, auth, g, logger, date):
    start = time.time()
    reponame = name.rstrip()
    logger.info(reponame + " importIssues")
    repofolder = "repos/" + reponame.replace("/", "_")
    repofile = repofolder + "/issue"
    repoPull = repofolder + "/pullrequest"
    repotext = repofolder + "/text"
    if not os.path.exists("repos"):
        os.mkdir("repos")
    if not os.path.exists(repofolder):
        os.mkdir(repofolder)
    if not os.path.exists(repofile):
        os.mkdir(repofile)
    if not os.path.exists(repotext):
        os.mkdir(repotext)
    repo = g.get_repo(reponame)
    issues = repo.get_issues(state="all")
    try:
        csvFile = pd.read_csv(repotext + "/issueResults.csv")
        csvExists = True
    except:
        csvExists = False
    try:
        pullCsvFile = pd.read_csv(repotext + "/pullResults.csv")
        pullCsvExists = True
    except:
        pullCsvExists = False
    pickleFile = open(repofile + "/data.pickle", "ab")
    length = issues.totalCount
    logger.info(f"Total issues: {length}")
    for idx, pr in enumerate(issues):
        prCreated = pr.created_at
        prNumber = pr.number
        logger.info(
            f"{reponame} - {idx + 1}/{length} - {prNumber} - Created at: {prCreated} - Current time: {datetime.datetime.now()}"
        )
        date = date.replace(tzinfo=prCreated.tzinfo)
        print(idx)
        if prCreated < date:
            logger.info("Too old")
            break
        if csvExists and (prNumber in csvFile["Number"].values):
            logger.info("Already done may be outdated")
            continue
        if pullCsvExists and (prNumber in pullCsvFile["Number"].values):
            logger.info("Issue converted to pull request")
            continue
        comments = pr.get_comments().totalCount
        prData = {
            "pr": pr,
            "number": prNumber,
            "comments": comments,
            "state": pr.state,
            "labels": pr.labels,
            "url": pr.html_url,
        }
        pickle.dump(prData, pickleFile, protocol=pickle.HIGHEST_PROTOCOL)
    pickleFile.close()
    end = time.time()
    logger.info(f"total time: {end-start}")
    logger.info("--------------------------")
