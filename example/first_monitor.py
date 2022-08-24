import time
import os
import sys
import threading
import json
import requests
import mercari

item_to_search = "hioki"
items = mercari.search(item_to_search)
items_list = {}
running = True
disable_alertzy  = False


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
    try:
        for item in items:
            # print("{}, {}, {}, {}, {}, {}".format(item.id, item.status, item.soldOut,
            #         item.price, item.productName, item.productURL))
            items_list[item.id] = [item.productName, item.price, item.soldOut, item.productURL]
        
        return items_list
    except:
        return items_list
        pass

def compareAndUpdateList(items_retreived, items_new):
    num_dif_items = 0
    different_items = {}
    found_different = False

    if not items_new:
        return items_retreived

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
        return items_retreived, different_items, num_dif_items

def thread_notif():
    global running
    global alertzy
    alertzy.sendNotification("Srated Hb for " + item_to_search  ,"Started Hb")
    while running:
        time.sleep(3600)
        alertzy.sendNotification("Still Alive looking for " + item_to_search  ,"Heartbeat 1h")


alertzy = None if disable_alertzy else Alertzy()
notif_thread = threading.Thread(target = thread_notif)
notif_thread.daemon = True
notif_thread.start()

def main():
    global notif_thread
    global running
    global alertzy
    global item_to_search
    list_retreived = searchFor(item_to_search)
    if not list_retreived:
        list_retreived = searchFor(item_to_search)
    if not list_retreived:
        list_retreived = searchFor(item_to_search)
    diff_items = {}
    print(list_retreived)
    while(True):
        try:
            print("Waiting for update")
            time.sleep(300)
            print("doing search")
            items_new = searchFor(item_to_search)
            list_retreived, diff_items, num_dif_items = compareAndUpdateList(list_retreived, items_new)
            if num_dif_items < 5:
                for element in diff_items.items():
                    alertzy.sendNotification("Master!!, " + element[0] + " " + element[1][3]  ,"New " + item_to_search + "!!!")
            else:
                print("too much new eleemnts")
        except KeyboardInterrupt:
            running = False
            notif_thread.join()
            break


if __name__ == '__main__':
    main()