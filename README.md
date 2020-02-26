# from graph database to PostgreSQL

## 준비물

* python 3.6.x
* PostgreSQL 10 이상
* 쉘 작업 환경은 LANG=ko_KR.UTF-8 환경
* http://data.visitkorea.or.kr/linked_open_data 페이지에 있는 데이터셋 visitkorea.nt.zip 다운로드 파일

## 테스트

1. 작업 순서
   1. git clone https://github.com/i0seph/visitkorea_for_pg.git
   1. cd visitkorea_for_pg
   1. python3 -m venv .
   1. . bin/activate
   1. pip install -r requirements.txt
   1. wget -O visitkorea.nt.gz http://data.visitkorea.or.kr/download/dataset
   1. gzip -d visitkorea.nt.gz
   1. python3 nt2pgcopy.py visitkorea.nt visitkorea.pg
   1. psql -c "create table visitkorea (s text, p text, ot text, ov text, ol text)"
   1. psql -c "\\copy visitkorea from 'visitkorea.pg'"
   1. cd app
   1. visitkorea.py, ntviewer.py 의 데이터베이스 접속 정보 수정 필요
   1. ntviewer.py - visitkorea 테이블 조회
   1. visitkorea.py - 사용자용 응용 프로그램 샘플
   1. python ntviewer.py
1. visitkorea 테이블 구경하기
   1. http://localhost:5000 웹페이지로 자료 구경
   1. PostgreSQL 쪽 인덱스가 필요함
       * CREATE INDEX visitkorea_ov_i ON visitkorea (ov) WHERE (ov <> '');
       * CREATE INDEX visitkorea_s_i ON visitkorea (s);
       * CREATE INDEX visitkorea_v_i ON visitkorea (p);
1. 응용프로그램 웹 서비스 시작
   1. python visitkorea.py
   1. http://localhost:8000 
   1. (SQL 교육용 샘플 코드임으로 당연히 실행되지 않습니다. 직접 다 만들어야 돌아갑니다!)
   
