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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@pg14:5432/postgres'
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['POST', 'GET'])
def start_page():
    sql('select 1')
    d = {"title": "PostgreSQL + Flask + jquery 로 구축하는 대한민국 구석구석"}
    return render_template('index.html', d = d)

@app.route('/place/<int:place_id>')
def view_resource(place_id):
    mod = __import__('sql_' + inspect.stack()[0][3] , fromlist=['sql_' + inspect.stack()[0][3]])
    query = mod.query
    d = sql(query, {'place_id': place_id})
    return render_template('place.html', d = d.fetchone())

@app.route('/ajax/getattrib/<int:place_id>')
def get_attribute(place_id):
    mod = __import__('sql_' + inspect.stack()[0][3] , fromlist=['sql_' + inspect.stack()[0][3]])
    query = mod.query
    d = sql(query, {'place_id': place_id})
    return jsonify([dict(row) for row in d.fetchall()])

@app.route('/ajax/getimages/<int:place_id>')
def get_images(place_id):
    mod = __import__('sql_' + inspect.stack()[0][3] , fromlist=['sql_' + inspect.stack()[0][3]])
    d = sql(mod.query, {'place_id': place_id})
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

@app.route('/ajax/gettodayfesta/')
def festa_list():
    mod = __import__('sql_' + inspect.stack()[0][3] , fromlist=['sql_' + inspect.stack()[0][3]])
    d = sql(mod.query)
    return jsonify([dict(row) for row in d.fetchall()])

@app.route('/ajax/list/<locaval>/<cateval>')
def place_list(locaval, cateval):
    mod = __import__('sql_' + inspect.stack()[0][3] , fromlist=['sql_' + inspect.stack()[0][3]])
    if (locaval == "all" and cateval == "all"):
        return random_list()
    elif locaval == "all":
        catestr = cateval.split(",")
        d = sql(mod.all_loca_query, {'catestr': catestr})
    elif cateval == "all":
        locastr = locaval.split(",")
        d = sql(mod.all_cate_query, {'locastr': locastr})
    else:
        if locaval == "undefind":
            catestr = cateval.split(",")
            d = sql(mod.undefind_loca_query, {'catestr': catestr})
        else:
            locastr = locaval.split(",")
            catestr = cateval.split(",")
            d = sql(mod.sub_loca_cate_query, {'locastr': locastr, 'catestr': catestr})
    return jsonify([dict(row) for row in d.fetchall()])

@app.route('/ajax/namesearch/<search_str>')
def search_list(search_str):
    mod = __import__('sql_' + inspect.stack()[0][3] , fromlist=['sql_' + inspect.stack()[0][3]])
    d = sql(mod.query, {'search_str': '%' + search_str + '%'})
    return jsonify([dict(row) for row in d.fetchall()])

@app.route('/ajax/getnames/<location>/<category>')
def get_cateloca_names(location,category):
    mod = __import__('sql_' + inspect.stack()[0][3] , fromlist=['sql_' + inspect.stack()[0][3]])
    if location == "None":
        locaname = "미지정"
    else:
        query = mod.loca_query
        res = sql(query, {'location': location})
        locaname = res.fetchone()[0];

    query = mod.cate_query
    res = sql(query, {'category': category})
    catename = res.fetchone()[0];
    return jsonify(catename=catename,locaname=locaname);

@app.route('/ajax/near/<place_id>/<x>/<y>')
def near_list(place_id, x,y):
    mod = __import__('sql_' + inspect.stack()[0][3] , fromlist=['sql_' + inspect.stack()[0][3]])
    d = sql(mod.query, {'place_id': place_id, 'x1': x, 'y1': y})
    return jsonify([dict(row) for row in d.fetchall()])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
