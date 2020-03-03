# -*- coding: utf-8 -*-
query = """
select column1 as place_id, column2 as place_name, column3 as imgurl from ( values
 (125415,'대아수목원','http://tong.visitkorea.or.kr/cms/resource/83/1605083_image2_1.jpg'),
 (126500,'홍릉수목원','http://tong.visitkorea.or.kr/cms/resource/35/746635_image2_1.jpg'),
 (126668,'아침고요수목원','http://tong.visitkorea.or.kr/cms/resource/36/2648236_image2_1.jpg'),
 (127045,'한국도로공사수목원','http://tong.visitkorea.or.kr/cms/resource/63/1605463_image2_1.jpg'),
 (127432,'경상북도수목원','http://tong.visitkorea.or.kr/cms/resource/20/609120_image2_1.jpg'),
 (127497,'국립수목원(광릉숲)','http://tong.visitkorea.or.kr/cms/resource/00/2031800_image2_1.jpg'),
 (127498,'완도수목원','http://tong.visitkorea.or.kr/cms/resource/24/493924_image2_1.jpg'),
 (127514,'한라수목원','http://tong.visitkorea.or.kr/cms/resource/69/1205469_image2_1.jpg'),
 (127816,'경상남도수목원','http://tong.visitkorea.or.kr/cms/resource/02/1951102_image2_1.jpg'),
 (127817,'미동산수목원','http://tong.visitkorea.or.kr/cms/resource/84/213084_image2_1.jpg')) a
 """