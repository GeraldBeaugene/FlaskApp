import mysql.connector
from mysql.connector import Error
from mysql.connector import cursor
import flask
from flask import jsonify, request, session, url_for, render_template, redirect
from flask_cors import CORS
import hashlib


def encrypt(string):
    result = hashlib.sha256(string.encode())

    return result.hexdigest()


def create_conn(hostname, username, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=user_password,
            database=db_name
        )
    except Error as e:
        print(f'The error {e} occurred')
    return connection


application = flask.Flask(__name__)
application.config['DEBUG'] = True
application.config['JSON_SORT_KEYS'] = False
application.secret_key = "This is a secret"
CORS(application)


@application.route('/api/planes/all', methods=['GET'])
def api_get_planes():
    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor(dictionary=True)
    result = None
    try:
        cursor.execute('select * from planes')
        result = cursor.fetchall()
    except Error as e:
        print(f'The error {e} occurred')
    return jsonify(result)


@application.route('/api/planes/add', methods=['POST'])
def api_add_planes():

    request_data = request.get_json()
    new_plane_make = request_data['make']
    new_plane_model = request_data['model']
    new_plane_year = request_data['year']
    new_plane_capacity = request_data['capacity']

    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor()
    add_to = '(make,model,year,capacity)'
    sql = f"insert into planes {add_to} values ('{new_plane_make}', '{new_plane_model}', {new_plane_year}," \
          f" {new_plane_capacity}) "

    try:
        cursor.execute(sql)
        conn.commit()
        return 'Query executed successfully'
    except Error as e:
        return f'The error {e} occurred'


@application.route('/api/planes/update', methods=['PUT'])
def api_update_planes():

    request_data = request.get_json()
    sel_plane = request_data['sell']
    new_plane_capacity = request_data['new_capacity']
    new_plane_year = request_data['new_year']

    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor()
    table_name = 'planes'
    update = f"set year = {new_plane_year}, capacity = {new_plane_capacity}"

    sql = f"update {table_name} {update} where id = {sel_plane}"

    try:
        cursor.execute(sql)
        conn.commit()
        return 'Query executed successfully'
    except Error as e:
        return f'The error {e} occurred'


@application.route('/api/planes/delete', methods=['DElETE'])
def api_delete_planes():

    request_data = request.get_json()
    plane_make = request_data['make']
    plane_model = request_data['model']
    plane_year = request_data['year']
    plane_capacity = request_data['capacity']

    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor()
    sql = f"delete from planes where make = '{plane_make}' and model = '{plane_model}' and year = {plane_year} and capacity = {plane_capacity}"

    try:
        cursor.execute(sql)
        conn.commit()
        return 'Query executed successfully'
    except Error as e:
        return f'The error {e} occurred'


@application.route('/api/airports/all', methods=['GET'])
def api_get_airports():
    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor(dictionary=True)
    result = None
    try:
        cursor.execute('Select * From airports')
        result = cursor.fetchall()
    except Error as e:
        print(f'The error {e} occurred')
    return jsonify(result)


@application.route('/api/airports/add', methods=['POST'])
def api_add_airports():

    request_data = request.get_json()
    new_airports_code = request_data['code']
    new_airports_name = request_data['name']
    new_airports_country = request_data['country']

    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor()
    add_to = '(airport_code,airport_name,country)'
    sql = f"insert into airports {add_to} values (upper('{new_airports_code}'), '{new_airports_name}', upper('{new_airports_country}'))"

    try:
        cursor.execute(sql)
        conn.commit()
        return 'Query executed successfully'
    except Error as e:
        return f'The error {e} occurred'


@application.route('/api/airports/update', methods=['PUT'])
def api_update_airports():

    request_data = request.get_json()
    airports_id = request_data['id']
    new_airports_country = request_data['new_country']
    new_airports_name = request_data['new_name']

    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor()
    table_name = 'airports'
    update = f"set country = '{new_airports_country}', airport_name = '{new_airports_name}'"

    sql = f"update {table_name} {update} where id = {airports_id}"

    try:
        cursor.execute(sql)
        conn.commit()
        return 'Query executed successfully'
    except Error as e:
        return f'The error {e} occurred'


