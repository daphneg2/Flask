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
    atrinet_queries = open("atrinet.txt").read().split("\n")
    temp_queries = open("temp.txt").read().split("\n")
    comments_queries = open("comments.txt").read().split("\n")
    layers = create_layers(open("layers.txt").read().split("\n"))
    frames = {}
    for i in range(len(nms_list)):
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


def run_queries(cursor, queries):
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


def get_frame(cursor, nms, frames, atrinet_queries, temp_queries, comments_queries, layers, index):
    atrinet_queries = [q.replace('%schema_name%', "MNGP_" + nms) for q in atrinet_queries]
    temp_queries = [q.replace('%schema_name%', "MNGP_" + nms) for q in temp_queries]
    comments_queries = [q.replace('%schema_name%', "MNGP_" + nms) for q in comments_queries]
    atrinet_data = run_queries(cursor, atrinet_queries)
    temp_data = run_queries(cursor, temp_queries)
    comments_data = run_comments(cursor, comments_queries)
    frame = {
        'Layers': layers,
        "Atrient_count": atrinet_data, "Temp_count": temp_data, "Comments in staging table": comments_data}
    df = pd.DataFrame(frame)
    frames[index] = df


def format_comments(comments):
    new_comments = []
    for i in range(len(comments)):
        count = str(comments[i][0])
        comment = str(comments[i][1])
        comment = comment.replace("|", "")
        to_add = count + " | " + comment
        new_comments.append(to_add)
    return new_comments
