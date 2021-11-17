# -*- coding: utf-8 -*-
query = """
select addrid, addrname 
from addrcodes
where upaddr = :upaddr 
order by addrname
"""
