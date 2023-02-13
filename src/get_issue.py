import datetime
from github import Organization, Repository

last_week = datetime.datetime.now()-datetime.timedelta(weeks=1)
last_day = datetime.datetime.now()-datetime.timedelta(days=1)

def get_all_issues(o: Organization.Organization):
    print('===== start : get_all_issues =====')
    return [i for r in o.get_repos() for i in r.get_issues(state="closed") if i.user.name != "Deleted user"]


def get_all_issues_in_last_week(o: Organization.Organization):
    print('===== start : get_all_issues_in_last_week =====')
    return [i for r in o.get_repos() for i in r.get_issues(state="closed", since=last_week) if i.user.name != "Deleted User" and i.closed_at >= last_week]


def get_repo_issues_last_week(r: Repository.Repository):
    print('===== start : get_repo_issues_last_week =====')
    return [i for i in r.get_issues(state="closed", since=last_week) if i.user.name != "Deleted User" and i.closed_at >= last_week]


def get_repo_issues_last_day(r: Repository.Repository):
    print('===== start : get_repo_issues_last_day =====')
    return [i for i in r.get_issues(state="closed", since=last_week) if i.user.name != "Deleted User" and i.closed_at >= last_day]
