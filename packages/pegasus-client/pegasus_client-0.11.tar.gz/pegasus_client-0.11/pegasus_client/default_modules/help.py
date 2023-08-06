from pegasus_client.pegasus_handler import Pegasus


class module:
    'Find all available commands'

    def __init__(self):

        pass

    def __run__(self, params=None):

        p = Pegasus()

        help_commands = [['Command', 'Description']]
        sub_commands = [['Command', 'Module']]

        for file in p.available_modules():

            if file not in p.modules:
                help_commands.append([file, 'Error, not imported.--'])
                continue

            # get description and subcommands
            try:
                instance = p.modules[file]
                description = instance.__doc__
                module_subcommands = []
                for sub_command in instance.subcommands():
                    module_subcommands.append(sub_command)
            except AttributeError:
                module_subcommands = []

            help_commands.append([file, description])

            # format sub-commands for the table
            if module_subcommands:
                for c in module_subcommands:
                    sub_commands.append(
                        [c, f'{file}'])

        return ['Module Commands', help_commands, 'Module Sub-Commands', sub_commands]
