from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
__version__ = '0.1.0'

import git
import sys
import time
import os
import requests

def internet_disconnected():
    try:
        requests.get("http://www.google.com")
        return False
    except:
        return True

def report_conflict(repo):
    print("repo has conflict")

def repo_has_conflicts(repo):
    return os.path.exists(repo.common_dir+"/MERGE_HEAD")

def repo_is_dirty(repo):
    return repo.is_dirty(untracked_files=True)

def do_commit(repo):
    repo.git.add(repo.working_dir)
    repo.index.commit("Auto commit at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def do_sync(repo):
    if "origin" in repo.remotes:
        repo.remotes.origin.pull()

        check_repo_conflicts(repo)

        repo.remotes.origin.push()
    

def check_repo_conflicts(repo):
    if repo_has_conflicts(repo):
        print( "Repo %s has conflict" %  repo.working_dir  )
        report_conflict(repo)
        raise Exception("Repo has conflict")


def sync_repo(repo_path):
    try:
        print( "Begin to sync %s " % repo_path )
        repo = git.Repo(repo_path)

        check_repo_conflicts(repo)

        if internet_disconnected():
            print( "Intenet is not avaliable" )
            raise Exception("Intenet is not avaliable")


        if repo_is_dirty(repo):
            do_commit(repo)


        do_sync(repo)

        check_repo_conflicts(repo)
        print( "End to sync %s " % repo_path )
        return True

    except Exception as e:
        print( "Sync for repo %s error" % repo_path )
        return False
