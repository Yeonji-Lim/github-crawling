from insert_db import *
from get_info import *
from get_issue import *
from get_pr import *

access_token='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'
g = Github(access_token)
o = get_org(g)

con = pymysql.connect(host='localhost', user='github_crawler', password='crawling', db='github_crawling', charset='utf8')
cur = con.cursor()

insert_db_teams_and_members(cur, o.get_teams(), ['server', 'client'])

con.commit()
con.close()