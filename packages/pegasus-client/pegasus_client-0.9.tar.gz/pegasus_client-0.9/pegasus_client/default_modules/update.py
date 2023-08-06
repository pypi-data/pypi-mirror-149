from requests import get


class module:
    """Check if you're running the latest version and update to the latest release."""

    def __init__(self):
        self.__VERSION__ = 'v0.18'

        self.repo_info_url = 'https://api.github.com/repos/euanacampbell/pegasus/releases/latest'

        self.repo_url = 'https://github.com/euanacampbell/pegasus'

    def __run__(self, params=None):

        latest_version = get(self.repo_info_url).json()["tag_name"]

        if latest_version == self.__VERSION__:
            return f'\nYou are using the latest version of Pegasus ({self.__VERSION__}).'
        else:
            return f"\nYou are using Pegasus version {self.__VERSION__}; however, version {latest_version} is the latest available. Access the latest version here: {self.repo_url}"
