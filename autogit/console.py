import autogit
import sys
import time
import os

def run():
    repo_paths = []

    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            with open(sys.argv[1]) as r:
                repo_paths = [ p.strip("\n").strip("\r") for p in r.readlines() ]
        else:
            repo_paths.append(sys.argv[1])
    else:
        repo_paths.append(".")

    print(repo_paths)

    while True:
        for repo_path in repo_paths:
            autogit.sync_repo(repo_path)
        time.sleep(10)
