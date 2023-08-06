import requests
import datetime


class module:
    'Check that an internet connection exists.'

    def __init__(self):
        self.timeout = 10
        self.default_url = 'https://google.co.uk'

    def __run__(self, params=None):

        if params[0] != '':
            r = self.check_connection(params[0])
        else:
            print('no command')
            r = self.check_connection()

        if str(r) == '200':
            return 'connection made'
        else:
            return 'no connection made'

    def check_connection(self, url=None):

        if not url:
            url = self.default_url

        end_time = datetime.datetime.now() + datetime.timedelta(0, self.timeout)

        while datetime.datetime.now() < end_time:
            try:
                pr = requests.get(
                    url, timeout=self.timeout).status_code  # 10 seconds
                if pr == 200:
                    return pr
            except:
                raise Exception('Unable to find URL.')
