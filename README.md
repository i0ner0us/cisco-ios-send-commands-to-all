# cisco-ios-send-commands-to-all
Send commands to every cisco switch in your inventory.txt file

## Requirements

Python 3 with the following modules:
1. Nemiko
2. Threading
3. Queue

## Using the script

To change the configurations that are sent to the switches, modify the variable `cfg_commands` in the format of a list. Each item in the list is a line of commands to inserted into the switch.

Example:

``cfg_commands = ['this is config line 1', 'this is config line 2',]```
