query = """
select column1 as addrid , column2 as addrname 
from (values 
('010000','서울'),('020000','인천'),('030000','대전'),('040000','대구'),('050000','광주'),
('060000','부산'),('070000','울산'),('080000','세종특별자치시'),('310000','경기도'),('320000','강원도'),
('330000','충청도'),('340000','충청남도'),('350000','경상북도'),('360000','경상남도'),
('370000','전라북도'),('380000','전라남도'),('390000','제주도')) a
"""