# from graph database to PostgreSQL

## 준비물

* python 3.6.x
* pip install -r requirements.txt
* PostgreSQL 10 이상
* http://data.visitkorea.or.kr/linked_open_data 페이지에 있는 데이터셋 visitkorea.nt.zip 다운로드 파일

## 테스트

1. 내려 받은 압축 파일 풀기 (unzip 일수도 있고, gzip -d 일수도 있음)
1. /usr/bin/python nt2pgcopy.py visitkorea.nt > vistkorea.pg  (python 2.x 대 코드임 3.x 로 실행하면 안될 것으로 예상됨)
1. PostgreSQL 테이블 만들기: create table visitkorea (s text, p text, ot text, ov text, ol text)
1. 자료 가져오기 \copy visitkorea from 'vistkorea.pg'
1. flask 실행
   1. python3 -m venv .
   1. . bin/activate
   1. cd app
   1. python visitkorea.py
1. http://localhost:8000/ 
