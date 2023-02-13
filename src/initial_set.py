from github import Github
from insert_db import *
from get_issue import *
from get_pr import *


def get_org(g: Github):
    return [x for x in g.get_user().get_orgs() if x.name == 'dalcomsoft'][0]


access_token = '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'
g = Github(access_token)
o = get_org(g)

con = pymysql.connect(host='localhost', user='github_crawler', password='crawling', db='github_crawling', use_unicode=True, charset='utf8')
cur = con.cursor()
