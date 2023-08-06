from platform import version
from pegasus_client.pegasus_handler import Pegasus
from pegasus_client.default_modules.update import module as update
from pegasus_client.default_modules.format import module as format
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from pegasus_client.default_modules.sql import sql_config, SQL_Conn
import os

sql_routes = Blueprint('sql_routes', __name__)


def setup_config():

    config_local = sql_config().load_config()
    config = sql_config().load_config(include_additional=True)

    # reformat sql to be readable
    for query in config['queries']:
        config['queries'][query]['query'] = format().format_sql(
            config['queries'][query]['query'])

        if query not in config_local['queries']:
            config['queries'][query]['location'] = 'external'
        else:
            config['queries'][query]['location'] = 'local'

    for command in config['commands']:

        if command not in config_local['commands']:
            config['commands'][command]['location'] = 'external'
        else:
            config['commands'][command]['location'] = 'local'

    return config


@sql_routes.route('/sqlcreator', methods=['GET', 'POST'])
def sql_creator():

    connection = str(request.form.get('connection', 0))
    query = str(request.form.get('query', 0))

    if connection != '0':

        connection_info = setup_config()['connections'][connection]
        results = SQL_Conn().run_query(connection_info, query)
        query_details = {'connection': connection, 'query': query}

        return render_template('sql/sql_creator.html', config=setup_config(), response=results, query_info=query_details)
    else:
        return render_template('sql/sql_creator.html', config=setup_config(), response=None, query_info=None)


@sql_routes.route('/sqlsetup')
def sql_default():

    return redirect(url_for('sql_routes.sql_setup', setting_type='queries', message=None))


@sql_routes.route('/sql-api/download')
def sql_download():

    dir_path = os.getcwd()

    path = f"{dir_path}/sql.yaml"
    return send_file(path, as_attachment=True)


@sql_routes.route('/sqlsetup/<setting_type>')
def sql_setup(setting_type):

    return render_template('sql/sql_config.html', config=setup_config(), version=update().__VERSION__, setting_type=setting_type, message=None)


# QUERY
@sql_routes.route('/sql-api/newquery', methods=['GET', 'POST'])
def newquery():

    query_name = str(request.form.get('queryName', 0))

    sql_config().new_query(query_name, request.form.get(
        'connection', 0), request.form.get('query', 0))

    flash('New query added.')

    return redirect(url_for('sql_routes.sql_setup', setting_type='queries'))


@sql_routes.route('/sql-api/updatequery', methods=['GET', 'POST'])
def updatequery():

    query_name = str(request.form.get("queryName", 0))
    query = request.form.get('query', 0)
    connection = request.form.get('connection', 0)

    query = query.replace("\r", " ")
    query = query.replace("\n", " ")

    query = ' '.join(query.split())

    sql_config().new_query(query_name, connection, query)

    flash('Query updated.')

    return redirect(url_for('sql_routes.sql_setup', setting_type='queries'))


@sql_routes.route('/sql-api/deletequery/<query>', methods=['GET', 'POST'])
def deletequery(query):

    sql_config().delete_query(query)

    flash('Query deleted.')

    return redirect(url_for('sql_routes.sql_setup', setting_type='queries'))

# COMMAND


@sql_routes.route('/sql-api/deletecommand/<command>', methods=['GET', 'POST'])
def deletecommand(command):

    sql_config().delete_command(command)

    flash('Command deleted.')

    return redirect(url_for('sql_routes.sql_setup', setting_type='commands'))


@sql_routes.route('/sql-api/updatecommand', methods=['GET', 'POST'])
def updatecommand():

    enabled_queries = [i for i in request.values if i !=
                       'commandName' and i != 'query_order']
    command_name = str(request.form.get('commandName', 0))

    query_order = str(request.form.get('query_order', 0))

    sql_config().update_command(command_name, enabled_queries, query_order)

    flash('Command updated.')

    return redirect(url_for('sql_routes.sql_setup', setting_type='commands'))

# SETTINGS


@sql_routes.route('/sql-api/updatesettings', methods=['GET', 'POST'])
def updatesettings():

    enabled_settings = [i for i in request.values]

    additional_config = request.values['additional_config']

    sql_config().update_settings(enabled_settings, additional_config)

    flash('Settings updated.')

    return redirect(url_for('sql_routes.sql_setup', setting_type='settings'))

# CONNECTION


@sql_routes.route('/sql-api/deleteconn/<conn>', methods=['GET', 'POST'])
def deleteconn(conn):
    try:
        sql_config().delete_conn(conn)
        flash(f'Connection ({conn}) deleted.')
    except Exception as e:
        flash(str(e))

    return redirect(url_for('sql_routes.sql_setup', setting_type='connections'))


@sql_routes.route('/sql-api/updateconn', methods=['GET', 'POST'])
def updateconn():
    conn_name = str(request.form.get('connName', 0))

    conn_setup = {
        'type': request.form.get('type', 0),
        'type': request.form.get('type', 0),
        'server': request.form.get('server', 0),
        'database': request.form.get('database', 0),
        'username': request.form.get('username', 0),
        'password': request.form.get('password', 0)
    }

    sql_config().update_conn(conn_name, conn_setup)

    flash('Connection updated.')

    return redirect(url_for('sql_routes.sql_setup', setting_type='connections'))
