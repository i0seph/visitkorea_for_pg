```sql

-- ov, ot 정리
select * from visitkorea where s = '<http://data.visitkorea.or.kr/>'

select * from visitkorea where ot <> '' and ov <> ''

select ov, count(*) from visitkorea where ot <> '' and ov <> '' group by ov

select p,count(*) from visitkorea where ot <> '' and ov = '<http://www.w3.org/2001/XMLSchema#double>'  group by p

update visitkorea set ov = '' 
  where ot <> '' and p in ('<http://www.w3.org/2003/01/geo/wgs84_pos#lat>',
'<http://www.w3.org/2003/01/geo/wgs84_pos#long>')

select ov, count(*) from visitkorea where ot <> '' and ov <> '' group by ov

update visitkorea set ov = '' 
  where ot <> '' and ov = '<http://www.w3.org/2001/XMLSchema#string>'
  
select * from visitkorea where ot <> '' and ov <> ''
-- ov, ot 정리 끝

```
