# -*- coding: utf-8 -*-
loca_query = """
with recursive t as (
select *,1 as level, addrname as conname from addrcodes where addrid = :location
union all
select a.*,t.level + 1, a.addrname || ' ' || t.conname from addrcodes a, t where a.addrid = t.upaddr
) select conname from t order by level desc limit 1
"""
cate_query = """
with recursive t as (
select *,1 as level, tourname as conname from tourism where tourid = :category
union all
select a.*,t.level + 1, a.tourname || ' > ' || t.conname from tourism a, t where a.tourid = t.uptour
) select conname from t order by level desc limit 1
"""
