import time
import os
import sys
import threading
import json
import requests

class Alertzy:

    def __init__(self):
        self.use_module = True
        self.lock = threading.Lock()
        config_filename = 'alertzy_conf.json'
        if os.path.isfile(config_filename):
            print("Found the file")
            with open(config_filename, 'r') as r:
                self.alertzy_key = json.load(r)['alertzy_key']
                print(self.alertzy_key)
            print("Sending notification")
            self.send_notification('Monitoring has started. Yuupii!', title='From Mercari Checker')
        else:
            self.use_module = False
            logger.warning('Alertzy was not configured. Notifications will not be sent to your '
                           'Phone through the Alertzy app.')

    def send_notification(self, message, title):
        # https://alertzy.app/
        if self.use_module:
            with self.lock:
                assert self.alertzy_key is not None
                try:
                    requests.post('https://alertzy.app/send', data={
                        'accountKey': self.alertzy_key,
                        'title': title,
                        'message': message
                    })
                except Exception:
                    return False
                return True


def main():
    disable_alertzy  = False
    alertzy = None if disable_alertzy else Alertzy()

if __name__ == '__main__':
    main()