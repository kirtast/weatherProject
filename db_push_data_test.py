import sqlite3
import app_test
from shutil import copyfile
import os
import datetime

def DB_insert_daily_data():
    data_dict = app_test.create_dataDict_from_API()
    data_daily_raw = data_dict['data_daily']
    data_daily = app_test.pull_data_daily_API(data_daily_raw)
    header_daily = app_test.create_header_daily(data_dict)

    strExe = app_test.create_str_pull_daily_data(header_daily)

    conn=sqlite3.connect('DB_weather.sqlite')
    cur=conn.cursor()

    for row in data_daily:
        cur.execute(strExe,tuple(row))

    conn.commit()
    cur.close()

def DB_insert_hour_data():
    data_dict = app_test.create_dataDict_from_API()
    data_hour_raw = data_dict['data_hour']
    header_hour = app_test.create_header_hour(data_dict)

    strExe = app_test.create_str_pull_hour_data(header_hour)

    data_hour_list = list()
    row_data_hour = list()
    for row in data_hour_raw:
        for header in header_hour:
            row_data_hour.append(data_hour_raw[row][header])
        data_hour_list.append(row_data_hour)
        row_data_hour = list()

    conn=sqlite3.connect('DB_weather.sqlite')
    cur=conn.cursor()

    for row in data_hour_list:
        cur.execute(strExe,tuple(row))

    conn.commit()
    cur.close()

#Funcition to create the structure of the database
def DB_initialize():
    conn=sqlite3.connect('DB_weather.sqlite')
    cur=conn.cursor()
    cur.executescript('''
    DROP TABLE IF EXISTS Daily;
    DROP TABLE IF EXISTS Hour_Data;
    DROP TABLE IF EXISTS InfoMeasures;
    DROP TABLE IF EXISTS InfoMeasuresHour;
    '''
    )

    vars = app_test.create_home_loc()
    url_main = app_test.create_url_API(vars['lan'],vars['API_KEY'],vars['location'])
    response = app_test.get_response_API(url_main)
    data = response.json()

    data_daily = list()
    data_hour = list()
    data_info = list()
    data_daily_info = list()

    keys = list()
    for key in data:
        if not key=='copyright' and not key=='web' and not key=='language' and not key=='locality' and not key=='use':
            keys.append(key)
    for key in keys:
        if key=='information':
            data_info=data[key]
        elif key=='day1' or key=='day2' or key=='day3' or key=='day4' or key=='day5' or key=='day6' or key=='day7':
            data_daily.append(data[key])
        elif key == 'hour_hour':
            data_hour=data[key]

    #===============================================================================
    #=================== APARTADO DE DAILY =========================================
    #===============================================================================
    row = data_daily[0]
    header_daily=list()

    for key in row:
        header_daily.append(key)

    type_header=list()
    for head in header_daily:
        if head == 'date':
            type_header.append('DATE')
        elif head.find('temperature')>-1:
            type_header.append('REAL')
        elif head == 'humidity':
            type_header.append('REAL')
        elif head == 'wind':
            type_header.append('REAL')
        else:
            type_header.append('TEXT')

    tup_daily = list(zip(header_daily, type_header))
    str_daily = 'CREATE TABLE Daily(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, '

    count = 1
    for pair in tup_daily:
        if count < len(tup_daily):
            str_daily = str_daily + pair[0] + ' ' + pair[1] + ', '
        else:
            str_daily = str_daily + pair[0] + ' ' + pair[1] + ')'
        count = count + 1

    #print(str_daily)
    cur.execute(str_daily)

    #===============================================================================
    #=================== APARTADO DE InfoMeasures ==================================
    #===============================================================================
    str='CREATE TABLE InfoMeasures(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,Measure TEXT UNIQUE, Unit TEXT)'
    cur.execute(str)
    for key in data_info:
        cur.execute(app_test.create_str_pull_info_data(data_info),tuple([key,data_info[key]]))
    #===============================================================================
    #=================== APARTADO DE HOURS =========================================
    #===============================================================================

    data_hour_test=data_hour['hour1']

    header_hour=list()
    for key in data_hour_test:
        header_hour.append(key)

    type_header=list()
    for head in header_hour:
        if head == 'date':
            type_header.append('DATE')
        elif head.find('temperature')>-1:
            type_header.append('REAL')
        elif head == 'humidity':
            type_header.append('REAL')
        elif head == 'pressure':
            type_header.append('REAL')
        elif head == 'wind':
            type_header.append('REAL')
        else:
            type_header.append('TEXT')

    tup_hour = list(zip(header_hour, type_header))
    str_hour = 'CREATE TABLE Hour_Data(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, '
    count = 1
    for pair in tup_hour:
        if count < len(tup_hour):
            str_hour = str_hour + pair[0] + ' ' + pair[1] + ', '
        else:
            str_hour = str_hour + pair[0] + ' ' + pair[1] + ')'
        count = count + 1

    cur.execute(str_hour)

    #===============================================================================
    #=================== APARTADO DE InfoMeasuresHour ==============================
    #===============================================================================
    str='CREATE TABLE InfoMeasuresHour(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,MeasureName TEXT UNIQUE, IndexMeasure INTEGER)'
    cur.execute(str)

    conn.commit()
    cur.close()

def DB_backups():
    user = os.getlogin()
    if user == 'Usuario' and os.path.isdir('C:/Users/Usuario/github/weather/'):
        now = datetime.datetime.now()
        src = 'C:/Users/Usuario/github/weather/DB_weather.sqlite'
        dst = 'C:/Users/Usuario/github/backup/DB_weather_' + (now.strftime("%Y%m%d%H%M%S")) + '.sqlite'
        copyfile(src, dst)


if __name__ == '__main__':
    DB_backups()
    DB_initialize()
    DB_insert_hour_data()
    DB_insert_daily_data()
