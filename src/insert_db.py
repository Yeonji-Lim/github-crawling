from github import PaginatedList, Team, Organization, Repository, NamedUser, PullRequest
import pymysql
from get_issue import *
from get_pr import *


def insert_db_team_and_members(cur: pymysql.cursors.Cursor, team: Team.Team):
    sql = 'insert into Team(id, name) values(%s, %s) on duplicate key update name = values(name)'
    cur.execute(sql, (int(team.id), team.name))
    for m in team.get_members():
        sql = 'insert into Member(id, name) values(%s, %s) on duplicate key update name = values(name)'
        cur.execute(sql, (int(m.id), m.name))
        sql = 'insert into Belong(team_id, member_id) values(%s, %s)'
        cur.execute(sql, (int(team.id), int(m.id)))


def insert_db_teams_and_members(cur: pymysql.cursors.Cursor, teams: PaginatedList.PaginatedList, team_names: list=[]):
    sql = 'truncate table belong'
    cur.execute(sql)
    for t in teams:
        if list:
            if t.name in team_names:
                insert_db_team_and_members(cur, t)
        else:
            insert_db_team_and_members(cur, t)


def is_user_in_member(cur: pymysql.cursors.Cursor, u: NamedUser.NamedUser):
    sql = 'select * from Member where id = %s'
    cur.execute(sql, int(u.id))
    return cur.fetchall()


# content: Issue.Issue or PullRequest.PullRequest
def insert_db_contents_and_member_statuses(cur: pymysql.cursors.Cursor, repo: Repository.Repository, content, content_type):
    sql = 'insert into Content(id, title, content_num, repo_id, content_type, url, created_at, updated_at) values(%s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update title = values(title), url = values(url), updated_at = values(updated_at)'
    cur.execute(sql, (int(content.id), content.title, content.number, int(repo.id), content_type, str(content.url).replace('https://api.github.com/repos/', 'https://github.com/'), content.created_at, content.updated_at))
    sql = 'insert ignore into MemberStatus(member_id, content_id, role) values(%s, %s, %s)'
    if is_user_in_member(cur, content.user):
        cur.execute(sql, (int(content.user.id), int(content.id), 'AUTHOR'))
    for a in content.assignees:
        if is_user_in_member(cur, a):
            cur.execute(sql, (int(a.id), int(content.id), 'ASSIGNEE'))
    if isinstance(content, PullRequest.PullRequest):
        for r in content.get_reviews():
            if is_user_in_member(cur, r):
                cur.execute(sql, (int(r.user.id), int(content.id), 'REVIEWER'))
    
def insert_db_contents_in_last_week(cur: pymysql.cursors.Cursor, org: Organization.Organization):
    for r in org.get_repos():
        sql = 'insert into Repository(id, name, url) values(%s, %s, %s) on duplicate key update name = values(name), url = values(url)'
        cur.execute(sql, (int(r.id), r.name, r.url))
        for i in get_repo_issues_last_week(r):
            insert_db_contents_and_member_statuses(cur, r, i, 'ISSUE')
        for p in get_repo_prs_last_week(r):
            insert_db_contents_and_member_statuses(cur, r, p, 'PULLREQUEST')
            
def insert_db_contents_in_last_day(cur: pymysql.cursors.Cursor, org: Organization.Organization):
    for r in org.get_repos():
        sql = 'insert into Repository(id, name, url) values(%s, %s, %s) on duplicate key update name = values(name), url = values(url)'
        cur.execute(sql, (int(r.id), r.name, r.url))
        for i in get_repo_issues_last_day(r):
            insert_db_contents_and_member_statuses(cur, r, i, 'ISSUE')
        for p in get_repo_prs_last_day(r):
            insert_db_contents_and_member_statuses(cur, r, p, 'PULLREQUEST')
          