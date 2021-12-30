import os.path
from flask import *
import cx_Oracle
import transformation_count
import sync_diffs
import sync_process_ids

app = Flask(__name__)
IS_DEV = app.env == 'development'


@app.route('/', methods=['GET'])
def welcome():
    return render_template('home_page.html')


@app.route('/transformation_count/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        output_file = transformation_count.start()
        path = os.path.abspath(output_file)
        return send_file(path)
    return render_template('check_box.html')


@app.route('/sync_diffs/', methods=['GET', 'POST'])
def sync_ids():
    if request.method == 'POST':
        output_file = sync_diffs.start()
        path = os.path.abspath(output_file)
        return send_file(path)
    return render_template('sync_ids.html')


@app.route('/sync_process_ids/',  methods=['GET', 'POST'])
def process_ids():
    if request.method == 'POST':
        output_file = sync_process_ids.start()
        path = os.path.abspath(output_file)
        return send_file(path)
    return render_template('sync_process_ids.html')


if __name__ == '__main__':
    # this establishes the initial client
    cx_Oracle.init_oracle_client(lib_dir='C:\\Users\\DAPHNEG\\instantclient\\instantclient_21_3')
    app.run(use_reloader=True)
