from db import Database
from comparator import *
from difflib import HtmlDiff
from more_itertools import sliced
import pandas as pd



class Connection:

    def __init__(self,Name, host, username, password, databasename):
        self.name = Name
        self.host = host
        self.username = username
        self.password = password
        self.databasename = databasename
        self.connection = Database(host=self.host,username=self.username,password=self.password, databasename=self.databasename)


def get_sps_list(name):
    name_sps = []
    namedb = name.connection.fetch_sp_list_for_db()
    for d in namedb: name_sps.append(d['ROUTINE_NAME'])
    return name_sps


def get_tables_list(name):
    name_tables = []
    namedb = name.connection.fetch_table_list_for_db()
    for d in namedb: name_tables.append(d['TABLE_NAME'])
    return name_tables


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


def get_tables_with_different_def_in_destination(source, destination):
    # source_tables = get_tables_list(source)
    destination_tables = get_tables_list(destination)
    destination_tables_missing = get_missing_tables_in_destination(source, destination)
    source_tables = [ table for table in destination_tables if table not in destination_tables_missing]
    tables_with_diff_def = []
    for src_tbl,dst_tbl in zip(source_tables,destination_tables):
        src_def = source.connection.fetch_table_definition(src_tbl)
        dst_def = destination.connection.fetch_table_definition(dst_tbl)
        src_def = src_def[0]['Create Table'] if src_def else "Table missing on : " + source.name
        dst_def = dst_def[0]['Create Table'] if dst_def else "Table missing on : " + destination.name
        if compare_definitions( src_def, dst_def):
            pass
        else:
            data = {}
            data['src_tbl'], data['dst_tbl'] = src_tbl, dst_tbl
            data['src_tbl_def'], data['dst_tbl_def'] = src_def, dst_def
            src_def = split_list_string_charc_grt(src_def.split("\n"), 63)
            dst_def = split_list_string_charc_grt(dst_def.split("\n"), 63)
            html = create_html_diff_table(src_def, dst_def)
            data['difftbl'] = html.replace('\n', '').replace("\\", "")
            tables_with_diff_def.append(data)

    return tables_with_diff_def


def get_sp_diff_definition(source, destination):
    try:
        # source_sps = get_sps_list(source)
        destination_sps = get_sps_list(destination)
        destination_sps_missing = get_missing_sps_in_destination(source, destination)
        source_sps = [sp for sp in destination_sps if sp not in destination_sps_missing]
        sps_with_diff_def = []
        source_sps_def = pd.DataFrame(source.connection.fetch_sp_def_for_db())
        destination_sps_def = pd.DataFrame(destination.connection.fetch_sp_def_for_db())

        for src_sp, dst_sp in zip(source_sps, destination_sps):
            src_sp_def =  source_sps_def[source_sps_def['ROUTINE_NAME'] == src_sp]
            src_sp_def = src_sp_def.iloc[0, 1] if not src_sp_def.empty else "Missing on " + source.name

            dst_sp_def = destination_sps_def[destination_sps_def['ROUTINE_NAME'] == dst_sp]
            dst_sp_def = dst_sp_def.iloc[0, 1] if not dst_sp_def.empty else "Missing on " + destination.name

            src_sp_def = src_sp_def.replace('\r', '').replace('\t', '') if src_sp_def else "Sp missing on " + source.name
            dst_sp_def = dst_sp_def.replace('\r', '').replace('\t', '') if dst_sp_def else "Sp missing on " + destination.name

            if compare_definitions(src_sp_def.lower(), dst_sp_def.lower()):
                pass
            else:
                data = {}
                data['src_sp'], data['dst_sp'] = src_sp, dst_sp
                # data['scr_sp_def'],data['dst_sp_def'] = src_sp_def, dst_sp_def
                src_sp_def = split_list_string_charc_grt(src_sp_def.split('\n'), 63)
                dst_sp_def = split_list_string_charc_grt(dst_sp_def.split('\n'), 63)
                html = create_html_diff_table(src_sp_def, dst_sp_def)
                data['difftbl'] = html.replace('\n', '').replace("\\", "")
                sps_with_diff_def.append(data)
        return sps_with_diff_def
    except Exception as e:
        print(str(e))


def get_sps_with_different_InParam(source, destination):
    destination_sps = get_sps_list(destination)
    destination_sps_missing = get_missing_sps_in_destination(source, destination)
    source_sps = [sp for sp in destination_sps if sp not in destination_sps_missing]
    sps_with_diff_inparam = []
    src_inparams_collection = pd.DataFrame(source.connection.fetch_sp_param_for_db())
    dst_inparams_collections = pd.DataFrame(destination.connection.fetch_sp_param_for_db())

    for src_sp, dst_sp in zip(source_sps, destination_sps):
        src_inparams = list(src_inparams_collection[src_inparams_collection['SPECIFIC_NAME'] == src_sp]['PARAMETER_NAME'])
        dst_inparams = list(dst_inparams_collections[dst_inparams_collections['SPECIFIC_NAME'] == dst_sp]['PARAMETER_NAME'])

        src_inparams_list = [ d for d in src_inparams ] if src_inparams else ["Missing on " + source.name ]
        dst_inparams_list = [ d for d in dst_inparams ] if dst_inparams else ["Missing on " + destination.name ]

        src_inparams_list = split_list_string_charc_grt(src_inparams_list,50)
        dst_inparams_list = split_list_string_charc_grt(dst_inparams_list,50)

        if compare_definitions(src_inparams, dst_inparams):
            pass
        else:
            data = {}
            data['src_sp'], data['dst_sp'] = src_sp, dst_sp
            data['src_inparam'] =  convert_in_params_to_string(src_inparams)
            data['dst_inparam'] =  convert_in_params_to_string(dst_inparams)
            html = create_html_diff_table(src_inparams_list, dst_inparams_list)
            data['difftbl'] = html
            sps_with_diff_inparam.append(data)

    return sps_with_diff_inparam


def convert_in_params_to_string(in_params):
    params = ""
    if in_params:
        for in_param in in_params:
            params = params + in_param + ","
        last_char_index = params.rfind(",")
        new_string = params[:last_char_index] + "," + params[last_char_index + 1:]
        return params
    else:
        return ""


def create_html_diff_table(list1, list2):
    return HtmlDiff().make_table(list1, list2)


def split_list_string_charc_grt(list1, greater_than):
    spdef = []
    for element in list1:
        if len(element) > greater_than:
            lines = list(sliced(element, greater_than))
            for line in lines: spdef.append(line)
        else:
            spdef.append(element)
    return add_blank_spaces(spdef, greater_than)


def add_blank_spaces(list1, length):
    newlist = []
    for line in list1:
        if len(line) < length:
            offset = length - len(line)
            line += ' ' * offset
            newlist.append(line)
        else:
            newlist.append(line)
    return newlist