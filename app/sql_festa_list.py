# -*- coding: utf-8 -*-

query = """
select a.place_id, to_char(startdate, 'FMMM/FMDD') || '~' || to_char(enddate, 'FMDD') || ', ' || a.place_name as place_name
from place a,
     (select * from place_term
        where daterange(startdate, enddate, '[]') @> current_date
          and daterange(date_trunc('month' , current_timestamp)::date, (date_trunc('month' , current_timestamp) + interval '1 month')::date) @> daterange(startdate, enddate)
     ) b
where a.place_id = b.place_id
order by startdate desc, enddate, place_name desc
limit 10
"""
