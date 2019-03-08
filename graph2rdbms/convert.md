## visitkorea 테이블 자료 정리
```sql

-- ov, ot 정리
select * from visitkorea where s = '<http://data.visitkorea.or.kr/>'

select * from visitkorea where ot <> '' and ov <> ''

select ov, count(*) from visitkorea where ot <> '' and ov <> '' group by ov

select p,count(*) from visitkorea 
where ot <> '' and ov = '<http://www.w3.org/2001/XMLSchema#double>'
group by p

update visitkorea set ov = '' 
  where ot <> '' and p in ('<http://www.w3.org/2003/01/geo/wgs84_pos#lat>',
'<http://www.w3.org/2003/01/geo/wgs84_pos#long>')

select ov, count(*) from visitkorea where ot <> '' and ov <> '' group by ov

update visitkorea set ov = '' 
  where ot <> '' and ov = '<http://www.w3.org/2001/XMLSchema#string>'
  
select * from visitkorea where ot <> '' and ov <> ''
-- ov, ot 정리 끝

```

## visitkorea 테이블에서 관광 카테고리 테이블 뽑기
```sql

CREATE TABLE public.tourism (
    tourid text NOT NULL PRIMARY KEY,
    tourname text,
    uptour text
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
update tourism set uptour = '' where uptour is null;
```

## visitkorea 테이블에서 주소 테이블 뽑기
```sql
CREATE TABLE public.addrcodes (
    addrid text NOT NULL PRIMARY KEY,
    addrname text,
    upaddr text
);
INSERT INTO addrcodes
SELECT Replace(Replace(a.s, '<http://data.visitkorea.or.kr/resource/CATEGORY:', ''), '>',
       '') AS s,
       a.ot,
       Replace(Replace(c.ov, '<http://data.visitkorea.or.kr/resource/CATEGORY:', ''), '>'
       , '')
            AS ov
FROM   visitkorea a
       JOIN visitkorea b
         ON b.ov = '<http://data.visitkorea.or.kr/resource/AddressScheme>'
            AND b.p = '<http://www.w3.org/2004/02/skos/core#inScheme>'
            AND a.s = b.s
            AND a.p = '<http://www.w3.org/2000/01/rdf-schema#label>'
       LEFT OUTER JOIN visitkorea c
                    ON a.s = c.s
                       AND c.p = '<http://www.w3.org/2004/02/skos/core#broader>';
update addrcodes set upaddr = '' where upaddr is null;
```

## visitkorea 테이블에서 ontology 뽑기
```sql
select * from visitkorea where 
s like '<http://data.visitkorea.or.kr/ontology/%>' 
and p in ('<http://www.w3.org/2000/01/rdf-schema#subClassOf>' 
          , '<http://www.w3.org/2002/07/owl#equivalentClass>')


select * from visitkorea where s = '<http://data.visitkorea.or.kr/ontology/Event>'
select * from visitkorea where s = '<http://data.visitkorea.or.kr/ontology/Musical>'
select * from visitkorea where ov  = '<http://data.visitkorea.or.kr/ontology/Event>'

with recursive t as (
select *,to_char(row_number() over (order by s), 'FM00000000') as level, 0 as depth from visitkorea 
	where s like '<http://data.visitkorea.or.kr/ontology/%' 
	and p = '<http://www.w3.org/2002/07/owl#equivalentClass>'
union all
select a.*, t.level || to_char(row_number() over (order by a.s), 'FM00000000'), t.depth + 1 
	from visitkorea a, t 
	where a.s like '<http://data.visitkorea.or.kr/ontology/%' 
	and a.p = '<http://www.w3.org/2000/01/rdf-schema#subClassOf>' and a.ov = t.s
)
select t.s,a.ot as ot, t.depth from t, visitkorea a 
where t.s = a.s and a.p = '<http://www.w3.org/2000/01/rdf-schema#label>' and a.ol in ('','ko')
-- and a.s like '<http://data.visitkorea.or.kr/ontology/%>'
order by t.level
```

## visitkorea 테이블에서 지역 테이블 뽑기
```sql
select s, ot from visitkorea 
where s ~ '<http://data.visitkorea.or.kr/resource/[0-9]+' 
  and p = '<http://www.w3.org/2000/01/rdf-schema#label>';
-- s 는 place_id int, ot 는 place_name varchar(80) 으로 place 테이블을 만들고, 이 자료를 입력
alter table place add long numeric;
alter table place add lat numeric;
select s, ot from visitkorea 
where s ~ '<http://data.visitkorea.or.kr/resource/[0-9]+' 
  and p = '<http://www.w3.org/2003/01/geo/wgs84_pos#lat>';
select s, ot from visitkorea 
where s ~ '<http://data.visitkorea.or.kr/resource/[0-9]+' 
  and p = '<http://www.w3.org/2003/01/geo/wgs84_pos#long>';
update place a set long = b.ot from (...) b where a.place_id = b.place_id;
update place a set lat = b.ot from (...) b where a.place_id = b.place_id;
```
## place_images 테이블 정리
```sql
p  = '<http://xmlns.com/foaf/0.1/depicts>'
```
## place_links 테이블 정리
```sql
p  = '<http://www.w3.org/2002/07/owl#sameAs>'
```
## attnames 테이블 
```sql
select s from visitkorea 
where p = '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>' 
and ov = '<http://www.w3.org/2002/07/owl#DatatypeProperty>' 
and s like '<http://data.visitkorea.or.kr/property/%';

select p, count(*) as c 
from visitkorea 
where p like '<http://data.visitkorea.or.kr/property/%' 
group by p;

select a.s, a.ot, coalesce(b.c,0) 
from visitkorea a 
     left join (select p, count(*) as c 
                from visitkorea 
		where p like '<http://data.visitkorea.or.kr/property/%' 
		group by p) b 
     on a.s = b.p 
where a.s in (select s from visitkorea 
              where p = '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>' 
              and ov = '<http://www.w3.org/2002/07/owl#DatatypeProperty>' 
              and s like '<http://data.visitkorea.or.kr/property/%') 
and a.p = '<http://www.w3.org/2000/01/rdf-schema#label>' 
and ol = 'ko' 
order by 3 desc,1;
```
## 
## 자료 보정
```sql
insert into tourism values ('B01', '교통', '');
insert into tourism values ('B0102', '교통시설', 'B01');
insert into tourism values ('B01020100', '공항', 'B0102');
insert into tourism values ('B01020200', '기차역', 'B0102');

update place set cate = 'A05020100' where place_id = 2521792;
update place set cate = 'A05020300' where place_id = 2521793;
update place set cate = 'A05020100' where place_id = 2521797;
update place set cate = 'A02030200' where place_id = 2518763;
update place set cate = 'B01020200' where place_id = 2398659;
update place set cate = 'B01020200' where place_id = 1964662;
update place set cate = null where place_id in (125387, 125357, 1989182);
update place set cate = 'A01010500' where place_id in (2518600);
update place set cate = null where place_id in (2518566);
```
