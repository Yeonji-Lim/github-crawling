import datetime
from github import Organization, Repository

last_week = datetime.datetime.now()-datetime.timedelta(weeks=1)

def get_all_prs(o: Organization.Organization):
    print('===== start : get_all_prs =====')
    return [p for r in o.get_repos() for p in r.get_pulls(state="closed") if p.user.name != "Deleted user"]


def get_all_prs_in_last_week(o: Organization.Organization):
    print('===== start : get_all_prs_in_last_week =====')
    return [p for r in o.get_repos() for p in r.get_pulls(state="closed") if p.user.name != "Deleted User" and p.closed_at >= last_week]


def get_repo_prs_last_week(r: Repository.Repository):
    print('===== start : get_repo_prs_last_week =====')
    return [p for p in r.get_pulls(state="closed") if p.user.name != "Deleted User" and p.closed_at >= last_week]
