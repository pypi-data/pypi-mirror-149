
class module:
    """Tagline here for description of the module. Used when running the default 'help' command."""

    def __init__(self):
        pass

    def __run__(self, params=None):

        format_dispatch = {
            'string': 'testing strings',
            'stringinlist': ['testing strings'],
            'int': 42,
            'intinlist': [42],
            'list_of_strings': ['hello', 'my', 'name', 'is', 'test'],
            'list_of_ints': [14, 19, 41, 1242, 0],
            'list_of_lists': [['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test'], ['hello', 'my', 'name', 'is', 'test']],
            'list_of_dicts': [{'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}, {'hello': 'test', 'hello': 'test',  'hello': 'test',  'hello': 'test'}]

        }

        return_all = []

        for format_type in format_dispatch:
            return_all.append(f"%bold%{format_type}")
            return_all.append(format_dispatch[format_type])

        return return_all

    def sub_commands(self):
        """Provide a list of sub-commands that can be called directly without the module code."""

        return []
