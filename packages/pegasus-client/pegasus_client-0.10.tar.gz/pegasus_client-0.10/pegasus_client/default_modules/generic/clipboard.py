import pyperclip


class Clipboard:

    def get_clipboard():
        try:
            return pyperclip.paste()
        except:
            pass

    def add_to_clipboard(value):
        try:
            pyperclip.copy(value)
        except:
            pass
