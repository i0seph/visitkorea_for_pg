all_loca_query = """
    select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl
    from place a, (select place_id from place where cate in
                        (with recursive t as (select * from tourism where uptour = any(:catestr)
                        union all select a.* from tourism a, t where a.uptour = t.tourid)
                   select tourid from t where length(tourid) = 9) order by place_name limit 50) b
    left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id
"""

all_cate_query = """
    select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl
    from place a, (select place_id from place where loca in
                        (select addrid from addrcodes where upaddr = any(:locastr)) order by place_name limit 50) b
    left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id
"""

undefind_loca_query = """
    select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl
    from place a, (select place_id from place where loca is null and cate in (
            (with recursive t as (select * from tourism where uptour = any(:catestr) 
                                  union all select a.* from tourism a, t where a.uptour = t.tourid)
             select tourid from t where length(tourid) = 9)) order by place_name limit 50) b 
    left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id
"""

sub_loca_cate_query = """
SELECT DISTINCT ON (a.place_id, a.place_name)
    a.place_id, a.place_name, c.imgurl
FROM place a,
    (SELECT place_id FROM place
      WHERE loca IN (SELECT addrid FROM addrcodes WHERE upaddr = ANY(:locastr))
        AND cate IN ( WITH RECURSIVE t AS (
                      SELECT * FROM tourism WHERE uptour = ANY(:catestr)
                      UNION ALL
                      SELECT a.* FROM tourism a,  t WHERE a.uptour = t.tourid)
                      SELECT tourid FROM t WHERE length(tourid) = 9)
      ORDER BY place_name FETCH FIRST 50 ROWS ONLY) b
    LEFT JOIN place_images c ON b.place_id = c.place_id
    WHERE a.place_id = b.place_id
ORDER BY a.place_name, a.place_id, c.imgurl;

"""

