# -*- coding: utf-8 -*-
query = """
select linkurl from place_links where place_id = :place_id order by linkurl
"""
