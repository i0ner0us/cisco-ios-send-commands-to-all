from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from queue import Queue
import threading, sys

"""
    This script will create a queue of every ip int inventry.txt.
    Then it will grab one ip from the queue for a total of 30 active sessions
    and configure each switch with the commands in the cfg_commands variable.
"""

cfg_commands= [
    'vlan 201', 
    'name DMZ',
    'interface Gi1/0/1',
    'switchport access vlan 201'

]

username = sys.argv[1]
password = sys.argv[2]
enable_secret = sys.argv[3]
inventory_file = open('inventory.txt', 'r')

def threadAction(ip):
    try:
        switch = ip.strip()

        # establish a connection to the device
        ssh_connection = ConnectHandler(
            device_type='cisco_ios',
            ip=switch,
            username=username,
            password=password,
            secret=enable_secret
        )

        ssh_connection.find_prompt()

        # enter enable mode
        ssh_connection.enable()

        # send configs to switch
        ssh_connection.send_config_set(cfg_commands)

        # save configuration
        ssh_connection.save_config()
    except (NetMikoTimeoutException, NetMikoAuthenticationException):
        print('could not connect to switch ' + str(ip))

def threader():
  while True:
    # get the job from the top of the queue and run it agains the thread action function
    threadAction(q.get())
    q.task_done()

def main():
    for x in range(30):
        t = threading.Thread(target = threader)
        # this ensures the thread will die when the main thread dies
        # can set t.daemon to False if you want it to keep running
        t.daemon = True
        t.start()

    for ip in inventory_file:
        # place every ip into the queue to be pulled out later and worked on
        q.put(ip)

    q.join()

if __name__ == '__main__':
    print_lock = threading.Lock()
    q = Queue()
    main()
