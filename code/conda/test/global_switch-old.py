# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
__filename__ = 'global_switch.py'

import os
import sys

def changepath(filename):
    # get the system path
    system_path = os.popen('''Reg Query "HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\Environment" /v "Path"''').read()
    system_path = system_path.replace("HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\Environment","")
    system_path = system_path.replace("\n","")
    system_path = system_path.replace("    Path    REG_SZ    ","")
    system_path = system_path.replace("    Path    REG_EXPAND_SZ    ","")
    #print(system_path)
    system_path_list = system_path.split(";")
    system_path_list = striplist(system_path_list)
    system_path_list = clean_path(system_path_list)
    system_path_list = list(set(system_path_list))
    print("current system path: ")
    print("\n".join(system_path_list))

    # clean system path ---delete python path in it

    if len(ispython(system_path_list)) > 0:
        print("system path contain python dir, cleaning...")
        system_path_list = remove_python_path(system_path_list)
        cmd = '''Reg add "HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\Environment" /v Path /t REG_SZ /d "{}" /f'''.format(";".join(system_path_list).strip())
        result = os.popen(cmd).read()
        print(result)
        print("system path cleaning done")

    # get the current path, it's temp, not write to register.
    #current_path = os.environ['path']
    fp = open(filename,"r")
    current_path = fp.readline()
    fp.close()
    #print(current_path)
    current_path = current_path.replace("PATH=","")
    current_path_list = current_path.split(";")
    current_path_list = striplist(current_path_list)
    current_path_list = clean_path(current_path_list)
    current_path_list = list(set(current_path_list))
    print("current path of conda: ")
    print("\n".join(current_path_list))

    if len(ispython(current_path_list)) == 1:
        print("one python dir detected. correct")
    elif len(ispython(current_path_list)) >= 2:
        print("the path that add to config contains multiple python dirs, cleaning ALL! you need to run activate again")
        current_path_list = remove_python_path(current_path_list)


    path_to_add = current_path_list
    for item in current_path_list:
        if item in system_path_list:
            path_to_add.remove(item)
    print("path to add: ")
    print("\n".join(path_to_add))
    #cmd = '''Reg add "HKEY_CURRENT_USER\Environment" /v Path /t REG_SZ /d "{}" /f'''.format(";".join(path_to_add).strip())
    cmd = '''Reg add "HKEY_CURRENT_USER\Environment" /v Path /t REG_EXPAND_SZ /d "{}" /f'''.format(";".join(path_to_add).strip())
    
    print(cmd)
    result = os.popen(cmd).read()
    print(result)


def ispython(path_list):
    python_path_list = []
    for item in path_list:
        pythonfile = os.path.join(item,"python.exe")
        if os.path.exists(pythonfile):
            python_path_list.append(item)
    return list(set(python_path_list))

def remove_python_path(path_list):
    to_remove = ispython(path_list)
    no_python_path_list= path_list
    if len(to_remove)>0:
        for item in to_remove:
            no_python_path_list.remove(item)
            for x in path_list:
                if x.startwith(item):
                    no_python_path_list.remove(path)
    return no_python_path_list

def clean_path(path_list): # del useless dir
    result_list = path_list
    for item in path_list:
        if os.path.exists(item):
            pass
        else:
            result_list.remove(item)
    return result_list


def striplist(input_list):
    result = []
    if isinstance(input_list,list):
        for item in input_list:
            item = item.strip()
            result.append(item)
        return result
    else:
        print "Error, the input type is not list!"


#changepath(sys.argv[1])
changepath("C:\ProgramData\Miniconda2\Scripts\\tmppath.txt")

