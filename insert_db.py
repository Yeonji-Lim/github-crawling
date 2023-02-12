from github import PaginatedList, Team
import pymysql

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