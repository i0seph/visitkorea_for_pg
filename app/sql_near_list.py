query = """
select distinct on (b.distance, a.place_id, a.place_name) a.place_id, a.place_name, d.tourname, c.imgurl, b.distance as distance
    from place a, (
    select place_id, round((earth_distance(position, ll_to_earth(:y1, :x1))::numeric / 1000)::numeric, 2)::float as distance from place a
    where earth_box(ll_to_earth(:y1, :x1), 2000) @> position and a.place_id <> :place_id
    ) b left join place_images c on b.place_id = c.place_id, tourism d where a.place_id = b.place_id and d.tourid = substring(a.cate, 1, 3) order by distance, place_name, place_id limit 50;
"""
