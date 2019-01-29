# from graph database to PostgreSQL

## 준비물

* python 3.6.x
* PostgreSQL 10 이상
* http://data.visitkorea.or.kr/linked_open_data 페이지에 있는 데이터셋 visitkorea.nt.zip 다운로드 파일

## 테스트

1. 작업 순서
   1. git clone https://github.com/i0seph/visitkorea_for_pg.git
   1. cd visitkorea_for_pg
   1. python3 -m venv .
   1. . bin/activate
   1. pip install -r requirements.txt
   1. wget -O visitkorea.nt.gz http://data.visitkorea.or.kr/download/dataset
   1. /usr/bin/python nt2pgcopy.py visitkorea.nt > vistkorea.pg  (python 2.x 코드임 3.x 로 실행하면 안될 것으로 예상됨)
   1. psql -c "create table visitkorea (s text, p text, ot text, ov text, ol text)"
   1. psql -c "\\copy visitkorea from 'visitkorea.pg'"
   1. cd app
   1. visitkorea.py 의 데이터베이스 접속 정보 수정 필요
   1. python visitkorea.py
1. http://localhost:8000 웹페이지로 자료 구경
   1. PostgreSQL 쪽 인덱스가 필요함
       * CREATE INDEX visitkorea_ov_i ON visitkorea (ov) WHERE (ov <> '');
       * CREATE INDEX visitkorea_s_i ON visitkorea (s);
       * CREATE INDEX visitkorea_v_i ON visitkorea (p);

## visitkorea 테이블에서 관광 카테고리 테이블 추가
```sql
CREATE TABLE public.tourism (
    tourid text NOT NULL PRIMARY KEY,
    tname text,
    upid text
);
INSERT INTO tourism
SELECT Replace(Replace(a.s, '<http://data.visitkorea.or.kr/resource/', ''), '>',
       '') AS s,
       a.ot,
       Replace(Replace(c.ov, '<http://data.visitkorea.or.kr/resource/', ''), '>'
       , '')
            AS ov
FROM   visitkorea a 
       JOIN visitkorea b
         ON b.ov = '<http://data.visitkorea.or.kr/resource/TourismScheme>'
            AND b.p = '<http://www.w3.org/2004/02/skos/core#inScheme>'
            AND a.s = b.s
            AND a.p = '<http://www.w3.org/2000/01/rdf-schema#label>'
       LEFT OUTER JOIN visitkorea c
                    ON a.s = c.s
                       AND c.p = '<http://www.w3.org/2004/02/skos/core#broader>';
```
