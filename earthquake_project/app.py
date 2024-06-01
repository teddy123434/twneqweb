from flask import Flask, render_template, g, url_for, jsonify
import sqlite3, scraper
from collections import defaultdict
import datetime
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)

scraper.save_to_db(scraper.data)
DATABASE = 'earthquake_project/data/earthquakes.db'

@freezer.register_generator
def url_generator():
    yield '/'
    yield '/data'
    yield '/epicenter'
    yield '/frequency'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT id, eq_id, date, magnitude, depth, location, MaxIntensity, Lon, Lat FROM earthquakes')
    earthquakes = cur.fetchall()
    return render_template('index.html', earthquakes=earthquakes)

@app.route('/data')
def data():
    db = get_db()
    cur = db.execute('SELECT id, eq_id, date, magnitude, depth, location, MaxIntensity, Lon, Lat FROM earthquakes')
    earthquakes = cur.fetchall()
    return render_template('data.html', earthquakes=earthquakes)

@app.route('/epicenter')
def epicenter():
    db = get_db()
    cur = db.execute('SELECT id, eq_id, date, magnitude, depth, location, MaxIntensity, Lon, Lat FROM earthquakes')
    earthquakes = cur.fetchall()
    return render_template('epicenter.html', earthquakes=earthquakes)

@app.route('/frequency')
def frequency():
    db = get_db()
    cur = db.execute('SELECT date FROM earthquakes')
    dates = cur.fetchall()

    # 計算每日地震頻率
    date_counts = defaultdict(int)
    for date in dates:
        date_str = date[0].split(' ')[0]  # 只取日期部分
        date_counts[date_str] += 1

    sorted_dates = sorted(date_counts.items())
    labels = [date[0] for date in sorted_dates]
    data = [date[1] for date in sorted_dates]

    return render_template('frequency.html', labels=labels, data=data)

@app.route('/get_urls')
def get_urls():
    urls = {
        'data': url_for('data'),
        'epicenter': url_for('epicenter'),
        'frequency': url_for('frequency'),
    }
    return jsonify(urls)

if __name__ == '__main__':
    app.run(debug=False)
