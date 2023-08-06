from platform import version
from pegasus_client.pegasus_handler import Pegasus
from pegasus_client.default_modules.update import module as update
from flask import Blueprint, render_template, request, redirect, url_for

core_routes = Blueprint('core_routes', __name__)
pegasus = Pegasus()


@core_routes.route('/')
def home():

    commands = pegasus.run_command('help')['response']

    return render_template('home.html', info=None, version=update().__VERSION__, commands=commands)


@core_routes.route('/<command>', methods=['GET', 'POST'])
def command(command):
    try:
        data = request.values['param']
    except:
        data = ''

    if command == '':
        return redirect(url_for('home'))

    commands = pegasus.run_command('help')['response']

    command_result = pegasus.run_command(command + ' ' + data)
    command_result['command'] = command
    command_result['param'] = data
    return render_template('home.html', info=command_result, version=update().__VERSION__, commands=commands)
