query = """
    select b.attname, a.v from place_attrib a join attnames b on a.attid = b.attid where place_id = :place_id
"""
