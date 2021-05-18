from flask import Flask, render_template
import sqlite3
import app_test
import db_push_data_test
import datetime
app = Flask(__name__)
# app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///DB_weather.sqlite'
# db = SQLAlchemy(app)


@app.route("/")
def main_page():

    db_push_data_test.DB_initialize()
    db_push_data_test.DB_insert_hour_data()
    db_push_data_test.DB_insert_daily_data()

    conn=sqlite3.connect('DB_weather.sqlite')
    cur=conn.cursor()
    cur.execute('SELECT * FROM Daily')
    daily = cur.fetchall()
    cur.execute('SELECT * FROM Hour_Data')
    hours = cur.fetchall()
    cur.execute('SELECT * FROM InfoMeasures')
    info = cur.fetchall()
    cur.close()
    now_raw = datetime.datetime.now()
    now = now_raw.strftime("%Y-%m-%d-%H:%M:%S")

    data_loc = app_test.create_home_loc()
    if data_loc['location'] == '6999':
        loc_str = 'Rubí (Barcelona)'
    else:
        loc_str = 'No Rubí (Barcelona)'
    return render_template('home.html', daily = daily, hours = hours, info = info, now = now, loc = data_loc['location'], loc_str = loc_str)

if __name__ == '__main__':
    #app.run(host = "0.0.0.0", port = 5000, debug = True, use_reloader = True)
    #app.run()
    app.run(host = '0.0.0.0', port = 5000)
