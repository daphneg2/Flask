import os
from flask import *
import pandas as pd
import connect


def start():
    db_credentials = connect.get_db_creds()
    output_file = request.form['output_file']
    ids = request.form.getlist('input_text[]')
    if ".xlsx" not in output_file:
        output_file += ".xlsx"
    sync_data(db_credentials, ids, output_file)
    return output_file


def sync_data(db_credentials, ids, output_file):
    con = connect.connect(db_credentials)
    cursor = con.cursor()
    sync_queires = open(os.path.abspath("sync.txt")).read().split("\n")
    frames = {}
    for i in range(len(ids)):
        get_sync_frame(cursor, ids[i], frames, sync_queires, i)
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        row_index = 0
        for i in range(len(frames)):
            header_to_add = "Sync id is: " + str(ids[i])
            df = pd.DataFrame([header_to_add])
            df.to_excel(writer, startrow=row_index, index=False, header=False)
            row_index += 1
            frames[i].to_excel(writer, startrow=row_index, index=False)
            row_index = row_index + len(frames[i].index) + 2
    cursor.close()
    con.close()


def get_sync_frame(cursor, sync_id, frames, sync_queries, index):
    sync_queries = [q.replace('%sync_id%', sync_id) for q in sync_queries]
    data_from_sync = run_sync_queries(cursor, sync_queries)
    data = data_from_sync[0]
    frame = {
        'Count': data['count'], 'Name': data['name'], 'Sync Diff Type': data['sync_diff_type'],
        'Provision Status': data['provision_status'], 'Status': data['status']
    }
    df = pd.DataFrame(frame)
    frames[index] = df


def run_sync_queries(cursor, sync_queries):
    data = []
    for i in range(len(sync_queries)):
        cursor.execute(sync_queries[i])
        ans = format_sync(cursor.fetchall())
        data.append(ans)
    return data


def format_sync(syncs):
    new_sync = {'count': [], 'name': [], 'sync_diff_type': [], 'provision_status': [], 'status': []}
    for i in range(len(syncs)):
        count = syncs[i][0]
        name = syncs[i][1]
        sync_diff_type = syncs[i][2]
        provision_stat_id = syncs[i][3]
        status = syncs[i][4]
        new_sync['count'].append(count)
        new_sync['name'].append(name)
        new_sync['sync_diff_type'].append(sync_diff_type)
        new_sync['provision_status'].append(provision_stat_id)
        new_sync['status'].append(status)
    return new_sync
