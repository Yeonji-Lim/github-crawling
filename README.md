# github-crawling

Client팀과 Server팀 팀원들의 Github History를 Reporting하는 프로젝트

## Quick Start

1. git clone

    ```
    git clone https://github.com/dalcomsoft/github-crawling.git
    ```

2. pip install

    ```
    pip install -r requirements.txt
    ```

3. mysql setting (for mac)

    설치
    ```
    brew install mysql
    ```

    mysql 데몬 실행
    ```
    brew services start mysql
    ```

    최초 실행시 root 패스워드 설정
    ```
    mysqladmin -u root -p password [패스워드]
    ```

    접속
    ```
    mysql -u root -p
    ```
    설정한 패스워드 입력

    ```
    create user 'github_crawler'@'localhost' identified by 'crawling';
    create database github_crawling;
    grant all privileges on github_crawling.* to 'github_crawler'@'localhost' with grant option;
    flush privileges;
    use github_crawling;
    ```

    테이블 생성
    ```
    source [github-crawling/createdb.sql의 절대경로];
    ```

4. initial_set.py에 토큰 설정하기

    ```
    access_token = '엑세스토큰'
    ```

5. 멤버 정보 저장
    ```
    python3 update_member_and_team.py
    ```

6. 최근 일주일 기록 저장
    ```
    python3 insert_info_last_week.py
    ```

## ERD Diagram

![github_crawling_erd](./docs/github_crawling_erd.png)