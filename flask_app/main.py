from db import Database
from difflib import HtmlDiff
from more_itertools import sliced

class Connection:

    def __init__(self,Name, host, username, password, databasename):
        self.name = Name
        self.host = host
        self.username = username
        self.password = password
        self.databasename = databasename
        self.connection = Database(host=self.host,username=self.username,password=self.password, databasename=self.databasename)


def get_tables_list(name):
    name_tables = []
    namedb = name.connection.fetch_table_list_for_db()
    for d in namedb: name_tables.append(d['TABLE_NAME'])
    return name_tables


def get_sps_list(name):
    name_sps = []
    namedb = name.connection.fetch_sp_list_for_db()
    for d in namedb: name_sps.append(d['ROUTINE_NAME'])
    return name_sps


def get_items_from_source_that_are_not_in_dest(source, destination):
    return [item for item in source if item not in destination]


def get_missing_sps_in_destination(source, destination):
    source_sps = get_sps_list(source)
    destination_sps = get_sps_list(destination)
    html = create_html_diff_table(source_sps, destination_sps)
    html = html.replace('\n', '').replace("\\", "")
    response = {}
    data = get_items_from_source_that_are_not_in_dest(source_sps,destination_sps)
    missing_sps = [ {'spname' : d } for d in data]
    response["missing_sps"] = missing_sps
    response["diff_tbl"] = html
    return response


def get_missing_tables_in_destination(source, destination):
    source_tables = get_tables_list(source)
    destination_tables = get_tables_list(destination)
    html = create_html_diff_table(source_tables, destination_tables)
    html = html.replace('\n','').replace("\\","")
    tables = get_items_from_source_that_are_not_in_dest(source_tables, destination_tables)
    missing_tbls = [ { 'tablename' : table } for table in tables]
    response = {}
    response["missing_tbls"] = missing_tbls
    response["diff_tbl"] = html
    return response


def create_html_diff_table(list1, list2):
    return HtmlDiff().make_table(list1, list2)


