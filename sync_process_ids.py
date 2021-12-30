import os.path
from flask import *
import pandas as pd
import connect


def start():
    db_credentials = connect.get_db_creds()
    output_file = request.form['output_file']
    if ".xlsx" not in output_file:
        output_file += ".xlsx"
    con = connect.connect(db_credentials)
    cursor = con.cursor()
    get_ids = 'select SYNCPROCESSID, NAME, STARTDATE, FINISHDATE, SP2PROVISIONSTATUS, FAILURETEXT from syncprocess order by 1 desc'
    cursor.execute(get_ids)
    ans = format_ids(cursor.fetchall())
    df = pd.DataFrame(ans)
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    cursor.close()
    con.close()
    return output_file


def format_ids(ids):
    data = {'sync process id': [], 'name': [], 'start date': [], 'finish date': [], 'provision status': [],
            'failure text': []}
    for i in range(len(ids)):
        data['sync process id'].append(ids[i][0])
        data['name'].append(ids[i][1])
        data['start date'].append(ids[i][2])
        data['finish date'].append(ids[i][3])
        data['provision status'].append(ids[i][4])
        data['failure text'].append(ids[i][5])
    return data
