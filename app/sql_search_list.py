# -*- coding: utf-8 -*-
query = """
select distinct on (a.place_name, a.place_id) a.place_id, a.place_name, b.imgurl
from place a, place_images b where place_name ~ to_regexp(:search_str)
and a.place_id = b.place_id order by a.place_name, a.place_id limit 50
 """
