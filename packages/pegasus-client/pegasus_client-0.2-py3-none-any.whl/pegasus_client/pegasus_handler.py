import traceback
from rich.traceback import install
from os.path import isfile, join
from os import listdir
from importlib.machinery import SourceFileLoader
import sys

import os
from os.path import dirname, basename, isfile, join
import glob


class Pegasus:

    def __init__(self):

        self.modules = {}
        self.modules = self.import_modules()

    def format_input(self, user_input):
        """Takes input from user, separates command and params and returns them"""

        command = user_input.split(' ')[0]

        try:
            param = user_input.split(' ')[1:]
        except:
            param = None

        return {
            'command': command,
            'param': param
        }

    def run_command(self, user_input):

        self.modules = self.import_modules()

        formatted_input = self.format_input(user_input)
        self.user_input = user_input
        command = formatted_input['command']
        param = formatted_input['param']

        try:
            sub_commands_lookup = self.sub_commands()
        except Exception as e:
            # return self.build_return(traceback.format_exc(), error='error')
            return self.build_return(e, error='error')

        sub_commands = list(sub_commands_lookup.keys())

        if command in self.modules:
            module = self.modules[command]
        elif command in sub_commands:  # sub-commands
            param.insert(0, command)
            command = sub_commands_lookup[command]
            module = self.modules[command]
        else:
            return self.build_return(f"'{command}' command not recognised, run 'help' to see available commands.", error='error')

        # catch any errors in the command/module
        # module_result = module.__run__(param)
        # return self.build_return(module_result)

        try:
            module_result = module.__run__(param)
            return self.build_return(module_result)
        except Exception as e:
            # return self.build_return(traceback.format_exc(), error='error')
            return self.build_return(e, error='error')

    def sub_commands(self):

        sub_commands = {}

        for file in self.available_modules():
            try:
                instance = globals()[file]()
            except KeyError:
                instance = self.modules[file]

            try:
                for command in instance.subcommands():
                    sub_commands[command] = file
            except AttributeError:
                pass
        return sub_commands

    def available_modules(self):

        paths = os.path.dirname(os.path.abspath(__file__)) + '/default_modules'

        current_path = os.path.dirname(
            os.path.abspath(__file__)) + '/default_modules'
        files = [f[:-3] for f in listdir(current_path) if isfile(
            join(current_path, f)) and '__init__' not in f and '.py' in f]

        file_paths = {}
        for file in files:
            file_paths[file] = f'{current_path}/{file}.py'

        return file_paths

    def build_return(self, response, error=None):

        if type(response) not in (dict, list):
            response = [response]

        built_response = []
        for item in response:
            if type(item) == int:
                item = str(item)
            new_item = {
                "type": error or self.result_type(item),
                "content": item
            }

            built_response.append(new_item)

        return {
            'command': self.user_input,
            'response': built_response,
            'error': error
        }

    def result_type(self, result):

        if type(result) is str:
            result_type = 'string'
        elif type(result) is bytes:
            result_type = 'string'
        elif type(result) is list:
            result_type = 'list'
            if type(result[0]) is list:
                result_type = 'listoflist'
        elif type(result) is dict:
            result_type = 'dict'
            if type(result[next(iter(result))]) is list:
                result_type = 'dictoflist'
        else:
            result_type = 'error'

        return result_type

    def import_modules(self):

        modules = {}

        file_paths = self.available_modules()
        for file in file_paths:
            try:
                module = SourceFileLoader(
                    file, file_paths[file]).load_module().module()
            except Exception as e:
                # unable to import module
                print(e)

            modules[file] = module

        return modules


if __name__ == "__main__":

    while True:
        text_input = input('\ncommand: ')
        p = Pegasus().run_command(text_input)
