from initial_set import *

insert_db_teams_and_members(cur, o.get_teams(), ['server', 'client'])

con.commit()
con.close()
