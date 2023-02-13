import pymysql
from datetime import datetime, timedelta

conn = pymysql.connect(host='127.0.0.1', user="root",
                       password="yourpassword", db="github_crawling", charset="utf8mb4")
c = conn.cursor()

yesterday = datetime.now() - timedelta(days=1)
start_time = yesterday.strftime("%Y-%m-%d 00:00:00")
end_time = yesterday.strftime("%Y-%m-%d 23:59:59")

get_members_sql = "SELECT `id`, `name`, `nick`, `team` FROM `members`"
c.execute(get_members_sql)
members = c.fetchall()

for member in members:
    print("===== start to get {}'s authored, assigned, reviewed daily counts =====".format(
        member[1]))
    get_autored_content_count_sql = "SELECT COUNT(*) FROM `closed_contents` WHERE `authored` = %s AND `closed_at` BETWEEN %s AND %s"
    c.execute(get_autored_content_count_sql, (member[2], start_time, end_time))
    autored_content_count = c.fetchone()
    print("autored_content_count: ", autored_content_count[0])
    get_assigned_content_count_sql = "SELECT COUNT(*) FROM `closed_contents` WHERE `assignees` LIKE %s AND `closed_at` BETWEEN %s AND %s"
    c.execute(get_assigned_content_count_sql,
              ('%' + member[2] + '%', start_time, end_time))
    assigned_content_count = c.fetchone()
    print("assigned_content_count: ", assigned_content_count[0])
    get_reviewed_content_count_sql = "SELECT COUNT(*) FROM `closed_contents` WHERE `reviewers` LIKE %s AND `closed_at` BETWEEN %s AND %s"
    c.execute(get_reviewed_content_count_sql,
              ('%' + member[2] + '%', start_time, end_time))
    reviewed_content_count = c.fetchone()
    print("reviewed_content_count: ", reviewed_content_count[0])
    insert_daily_content_count_sql = "INSERT INTO `daily_content_counts` (`member_id`, `authored_count`, `assigned_count`, `reviewed_count`, `aggregation_date`) VALUES (%s, %s, %s, %s, %s)"
    c.execute(insert_daily_content_count_sql, (member[0], autored_content_count[0],
              assigned_content_count[0], reviewed_content_count[0], yesterday.strftime("%Y-%m-%d")))
    conn.commit()
    print("===== result to {}'s authored, assigned, reviewed daily counts: {}, {}, {} =====".format(
        member[1], autored_content_count[0], assigned_content_count[0], reviewed_content_count[0]))

conn.close()
