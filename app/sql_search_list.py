# -*- coding: utf-8 -*-
query = """
SELECT DISTINCT ON (a.place_name, a.place_id) a.place_id, a.place_name, b.imgurl
FROM place a LEFT JOIN place_images b ON a.place_id = b.place_id
WHERE place_name ~* to_regexp(:search_str)
ORDER BY a.place_name, a.place_id, b.imgurl
FETCH FIRST 50 ROWS ONLY
 """
