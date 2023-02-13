# github-crawling

Client팀과 Server팀 팀원들의 Github History를 Reporting하는 프로젝트

## Requirements
- Python 3.9.6
- mysql  Ver 8.0.32
- pip 23.0 from /Users/yourNick/Library/Python/3.9/lib/python/site-packages/pip (python 3.9)

## QuickStart
```sh
git clone https://github.com/dalcomsoft/github-crawling.git
cd github-crawling

pip install -r requirements.txt

# MySql에서 github_crawling 데이터베이스 생성
# 데이터베이스 생성 후 schema.sql 덤프 파일을 로컬 DB에 덤프
cd your/path/github_crawling
mysql -u root - p github_crawling < schema.sql

# src폴더 내 4개의 파일 4~5번째 줄에 로컬 DB root 계정 password 입력 후 저장
conn = pymysql.connect(host='127.0.0.1', user="root", password="yourpassword", db="github_crawling", charset="utf8mb4")

# 매일 클라이언트팀, 서버팀 멤버 불러오기 in terminal
python3 src/get_members.py

# 매일 Closed된 Issue와 PR 리스트 불러오기 (매개변수: 'daily', 'weekly')
python3 src/get_closed_contents.py daily

# 일별 각 멤버의 authored, assigned. reviewed 카운트를 daily_content_counts 테이블에 저장하기
python3 src/get_daily_content_counts.py

# 주별 각 멤버의 authored, assigned. reviewed 카운트를 weekly_content_counts 테이블에 저장하기
python3 src/get_weekly_content_counts.py
```