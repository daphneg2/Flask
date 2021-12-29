This is an explanation how to use this tool:

Before starting (cannot download on Amdocs network):
    Installations:
    1. python 3.10
    2. packages:
        a. pip: python get-pip.py
        b. cx_Oracle: pip install cx_Oracle
        c. pandas: pip install pandas
        d. xlsxwriter: pip install xlsxwriter
    3.Oracle Instant Client (download from: https://www.oracle.com/database/technologies/instant-client/downloads.html)

    Configurations needed:
    1. After downloading Oracle Instant Client we need to extract it to a new folder, for example: C:\Users\DAPHNEG\instantclient\instantclient_21_3
    2. copy the folder path (C:\Users\DAPHNEG\instantclient\instantclient_21_3)
    3. Add it to Path in environment variables
    4. change in the app.py the folder in cx_Oracle.init_oracle_client

    Flask:
    This tool is using Flask library and is very easy to work with.
    In order to add another ability to the tool we need to do the following in app.py:
        1. Add a @app.route() with the new path. For example: @app.route('/new_function/', methods=['GET', 'POST]).
        2. After configuring the new route we need to create a new function, within the function we need to state what to do with each methods.
        3. We need to add an import to the head of the file to the new file with the code for the new ability. For example: import new_function.
        4. If we are adding more templates we should add them to the templates' folder.
        5. Add to home_page.html a button with the new redirect

    DB connection:
        The DB connection details should be formatted in the following way:
        username/password@hostname:port/sid
        For example: ADAPTERCONF/ADAPTERCONF@10.234.38.117:1521/PLDACE11

Adding new function:
    After adding the route to the app.py we need to create a new python file and write all our code there
    
    * Note that the queries might take a while, depends on the NMS.