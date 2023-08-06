class module:
    'Provide code snippets'

    def __init__(self):

        pass

    def __run__(self, params=None):

        snippet_type = params[0]

        if snippet_type == 'help':
            return self.help()

        code_snippet = self.grab_snippet(snippet_type)

        return code_snippet

    def grab_snippet(self, snippet_type):

        output = ''
        use_line = False
        area_code = f"'''{snippet_type}'''"

        f = open("pegasus/default_modules/generic/snippets.py", "r")

        print(area_code)

        for row in f:
            row_formatted = row.replace('\n', '')

            if row_formatted == area_code and use_line == False:
                use_line = True
                continue
            elif row_formatted == area_code and use_line == True:
                break

            if use_line == True:
                output = output + row

        formatted = [[output]]
        return formatted

    def help(self):
        commands = []
        f = open("pegasus/default_modules/generic/snippets.py", "r")

        for row in f:
            if "'''" in row:
                commands.append(row.split("'''")[1])

        return list(set(commands))

    def subcommands(self):

        return list(self.format_dispatch.keys())


if __name__ == '__main__':

    s = snippet()

    s.__run__(['csv'])
