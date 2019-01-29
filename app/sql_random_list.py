# -*- coding: utf-8 -*-
query = "select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl \
        from place a, (select place_id from place order by random() limit 20) b left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id"
