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
    'name KMA-B1-Users',
    'vlan 202',
    'name KMA-B2-Users',
    'vlan 203',
    'name KMA-B3-Users',
    'vlan 204',
    'name KMA-PLC',
    'vlan 205',
    'name KMA-Guest',
    'vlan 209',
    'name KMA-Svr-Mgmt',
    'vlan 210',
    'name KMA-Svr-VM-Network',
    'vlan 220',
    'name KMA-Voice-Deskphones',
    'vlan 222',
    'name KMA-Voice-Wireless',
    'vlan 230',
    'name KMA-AP-Mgmt',
    'vlan 241',
    'name KMA-B1-Cameras',
    'vlan 242',
    'name KMA-B2-Cameras',
    'vlan 243',
    'name KMA-B3-Cameras',
    'vlan 244',
    'name KMA-ISCII',
    'vlan 245',
    'name KMA-Tats-P2PBridge',
    'vlan 250',
    'name KMA-Secure',
    'vlan 291',
    'name KMA-B1-Network-Mgmt',
    'vlan 292',
    'name KMA-B2-Network-Mgmt',
    'vlan 293',
    'name KMA-B3-Network-Mgmt',
    'vlan 298',
    'name KMA-TEA-Network',
    'vlan 299',
    'name KMA-DMZ',
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
