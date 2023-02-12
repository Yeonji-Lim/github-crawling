import datetime
from github import Organization

def get_all_prs(o: Organization.Organization):
    print('===== start : get_all_prs =====')
    return (p for r in o.get_repos() for p in r.get_pulls(state="closed") if p.user.name != "Deleted user")

def get_all_prs_in_last_week(o: Organization.Organization):
    print('===== start : get_all_prs_in_last_week =====')
    return (p for r in o.get_repos() for p in r.get_pulls(state="closed") if p.user.name != "Deleted User" and p.closed_at >= (datetime.datetime.now()-datetime.timedelta(weeks=1)))
