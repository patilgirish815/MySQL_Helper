import time
from celery import Celery
from celery.utils.log import get_task_logger
import json
from main import *


logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@app.task()
def get_sp_difference(data):
    logger.info('Got Request - Starting work to get diff sp definition')
    sourcedb, destinationdb = create_connection(data)
    sps_with_diff_def = get_sp_diff_definition(sourcedb, destinationdb)
    logger.info('Work Finished got diff sp definition')
    return json.dumps(sps_with_diff_def)


@app.task()
def get_diff_sp_inparams(data):
    logger.info('Got Request - Starting work to get diff sp in params')
    sourcedb, destinationdb = create_connection(data)
    sps_with_diff_inparam = get_sps_with_different_InParam(sourcedb, destinationdb)
    logger.info('Work Finished got diff sp inparams')
    return json.dumps(sps_with_diff_inparam)


@app.task()
def get_diff_tbl_definition(data):
    logger.info('Got Request - Starting work to get diff tbl definition')
    sourcedb, destinationdb = create_connection(data)
    tables_with_diff_def = get_tables_with_different_def_in_destination(sourcedb, destinationdb)
    logger.info('Work Finished got diff tbl definitions')
    return json.dumps(tables_with_diff_def)


def create_connection(data):
    sourcedb = Connection(Name=data['sourcename'], host=data['sourcehost'], username=data['sourceusername'],password=data['sourcepassword'], databasename=data['sourcedatabase'])
    destinationdb = Connection(Name=data['destinationname'], host=data['destinationhost'],username=data['destinationusername'], password=data['destinationpassword'],databasename=data['destinationdatabase'])
    return (sourcedb,destinationdb)
