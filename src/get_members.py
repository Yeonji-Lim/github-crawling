from github import Github
import pymysql

conn = pymysql.connect(host='127.0.0.1', user="crawler",
                       password="dalcomsoft", db="github_crawling", charset="utf8mb4")
c = conn.cursor()

g = Github("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")

org = g.get_organization("dalcomsoft")

teams = org.get_teams()

for team in teams:
    if team.name == "server" or team.name == "client":
        print("===== get members to {} team =====".format(team.name))
        members = team.get_members()
        for member in members:
            is_exist_member_sql = "SELECT * FROM `members` WHERE `nick` = %s LIMIT 1"
            c.execute(is_exist_member_sql, (member.login))
            is_exist_member = c.fetchone()
            if is_exist_member:
                continue

            sql = "INSERT INTO `members` (`id`, `name`, `nick`, `team`) VALUES (%s, %s, %s, %s)"
            c.execute(sql, (member.id, member.name, member.login, team.name))
            conn.commit()
            print("===== {} member is inserted =====".format(member.login))

conn.close()
