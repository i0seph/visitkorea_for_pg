# -*- coding: utf-8 -*-
#select 
#	128981 as place_id, 
#	'관방제림' as place_name, 
#	'http://tong.visitkorea.or.kr/cms/resource/02/1606902_image2_1.jpg' as imgurl

query = """
with i as (
  select distinct on (place_id) place_id, imgurl
  from (
    select place_id, imgurl
    from place_images
    tablesample bernoulli (0.05) limit 20
  ) a
  order by place_id, imgurl limit 10
)
select p.place_id, p.place_name as place_name, i.imgurl, p.long::float, p.lat::float
from place p, i
where p.place_id = i.place_id
"""
