from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import psycopg2
import psycopg2.extras
from urllib.parse import quote_plus
from pprint import pprint

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    f = request.args.get('f', '').strip()
    v = request.args.get('v', '').strip()
    if f == '' and v == '':
        return redirect('/?f=s&v=<http%3A%2F%2Fdata.visitkorea.or.kr%2Fresource%2FKTODataset>')
    d = {}
    d['f'] = f
    d['v'] = v
    conn = psycopg2.connect('user=postgres host=localhost')
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = "select s, p, case when ot <> '' then ot else ov end as ot, '' as ov, ol from visitkorea where {} = %s".format(f)
    cur.execute(query, (v,))

    d['rows'] = cur.fetchall();
    d['quote_plus'] = quote_plus
    cur.close()
    conn.close()
    
    return render_template('ntviewer.html', d = d)

if __name__ == '__main__':
    app.run(debug=True)
