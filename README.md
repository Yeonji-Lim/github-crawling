이 프로젝트는 (주)달콤소프트 내에서 진행한 프로젝트로

허가를 받은 후 보안 관련 내용을 제외하고 복제하였습니다. (git mirror 사용)

- issue, pull request의 history는 삭제됨

다음의 이유로 당시 반려되었습니다.
- report용 프로젝트이지만 서비스용으로 설계된 erd  
- 느린 실행 속도

# github-crawling

Client팀과 Server팀 팀원들의 Github History를 Reporting하는 프로젝트

## Requirements

- macOS
- Python 3.9.7
- MySQL 8.0.32

## Structure

```
github-crawling
 ┣ docs
 ┃ ┗ github_crawling_erd.png
 ┣ src
 ┃ ┣ schema.sql                       -> 테이블 생성 쿼리
 ┃ ┣ get_issue.py                     -> 이슈 목록 불러오는 메소드 모음
 ┃ ┣ get_pr.py                        -> PR 목록 불러오는 메소드 모음
 ┃ ┣ initial_set.py                   -> 실행 시 처음 처리 되어야 하는 부분
 ┃ ┣ insert_content_last_week.py      -> 현재 날짜 기준으로 지난 하루의 이슈 및 PR 목록 저장
 ┃ ┣ insert_content_last_week.py      -> 현재 날짜 기준으로 지난 주의 이슈 및 PR 목록 저장
 ┃ ┣ insert_db.py                     -> DB에 저장하는 메소드 모음
 ┃ ┗ insert_member_and_team.py        -> 팀, 멤버를 저장하거나 업데이트
 ┣ .gitignore
 ┣ README.md
 ┗ requirements.txt
```

## Quick Start

1. git clone

   ```sh
   git clone https://github.com/Yeonji-Lim/github-crawling.git
   cd github-crawling
   ```

2. pip install

   ```sh
   pip install -r requirements.txt
   ```

3. mysql setting (for mac)

   설치

   ```sh
   brew install mysql
   ```

   mysql 데몬 실행

   ```sh
   brew services start mysql
   ```

   최초 실행시 root 패스워드 설정

   ```sh
   mysqladmin -u root -p password [패스워드]
   ```

   MySQL 접속

   ```sh
   mysql -u root -p
   ```

   설정한 패스워드 입력

   사용자 설정, db 사용 설정

   ```sh
   create user 'github_crawler'@'localhost' identified by 'crawling';
   create database github_crawling;
   grant all privileges on github_crawling.* to 'github_crawler'@'localhost' with grant option;
   flush privileges;
   use github_crawling;
   ```

   테이블 생성

   ```sh
   source [github-crawling/schema.sql의 절대경로];
   ```

4. initial_set.py에 토큰 설정 및 크롤링 대상이 되는 조직 이름 작성

   ```python
   def get_org(g: Github):
    return [x for x in g.get_user().get_orgs() if x.name == '소속조직이름'][0]

   access_token = '엑세스토큰'
   ```

5. 멤버 정보 저장

   ```sh
   python3 src/update_member_and_team.py
   ```

6. 최근 일주일 기록 저장
   ```sh
   python3 src/insert_content_last_week.py
   ```

## ERD

잘못된 설계 : report용 프로젝트이지만 서비스용으로 설계

![github_crawling_erd](./docs/github_crawling_erd.png)
