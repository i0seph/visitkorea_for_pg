# -*- coding: utf-8 -*-
loca_query = """
WITH RECURSIVE t AS (
    SELECT *, addrname AS conname
    FROM   addrcodes
    WHERE  addrid = :location
    UNION ALL
    SELECT a.*, a.addrname || ' ' || t.conname
    FROM   addrcodes a, t
    WHERE  a.addrid = t.upaddr
)
  SEARCH DEPTH FIRST BY addrname SET path
  CYCLE addrname SET is_cycle USING path2
  SELECT   conname
  FROM     t
  WHERE    is_cycle = false
  ORDER BY path DESC
  FETCH FIRST 1 ROW ONLY
"""
cate_query = """
with recursive t as (
select *,1 as level, tourname as conname from tourism where tourid = :category
union all
select a.*,t.level + 1, a.tourname || ' > ' || t.conname from tourism a, t where a.tourid = t.uptour
) select conname from t order by level desc limit 1
"""
