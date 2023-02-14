from github import Github
import pymysql
import sys
from datetime import datetime, timedelta

conn = pymysql.connect(host='127.0.0.1', user="crawler",
                       password="dalcomsoft", db="github_crawling", charset="utf8mb4")
c = conn.cursor()

g = Github("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")

org = g.get_organization("dalcomsoft")

repos = org.get_repos()

for repo in repos:

    print("====== get {} closed contents to {} repository ======".format(
        sys.argv[1], repo.name))

    prs = repo.get_pulls(state="closed")
    for pr in prs:
        confirm_pr_number_sql = "SELECT * FROM `closed_contents` WHERE `repository` = %s AND `pr_id` = %s LIMIT 1"
        c.execute(confirm_issue_number_sql, (repo.name, pr.number))
        confirm_pr_number = c.fetchone()
        if confirm_pr_number:
            continue

        closed_at_kst = pr.closed_at + timedelta(hours=9)
        yesterday = datetime.now() - timedelta(days=1)
        a_weekt_ago = yesterday - timedelta(days=7)

        if sys.argv[1] == "daily":
            start_time = yesterday.strftime("%Y-%m-%d 00:00:00")
        elif sys.argv[1] == "weekly":
            start_time = a_weekt_ago.strftime("%Y-%m-%d 00:00:00")
        end_time = yesterday.strftime("%Y-%m-%d 23:59:59")
        if str(closed_at_kst) <= start_time:
            break

        if start_time <= str(closed_at_kst) <= end_time:
            assignees = []
            reviewers = []
            for assignee in pr.assignees:
                assignees.append(assignee.login)

            for reviewer in pr.get_review_requests()[0]:
                reviewers.append(reviewer.login)

            sql = "INSERT INTO `closed_contents` (`repository`, `pr_id`, `authored`, `assignees`, `reviewers`, `closed_at`) VALUES (%s, %s, %s, %s, %s, %s)"
            c.execute(sql, (repo.name, pr.number, pr.user.login, ','.join(
                assignees), ','.join(reviewers), closed_at_kst))
            conn.commit()

    issues = repo.get_issues(state="closed")
    for issue in issues:
        confirm_issue_number_sql = "SELECT * FROM `closed_contents` WHERE `repository` = %s AND `pr_id` = %s LIMIT 1"
        c.execute(confirm_issue_number_sql, (repo.name, issue.number))
        confirm_issue_number = c.fetchone()
        if confirm_issue_number:
            continue

        closed_at_kst = issue.closed_at + timedelta(hours=9)
        yesterday = datetime.now() - timedelta(days=1)
        a_weekt_ago = yesterday - timedelta(days=7)

        if sys.argv[1] == "daily":
            start_time = yesterday.strftime("%Y-%m-%d 00:00:00")
        elif sys.argv[1] == "weekly":
            start_time = a_weekt_ago.strftime("%Y-%m-%d 00:00:00")
        end_time = yesterday.strftime("%Y-%m-%d 23:59:59")
        if str(closed_at_kst) <= start_time:
            break

        if start_time <= str(closed_at_kst) <= end_time:
            assignees = []
            for assignee in issue.assignees:
                assignees.append(assignee.login)

            sql = "INSERT INTO `closed_contents` (`repository`, `issue_id`, `authored`, `assignees`, `closed_at`) VALUES (%s, %s, %s, %s, %s)"
            c.execute(sql, (repo.name, issue.number, issue.user.login,
                      ','.join(assignees), closed_at_kst))
            conn.commit()

conn.close()
