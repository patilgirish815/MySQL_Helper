from main import *
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, make_response
from flask_cors import CORS, cross_origin
from celery import Celery
import os

app = Flask(__name__)
simple_app = Celery('simple_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
cors = CORS(app)
app.secret_key = os.urandom(24)



@app.route('/')
def dashboard():
    response = make_response(render_template('index.html'))
    return response


@app.route("/connectdbs", methods=['POST'])
@cross_origin()
def connectdbs():
    try:
        data = request.get_json()

        src_name, src_host, src_username, src_password, src_database = data['sourcename'],data['sourcehost'],data['sourceusername'],data['sourcepassword'],data['sourcedatabase']
        dst_name, dst_host, dst_username, dst_password, dst_database = data['destinationname'],data['destinationhost'],data['destinationusername'],data['destinationpassword'],data['destinationdatabase']
        source, destination = {},{}

        source['src_name'],source['src_host'],source['src_username'],source['src_password'],source['src_database'] = src_name, src_host, src_username, src_password, src_database
        destination['dst_name'],destination['dst_host'],destination['dst_username'],destination['dst_password'],destination['dst_database'] = dst_name, dst_host, dst_username, dst_password, dst_database

        sourcedb = Connection(Name=source['src_name'], host=source['src_host'], username=source['src_username'], password=source['src_password'], databasename=source['src_database'])
        destinationdb = Connection(Name=destination['dst_name'], host=destination['dst_host'],username=destination['dst_username'],password=destination['dst_password'], databasename=destination['dst_database'])

    except Exception as e:
        return jsonify({'message':str(e), "status":"error"})
    return jsonify({'message':"Connection established successfully", "status":"success"})


@app.route("/missingsps", methods=['POST'])
@cross_origin()
def missing_sps():
    try:
        data = request.get_json()
        sourcedb, destinationdb = create_connection(data)
        missingSps = get_missing_sps_in_destination(sourcedb, destinationdb)
        return jsonify(missingSps)
    except Exception as e:
        return jsonify({"message": str(e)})


@app.route("/missingtables", methods=['POST'])
@cross_origin()
def missing_tables():
    try:
        data = request.get_json()
        sourcedb,destinationdb = create_connection(data)
        missing_tables = get_missing_tables_in_destination(sourcedb, destinationdb)
        return jsonify(missing_tables)
    except Exception as e:
        return jsonify({"message":str(e)})


@app.route("/tablesdiffdef", methods=['POST'])
@cross_origin()
def tables_diff_def():
    try:
        data = request.get_json()
        r = simple_app.send_task('tasks.get_diff_tbl_definition',kwargs={'data': data})
        return jsonify({"task_id":str(r.id)})
    except Exception as e:
        return jsonify({"message":str(e)})


@app.route("/spsdiffdef", methods=['POST'])
@cross_origin()
def sps_diff_def():
    try:
        data = request.get_json()
        r = simple_app.send_task('tasks.get_sp_difference', kwargs={'data': data})
        return jsonify({"task_id":str(r.id)})
    except Exception as e:
        return jsonify({"messgae":str(e)})


@app.route("/spsdiffinparam", methods=['POST'])
@cross_origin()
def sps_diff_inparam():
    try:
        data = request.get_json()
        r = simple_app.send_task('tasks.get_diff_sp_inparams', kwargs={'data': data})
        return jsonify({"task_id":str(r.id)})
    except Exception as e:
        return jsonify({"message":str(e)})


@app.route('/simple_task_status/<task_id>')
@cross_origin()
def get_status(task_id):
    print("In simple_task_status")
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return str(status.state)


@app.route('/simple_task_result/<task_id>')
@cross_origin()
def task_result(task_id):
    result = simple_app.AsyncResult(task_id).result
    return str(result)


def create_connection(data):
    sourcedb = Connection(Name=data['sourcename'], host=data['sourcehost'], username=data['sourceusername'],password=data['sourcepassword'], databasename=data['sourcedatabase'])
    destinationdb = Connection(Name=data['destinationname'], host=data['destinationhost'],username=data['destinationusername'], password=data['destinationpassword'],databasename=data['destinationdatabase'])
    return (sourcedb,destinationdb)




