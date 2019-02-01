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
select *,to_char(row_number() over (order by s), 'FM00000000') as level from visitkorea 
	where s like '<http://data.visitkorea.or.kr/ontology/%' 
	and p = '<http://www.w3.org/2002/07/owl#equivalentClass>'
union all
select a.*, t.level || to_char(row_number() over (order by a.s), 'FM00000000')
	from visitkorea a, t 
	where a.s like '<http://data.visitkorea.or.kr/ontology/%' 
	and a.p = '<http://www.w3.org/2000/01/rdf-schema#subClassOf>' and a.ov = t.s
)
select t.s,repeat(' ',length(t.level) - 8) || a.ot as ot,t.ov from t, visitkorea a 
where t.s = a.s and a.p = '<http://www.w3.org/2000/01/rdf-schema#label>' and a.ol in ('','ko')
-- and a.s like '<http://data.visitkorea.or.kr/ontology/%>'
order by t.level
```

## visitkorea 테이블에서 지역 테이블 뽑기