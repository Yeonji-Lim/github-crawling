from github import Github, Organization
from get_issue import *
from get_pr import *

def get_org(g: Github):
    return [x for x in g.get_user().get_orgs() if x.name == 'dalcomsoft'][0]

def get_members(o: Organization.Organization):
    return [(m.name, t.name) for t in o.get_teams() for m in t.get_members()]

# 모두 저장
def save_all(o):
    issues = get_all_issues(o)
    prs = get_all_prs(o)

# 지금으로 부터 한 주 간의 기록 저장
def save_all_in_last_week(o):
    issues = get_all_issues_in_last_week(o)
    prs = get_all_prs_in_last_week(o)

