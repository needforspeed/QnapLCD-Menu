#!/usr/bin/env python3
import sys
import os
import time
import qnaplcd
import platform
import subprocess
import socket
import threading
import json

DISPLAY_TIMEOUT = 30    # seconds

PORT = '/dev/ttyS1'     # same as default
PORT_SPEED = 1200

lcd = None

lcd_timer = None
def lcd_on():
    global lcd_timer

    lcd.backlight(True)

    if lcd_timer:
        lcd_timer.cancel()

    lcd_timer = threading.Timer(DISPLAY_TIMEOUT, lambda: lcd.backlight(False))
    lcd_timer.start()

def shell(cmd):
    return subprocess.check_output(cmd, shell=True, universal_newlines=True).strip()

def show_version():
    sys_name = platform.node()
    sys_vers = f'{platform.system()} ({platform.machine()})'
    lcd.clear()
    lcd.write(0, [sys_name, sys_vers])

def show_uptime():
    #  21:16:52 up  3:09,  5 users,  load average: 1.33, 1.52, 1.58
    [uptime, users, load_avg] = map(str.strip, shell('uptime').split(',', 2))
    [ts, _, up] = [x for x in map(str.strip, uptime.split(' ')) if x]
    
    [load, avg, _l1, _l5, _l15] = load_avg.split(' ')

    lcd.clear()
    lcd.write(0, [f'Up {up}, {users}', f'{_l1} {_l5} {_l15}'])

ip_addresses = []
def add_ips_to_menu():
    def get_kind(iface):
        if 'linkinfo' in iface:
            if 'info_kind' in iface['linkinfo']:
                return iface['linkinfo']['info_kind']

        return ''

    def get_ipv4(iface):
        if 'addr_info' in iface:
            for addr in iface['addr_info']:
                if addr['family'] == 'inet':
                    return addr['local']

        return '0.0.0.0'

    ip_json = json.loads(shell('ip -details -json address show'))
    ip_addresses.clear()
    for iface in ip_json:
        if iface['link_type'] == 'loopback':
            continue

        if get_kind(iface) not in ['', 'tun']:
                continue

        ip_addresses.append(( iface['ifname'], get_ipv4(iface)))

    while show_ip in menu:
        menu.remove(show_ip)

    for _ in ip_addresses:
        menu.append(show_ip)

def show_ip():
    ip_index = 0
    for index in range(menu_item):
        if menu[index] == show_ip:
            ip_index += 1

    lcd.clear()
    lcd.write(0, [f'{ip_addresses[ip_index][0]}', f'{ip_addresses[ip_index][1]}'])

#
# Menu
#
menu_item = 0
menu = [
    show_version,
    show_uptime
]

def response_handler(command, data):
    global menu_item, lcd_timeout
    prev_menu = menu_item

    #print(f'RECV: {command} - {data:#04x}')

    if command == 'Switch_Status':
        lcd_on()

        if data == 0x01: # up
            menu_item = (menu_item - 1) % len(menu)

        if data == 0x02: # down
            menu_item = (menu_item + 1) % len(menu)

    if prev_menu != menu_item:
        #print(f'SHOW: {menu_item}')
        menu[menu_item]()


def main():
    global lcd
    lcd = qnaplcd.QnapLCD(PORT, PORT_SPEED, response_handler)
    lcd_on()
    lcd.reset()
    lcd.clear()

    quit = False
    while not quit:
        add_ips_to_menu()
        menu[menu_item]()

        print('sleep...')
        time.sleep(30)

    lcd.backlight(False)

main()
