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
    data = {'sync process id': [], 'name': [], 'start date': [], 'finish date': [], 'provision status': [], 'failure text': []}
    for i in range(len(ids)):
        id = ids[i][0]
        name = ids[i][1]
        start = ids[i][2]
        end = ids[i][3]
        status = ids[i][4]
        failure = ids[i][5]
        data['sync process id'].append(id)
        data['name'].append(name)
        data['start date'].append(start)
        data['finish date'].append(end)
        data['provision status'].append(status)
        data['failure text'].append(failure)
    return data
