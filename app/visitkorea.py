import os
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
import psycopg2
import psycopg2.extras
from urllib.parse import quote_plus
from pprint import pprint

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    f = request.args.get('f', 's').strip()
    v = request.args.get('v', '<http://data.visitkorea.or.kr/>').strip()

    d = {}
    d['f'] = f
    d['v'] = v
    d['fs'] = ('s', 'p', 'ot', 'ov')

    conn = psycopg2.connect('user=postgres port=5432 host=/tmp')
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = "select * from visitkorea where {} = %s".format(f)
    cur.execute(query, (v,))

    d['rows'] = cur.fetchall();
    d['quote_plus'] = quote_plus
    cur.close()
    conn.close()
    
    return render_template('index.html', d = d)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