@application.route('/api/airports/delete', methods=['DELETE'])
def api_delete_airports():

    request_data = request.get_json()
    code = request_data['code']
    name = request_data['name']
    country = request_data['country']

    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor()

    sql = f"delete from airports where airport_name = '{name}' and airport_code = upper('{code}') and country = upper('{country}')"

    print(sql)

    try:
        cursor.execute(sql)
        conn.commit()
        return 'Query executed successfully'
    except Error as e:
        return f'The error {e} occurred'


@application.route('/api/flights/all', methods=['GET'])
def api_get_flights():
    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(
                       ' select planes.make, planes.model, a1.airport_name as from_airport, ' +
                       f" a2.airport_name as to_airport, date_format(flights.date,'%M %D, %Y') as date from " +
                       ' flights inner join planes on ' +
                       ' planes.id = flights.plane_id ' +
                       ' inner join airports a1 on ' +
                       ' a1.id = flights.airport_from_id ' +
                       ' inner join airports a2 on ' +
                       ' a2.id = flights.airport_to_id' +
                       ' order by date desc')
        result = cursor.fetchall()
    except Error as e:
        print(f'The error {e} occurred')
    return jsonify(result)


@application.route('/api/flights/add', methods=['POST'])
def api_add_flights():

    request_data = request.get_json()
    new_plane_id = request_data['planeid']
    new_from_id = request_data['departid']
    new_to_id = request_data['arriveid']
    new_date = request_data['date']

    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor()
    add_to = '(plane_id,airport_from_id,airport_to_id,date)'
    sql = f"insert into flights {add_to} values ({new_plane_id}, {new_from_id}, {new_to_id}," \
          f" '{new_date}')"

    try:
        cursor.execute(sql)
        conn.commit()
        return 'Query executed successfully'
    except Error as e:
        return f'The error {e} occurred'


@application.route('/api/flights/delete', methods=['DELETE'])
def api_delete_flights():

    request_data = request.get_json()
    plane_id = request_data['planeid']
    depart_id = request_data['departid']
    arrive_id = request_data['arriveid']
    del_date = request_data['date']

    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor()
    table_name = 'flights'
    sql = f"delete from {table_name} where plane_id = {plane_id} and airport_from_id = {depart_id} and airport_to_id " \
          f"= {arrive_id} and date = '{del_date}'"

    try:
        cursor.execute(sql)
        conn.commit()
        return 'Query executed successfully'
    except Error as e:
        return f'The error {e} occurred'


@application.route('/api/users/login', methods=['POST'])
def api_get_users():
    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor(dictionary=True)
    result = None

    request_data = request.get_json()
    email = encrypt(request_data['email'])
    password = encrypt(request_data['password'])
    sql = f"SELECT count(email) as 'count' from CIS3368FALLDB.users " \
          f"where email = '{email}'  and password = '{password}'"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except Error as e:
        print(f'The error {e} occurred')
    return jsonify(result)


@application.route('/api/users/register', methods=['POST'])
def api_add_users():
    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor(dictionary=True)
    result = None

    request_data = request.get_json()
    email = encrypt(request_data['email'])
    username = request_data['username']
    password = encrypt(request_data['password'])
    sql = f"insert into CIS3368FALLDB.users (username, password, email) values ('{username}','{password}','{email}')"

    try:
        cursor.execute(sql)
        conn.commit()
        return 'Success'
    except Error as e:
        print(f'The error {e} occurred')


@application.route('/api/reset', methods=['PUT'])
def api_reset_users():
    conn = create_conn('cis3368fall.chiudr0wp2rq.us-east-2.rds.amazonaws.com', 'admin', 'admin123', 'CIS3368FALLDB')
    cursor = conn.cursor(dictionary=True)
    result = None

    request_data = request.get_json()
    email = encrypt(request_data['email'])
    new_password = encrypt(request_data['new_password'])

    table_name = 'users'
    update = f"set password = '{new_password}'"

    sql = f"update {table_name} {update} where email = '{email}'"

    try:
        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchall()
    except Error as e:
        print(f'The error {e} occurred')
    return jsonify(result)


if __name__ == '__main__':
    application.run(debug=True)
