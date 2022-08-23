import time
import os
import sys
import threading
import json
import requests
import mercari


items = mercari.search("Hioki")
items_list = {}

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
            self.sendNotification('Monitoring has started. Yuupii!', title='From Mercari Checker')
        else:
            self.use_module = False
            logger.warning('Alertzy was not configured. Notifications will not be sent to your '
                           'Phone through the Alertzy app.')

    def sendNotification(self, message, title):
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


def searchFor(item_name):
    items = mercari.search(item_name)
    items_list = {}

    for item in items:
        # print("{}, {}, {}, {}, {}, {}".format(item.id, item.status, item.soldOut,
        #         item.price, item.productName, item.productURL))
        items_list[item.id] = [item.productName, item.price, item.soldOut, item.productURL]
    
    return items_list

def compareAndUpdateList(items_retreived, items_new):
    num_dif_items = 0
    different_items = {}
    found_different = False
    for new_key in items_new.keys():
        # print("test key ", new_key)
        found_in_prev_list = False
        for old_key in items_retreived.keys():
            if new_key == old_key:
                found_in_prev_list = True
                #print("found same")
                break
        if not found_in_prev_list:
            num_dif_items += 1
            print("not found!!! new element")
            found_different = True
            different_items[new_key] = items_new[new_key] 
            print(new_key, " ", items_new[new_key])
        else:
            print("Nothing new :(")

    if found_different:
        return items_new, different_items, num_dif_items
    else:
        return items_new, different_items, num_dif_items


def main():
    disable_alertzy  = False
    item_to_search = "Hioki"
    list_retreived = searchFor(item_to_search)
    alertzy = None if disable_alertzy else Alertzy()
    diff_items = {}
    print(list_retreived)
    while(True):
        print("Waiting for update")
        time.sleep(30)
        items_new = searchFor(item_to_search)
        list_retreived, diff_items, num_dif_items = compareAndUpdateList(list_retreived, items_new)
        if num_dif_items < 5:
            for element in diff_items.items():
                alertzy.sendNotification("Master!!, found " + element[0] + " " + element[3]  ,"New " + item_to_search + "!!!")
        else:
            print("too much new eleemnts")
                



if __name__ == '__main__':
    main()