# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import os
import sys

def changepath(filename):
    system_path = os.popen('''Reg Query "HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\Environment" /v "Path"''').read()
    system_path = system_path.replace("HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\Environment","")
    system_path = system_path.replace("\n","")
    system_path = system_path.replace("    Path    REG_SZ    ","")
    #print(system_path)
    system_path_list = system_path.split(";")
    print("current system path")
    print(system_path_list)

    #current_path = os.environ['path']
    fp = open(filename,"r")
    current_path = fp.readline()
    fp.close()
    #print(current_path)
    current_path = current_path.replace("PATH=","")
    current_path_list = current_path.split(";")
    print("current path of conda")
    print(current_path_list)

    path_to_add = current_path_list
    for item in current_path_list:
        if item in system_path_list:
            path_to_add.remove(item)
    print("path to add:")
    print(path_to_add)
    #cmd = '''Reg add "HKEY_CURRENT_USER\Environment" /v Path /t REG_SZ /d "{}" /f'''.format(";".join(path_to_add).strip())
    cmd = '''Reg add "HKEY_CURRENT_USER\Environment" /v Path /t REG_EXPAND_SZ /d "{}" /f'''.format(
        ";".join(path_to_add).strip())
    
    print(cmd)
    result = os.popen(cmd).read()
    print(result)

changepath(sys.argv[1])

