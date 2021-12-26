import os.path
from flask import *
import pandas as pd
import connect


def start():
    db_credentials = connect.get_db_creds()
    nms_list = request.form.getlist('nms')
    output_file = request.form['output_file']
    if ".xlsx" not in output_file:
        output_file += ".xlsx"
    con = connect.connect(db_credentials)
    cursor = con.cursor()
    # gets the relevant queries
    atrinet_queries = open(os.path.abspath("atrinet.txt")).read().split("\n")
    temp_queries = open(os.path.abspath("temp.txt")).read().split("\n")
    comments_queries = open(os.path.abspath("comments.txt")).read().split("\n")
    layers = create_layers(open("layers.txt").read().split("\n"))
    frames = {}
    for i in range(len(nms_list)):
        # creates a data frame for each NMS chosen
        get_frame(cursor, nms_list[i], frames, atrinet_queries, temp_queries, comments_queries, layers, i)
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for i in range(len(frames)):
            frames[i].to_excel(writer, sheet_name=nms_list[i], index=False)
    cursor.close()
    con.close()
    return output_file


def create_layers(layers):
    new_layers = []
    for i in range(len(layers)):
        new_layers.append(layers[i])
    return new_layers


# this function creates the frame for the NMS
def get_frame(cursor, nms, frames, atrinet_queries, temp_queries, comments_queries, layers, index):
    atrinet_queries = [q.replace('%schema_name%', "MNGP_" + nms) for q in atrinet_queries]
    temp_queries = [q.replace('%schema_name%', "MNGP_" + nms) for q in temp_queries]
    comments_queries = [q.replace('%schema_name%', "MNGP_" + nms) for q in comments_queries]
    atrinet_data = run_fetchone_queries(cursor, atrinet_queries)
    temp_data = run_fetchone_queries(cursor, temp_queries)
    comments_data = run_comments(cursor, comments_queries)
    percentage = get_percentage(atrinet_data, temp_data)
    frame = {
        'Layers': layers,
        "Atrient_count": atrinet_data, "Temp_count": temp_data, 'Percentage (Temp_count/Atrient_count)': percentage,
        "Comments in staging table": comments_data}
    df = pd.DataFrame(frame)
    frames[index] = df


def run_fetchone_queries(cursor, queries):
    data = []
    for i in range(len(queries)):
        cursor.execute(queries[i])
        data.append(cursor.fetchone()[0])
    return data


def run_comments(cursor, queries):
    data = []
    for i in range(len(queries)):
        cursor.execute(queries[i])
        ans = format_comments(cursor.fetchall())
        data.append(ans)
    return data


def format_comments(comments):
    new_comments = []
    for i in range(len(comments)):
        count = str(comments[i][0])
        comment = str(comments[i][1])
        comment = comment.replace("|", "")
        to_add = count + " | " + comment
        new_comments.append(to_add)
    return new_comments


def get_percentage(atrinet_data, temp_data):
    data = []
    for i in range(len(atrinet_data)):
        percentage = round((temp_data[i] / atrinet_data[i]) * 100, 2) if atrinet_data[i] > 0 else 0
        data.append(percentage)
    return data
