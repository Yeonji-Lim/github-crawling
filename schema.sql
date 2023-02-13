CREATE TABLE Team (
  id bigint NOT NULL,
  name text,
  PRIMARY KEY (id)
);

CREATE TABLE Member (
  id bigint NOT NULL,
  name text,
  PRIMARY KEY (id)
);

CREATE TABLE Belong (
  id bigint NOT NULL AUTO_INCREMENT,
  team_id bigint,
  member_id bigint,
  PRIMARY KEY (id),
  FOREIGN KEY (member_id) REFERENCES Member(id),
  FOREIGN KEY (team_id) REFERENCES Team(id)
);

CREATE TABLE Repository (
  id bigint NOT NULL,
  name text NOT NULL,
  url text NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Content (
  id bigint NOT NULL,
  title text NOT NULL,
  content_num bigint NOT NULL,
  repo_id bigint NOT NULL,
  content_type text NOT NULL,
  url text NOT NULL,
  created_at timestamp NOT NULL,
  updated_at timestamp NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (repo_id) REFERENCES Repository(id)
);

CREATE TABLE MemberStatus (
  member_id bigint NOT NULL,
  content_id bigint NOT NULL,
  role varchar(10) NOT NULL,
  PRIMARY KEY (member_id, content_id, role),
  FOREIGN KEY (content_id) REFERENCES Content(id),
  FOREIGN KEY (member_id) REFERENCES Member(id)
);
