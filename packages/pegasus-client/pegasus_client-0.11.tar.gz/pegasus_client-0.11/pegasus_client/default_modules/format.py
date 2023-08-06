import sqlparse
import json
import xml.dom.minidom
from pegasus_client.default_modules.generic.clipboard import Clipboard


class module:
    'Format json, sql, xml, and sql lists from your clipboard.'

    def __init__(self):
        self.format_dispatch = {
            'json': self.format_json,
            'sql': self.format_sql,
            'xml': self.format_xml,
            'list': self.format_list
        }

        self.list_output_width = 4

    def __run__(self, params=None):

        format_type = params[0]

        if format_type not in self.format_dispatch:
            raise Exception('format not recognised')

        # use clipboard if no parameter provided
        if len(params) == 1:
            c_board = Clipboard.get_clipboard()
        else:
            c_board = " ".join(params[1:])

        # attempt format
        return_values = []
        try:
            formatted = self.format_dispatch[format_type](c_board)
        except:
            raise Exception(f'unable to format to {format_type}')

        # try to add result to clipboard
        try:
            Clipboard.add_to_clipboard(formatted)
        except:
            return_values.append(
                f'Unable to add formatted to clipboard.')

        return_values.append(f'Formatted {format_type}. ({len(formatted)})')
        return_values.append(formatted)

        return return_values

    def format_json(self, to_format):

        parsed = json.loads(to_format)
        formatted = json.dumps(parsed, indent=4, sort_keys=True)

        return formatted

    def format_sql(self, to_format):

        formatted = sqlparse.format(
            to_format, reindent=True, keyword_case='upper')

        return formatted

    def format_xml(self, to_format):

        dom = xml.dom.minidom.parseString(to_format)
        pretty_xml = dom.toprettyxml()

        return pretty_xml

    def format_list(self, to_format):

        default_bracket = '()'

        if to_format in ['[', ']']:
            to_format = '[]'
        elif to_format in ['(', ')']:
            to_format = '()'

        if to_format in ['()', '[]']:
            default_bracket = to_format
            to_format = Clipboard.get_clipboard()

        # find delimiter
        # already formatted
        if (to_format.startswith('(') and to_format.endswith(')')) or (to_format.startswith('[') and to_format.endswith(']')):
            replace_characters = ['"', "'", '\n', '(', ')', '[', ']']

            for char in replace_characters:
                to_format = to_format.replace(char, '')

            to_list = to_format.split(',')
        elif ',' in to_format:
            to_list = to_format.split(',')
        elif '\n' in to_format:
            to_list = to_format.splitlines()
        else:
            to_list = to_format.split(' ')

        # clean data
        to_list = [item.strip() for item in to_list if item.strip() != '']

        # build new row
        formatted = ''
        for count, row in enumerate(to_list):
            formatted += f"'{row}', "

            # builds a grid instead of a list, easier to read
            if ((count+1) % self.list_output_width == 0) and (count != 0) and (count+1 != len(to_list)):
                formatted += '\n'

        # remove trailing space + comma
        formatted = formatted[:-2]
        formatted = f"{default_bracket[0]}{formatted}{default_bracket[1]}"

        return formatted

    def subcommands(self):

        return list(self.format_dispatch.keys())
