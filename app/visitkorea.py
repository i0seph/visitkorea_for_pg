# -*- coding: utf-8 -*-
'''
Copyright(c) 2019. KTDS Opensource Business Team. All rights reserved.
Author: Ioseph
이 저작물은 크리에이티브 커먼즈 저작자표시-비영리 4.0 국제 라이선스에 따라 이용할 수 있습니다.
'''
import os
from flask import Flask
from flask import abort, render_template
from flask import request
from flask import Response
from flask import g
from flask import jsonify, json
from flask import send_from_directory
import psycopg2
import psycopg2.extras
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from pprint import pprint
import inspect


app = Flask(__name__)

app.config['SECRET_KEY'] = '9b1780f7bce9960bfefc34f0d52f0690'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def sql(rawSql, sqlVars={}):
    "Execute raw sql, optionally with prepared query"
    assert type(rawSql)==str
    assert type(sqlVars)==dict
    try:
        res=db.session.execute(rawSql, sqlVars)
        db.session.commit()
        return res
    except SQLAlchemyError as e:
        error = "\n" + str(e.__dict__['orig'])
        app.logger.error(error)
        abort(500, description=error)

@app.errorhandler(500)
def program_internal_error(description):
    return render_template('error.html', error = description), 500

@app.route('/', methods=['POST', 'GET'])
def start_page():
    sql('select 1')
    d = {"title": "PostgreSQL + Flask + jquery 로 구축하는 대한민국 구석구석"}
    return render_template('index.html', d = d)

@app.route('/place/<int:place_id>')
def view_resource(place_id):
    query = "select * from place where place_id = :place_id"
    d = sql(query, {'place_id': place_id})
    return render_template('place.html', d = d.fetchone())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/ajax/getattrib/<int:place_id>')
def get_attribute(place_id):
    query = "select b.attname, a.v from place_attrib a, attnames b where a.place_id = :place_id and a.attid = b.attid order by b.sortnum"
    d = sql(query, {'place_id': place_id})
    return jsonify([dict(row) for row in d.fetchall()])

@app.route('/ajax/getimages/<int:place_id>')
def get_images(place_id):
    query = "select imgurl from place_images where place_id = :place_id order by 1"
    d = sql(query, {'place_id': place_id})
    return jsonify([dict(row) for row in d.fetchall()])


@app.route('/ajax/location')
@app.route('/ajax/location/')
@app.route('/ajax/location/<upaddr>')
def location_list(upaddr = ''):
    mod = __import__('sql_' + inspect.stack()[0][3] , fromlist=['sql_' + inspect.stack()[0][3]])
    d = sql(mod.query, {'upaddr': upaddr});
    return jsonify([dict(row) for row in d.fetchall()])

@app.route('/ajax/category')
@app.route('/ajax/category/')
@app.route('/ajax/category/<uptour>')
def category_list(uptour = ''):
    mod = __import__('sql_' + inspect.stack()[0][3] , fromlist=['sql_' + inspect.stack()[0][3]])
    d = sql(mod.query, {'uptour': uptour});
    return jsonify([dict(row) for row in d.fetchall()])

@app.route('/ajax/random10/')
def random_list():
    mod = __import__('sql_' + inspect.stack()[0][3] , fromlist=['sql_' + inspect.stack()[0][3]])
    d = sql(mod.query)
    return jsonify([dict(row) for row in d.fetchall()])

@app.route('/ajax/list/<locaval>/<cateval>')
def place_list(locaval, cateval):
    if (locaval == "all" and cateval == "all"):
        return random_list()
    elif locaval == "all":
        query = "select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl \
			from place a, (select place_id from place where cate in \
			(with recursive t as (select * from tourism where uptour = any(:catestr) \
			union all select a.* from tourism a, t where a.uptour = t.tourid) select tourid from t where length(tourid) = 9) order by place_name limit 50) b \
		    left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id"
        catestr = cateval.split(",")
        d = sql(query, {'catestr': catestr})
    elif cateval == "all":
        query = "select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl \
			from place a, (select place_id from place where loca in \
			(select addrid from addrcodes where upaddr = any(:locastr)) order by place_name limit 50) b \
		    left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id"
        locastr = locaval.split(",")
        d = sql(query, {'locastr': locastr})
    else:
        if locaval == "undefind":
            query = "select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl \
		    from place a, (select place_id from place where loca is null and cate in (\
	    (with recursive t as (select * from tourism where uptour = any(:catestr) \
            union all select a.* from tourism a, t where a.uptour = t.tourid) select tourid from t where length(tourid) = 9)) order by place_name limit 50) b \
            left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id"
            catestr = cateval.split(",")
            d = sql(query, {'catestr': catestr})
        else:
            query = "select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl \
		    from place a, (select place_id from place where loca in \
            (select addrid from addrcodes where upaddr = any(:locastr) and cate in \
	    (with recursive t as (select * from tourism where uptour = any(:catestr) \
            union all select a.* from tourism a, t where a.uptour = t.tourid) select tourid from t where length(tourid) = 9)) order by place_name limit 50) b \
            left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id"
            locastr = locaval.split(",")
            catestr = cateval.split(",")
            d = sql(query, {'locastr': locastr, 'catestr': catestr})
    return jsonify([dict(row) for row in d.fetchall()])

@app.route('/ajax/namesearch/<search_str>')
def search_list(search_str):
    query = "select distinct a.place_id, a.place_name, first_value(c.imgurl) over (partition by a.place_id) as imgurl \
		    from place a, (select place_id from place where place_name like :search_str order by place_name limit 50) b \
		    left join place_images c on b.place_id = c.place_id where a.place_id = b.place_id"
    d = sql(query, {'search_str': '%' + search_str + '%'})
    return jsonify([dict(row) for row in d.fetchall()])

@app.route('/ajax/getnames/<location>/<category>')
def get_cateloca_names(location,category):
    if location == "None":
        locaname = "미지정"
    else:
        query = "with recursive t as \
		(select * from addrcodes where addrid = :location union all select a.* from addrcodes a, t where a.addrid = t.upaddr ) \
		select string_agg(addrname,' ') from (select * from t order by addrid) a"
        res = sql(query, {'location': location})
        locaname = res.fetchone()[0];

    query = "with recursive t as (select * from tourism where tourid = :category union all select a.* from tourism a, t where a.tourid = t.uptour ) select string_agg(tourname,' > ') from (select * from t order by tourid) a"
    res = sql(query, {'category': category})
    catename = res.fetchone()[0];
    return jsonify(catename=catename,locaname=locaname);

@app.route('/ajax/near/<place_id>/<x>/<y>')
def near_list(place_id, x,y):
    query = "select distinct a.place_id, a.place_name, d.tourname, first_value(c.imgurl) over (partition by a.place_id) as imgurl, b.distance as distance \
    from place a, ( \
    select place_id, round((earth_distance(position, ll_to_earth(:y1,:x1))::numeric / 1000)::numeric, 2)::float as distance from place a \
    where earth_box(ll_to_earth(:y1,:x1), 2000) @> position and a.place_id <> :place_id \
    ) b left join place_images c on b.place_id = c.place_id, tourism d where a.place_id = b.place_id and d.tourid = substring(a.cate, 1, 3) order by 3, 5"
    d = sql(query, {'place_id': place_id, 'x1': x, 'y1': y})
    return jsonify([dict(row) for row in d.fetchall()])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
