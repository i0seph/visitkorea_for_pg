all_loca_query = "select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl \
                        from place a, (select place_id from place where cate in \
                        (with recursive t as (select * from tourism where uptour = any(:catestr) \
                        union all select a.* from tourism a, t where a.uptour = t.tourid) select tourid from t where length(tourid) = 9) order by place_name limit 50) b \
                    left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id"

all_cate_query = "select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl \
                        from place a, (select place_id from place where loca in \
                        (select addrid from addrcodes where upaddr = any(:locastr)) order by place_name limit 50) b \
                    left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id"

undefind_loca_query = "select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl \
                    from place a, (select place_id from place where loca is null and cate in (\
            (with recursive t as (select * from tourism where uptour = any(:catestr) \
            union all select a.* from tourism a, t where a.uptour = t.tourid) select tourid from t where length(tourid) = 9)) order by place_name limit 50) b \
            left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id"

sub_loca_cate_query = "select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl \
                    from place a, (select place_id from place where loca in \
            (select addrid from addrcodes where upaddr = any(:locastr)) and cate in \
            (with recursive t as (select * from tourism where uptour = any(:catestr) \
            union all select a.* from tourism a, t where a.uptour = t.tourid) select tourid from t where length(tourid) = 9) order by place_name limit 50) b \
            left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id"

