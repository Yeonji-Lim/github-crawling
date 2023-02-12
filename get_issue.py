import datetime
from github import Organization

def get_all_issues(o: Organization.Organization):
    print('===== start : get_all_issues =====')
    return (i for r in o.get_repos() for i in r.get_issues(state="closed") if i.user.name != "Deleted user")

def get_all_issues_in_last_week(o: Organization.Organization):
    print('===== start : get_all_issues_in_last_week =====')
    return (i for r in o.get_repos() for i in r.get_issues(state="closed") if i.user.name != "Deleted User" and i.closed_at >= (datetime.datetime.now()-datetime.timedelta(weeks=1)))