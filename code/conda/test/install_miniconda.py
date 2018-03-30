# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'


import os
import sys
import urllib

global_switch =r"""# !/usr/bin/env python
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
    system_path_list = list(set(system_path_list))
    print("current system path: ")
    print("\n".join(system_path_list))

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
    current_path_list = list(set(current_path_list))
    print("current path of conda: ")
    print("\n".join(current_path_list))

    if len(ispython(current_path_list)) == 1:
        print("one python dir detected. correct")
    elif len(ispython(current_path_list)) >= 2:
        print("multiple python dirs detected, cleaning ALL! you need to run activate again")
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

def striplist(input_list):
    result = []
    if isinstance(input_list,list):
        for item in input_list:
            item = item.strip()
            result.append(item)
        return result
    else:
        print "Error, the input type is not list!"

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
            for x in path_list:
                if x.startswith(item):
                    no_python_path_list.remove(x)
    return no_python_path_list

changepath(sys.argv[1])
#changepath("C:\ProgramData\Miniconda2\Scripts\\tmppath.txt")

"""

activate_bat_add =r"""

@echo %path% > %~dp0\..\Scripts\tmppath.txt
@start %~dp0\..\python.exe %~dp0\..\Scripts\global_switch.py %~dp0\..\Scripts\tmppath.txt
@call %~dp0\..\Scripts\RefreshEnv.cmd

"""

RefreshEnv_cmd =r"""@echo off
::
:: RefreshEnv.cmd
::
:: Batch file to read environment variables from registry and
:: set session variables to these values.
::
:: With this batch file, there should be no need to reload command
:: environment every time you want environment changes to propagate

::echo "RefreshEnv.cmd only works from cmd.exe, please install the Chocolatey Profile to take advantage of refreshenv from PowerShell"
echo | set /p dummy="Refreshing environment variables from registry for cmd.exe. Please wait..."

goto main

:: Set one environment variable from registry key
:SetFromReg
    "%WinDir%\System32\Reg" QUERY "%~1" /v "%~2" > "%TEMP%\_envset.tmp" 2>NUL
    for /f "usebackq skip=2 tokens=2,*" %%A IN ("%TEMP%\_envset.tmp") do (
        echo/set "%~3=%%B"
    )
    goto :EOF

:: Get a list of environment variables from registry
:GetRegEnv
    "%WinDir%\System32\Reg" QUERY "%~1" > "%TEMP%\_envget.tmp"
    for /f "usebackq skip=2" %%A IN ("%TEMP%\_envget.tmp") do (
        if /I not "%%~A"=="Path" (
            call :SetFromReg "%~1" "%%~A" "%%~A"
        )
    )
    goto :EOF

:main
    echo/@echo off >"%TEMP%\_env.cmd"

    :: Slowly generating final file
    call :GetRegEnv "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" >> "%TEMP%\_env.cmd"
    call :GetRegEnv "HKCU\Environment">>"%TEMP%\_env.cmd" >> "%TEMP%\_env.cmd"

    :: Special handling for PATH - mix both User and System
    call :SetFromReg "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" Path Path_HKLM >> "%TEMP%\_env.cmd"
    call :SetFromReg "HKCU\Environment" Path Path_HKCU >> "%TEMP%\_env.cmd"

    :: Caution: do not insert space-chars before >> redirection sign
    echo/set "Path=%%Path_HKLM%%;%%Path_HKCU%%" >> "%TEMP%\_env.cmd"

    :: Cleanup
    del /f /q "%TEMP%\_envset.tmp" 2>nul
    del /f /q "%TEMP%\_envget.tmp" 2>nul

    :: capture user / architecture
    SET "OriginalUserName=%USERNAME%"
    SET "OriginalArchitecture=%PROCESSOR_ARCHITECTURE%"

    :: Set these variables
    call "%TEMP%\_env.cmd"

    :: reset user / architecture
    SET "USERNAME=%OriginalUserName%"
    SET "PROCESSOR_ARCHITECTURE=%OriginalArchitecture%"

    echo | set /p dummy="Finished."
    echo .
"""



def download(url="https://repo.continuum.io/miniconda/Miniconda2-latest-Windows-x86_64.exe",filename="Miniconda2-latest-Windows-x86_64.exe"):
    while True:
        if os.path.exists(filename):
            print "Download complete."
            return True
        else:
            if os.path.exists(filename):

                print "Install to C:\ProgramData\Miniconda2"

            print "Miniconda2-latest-Windows-x86_64.exe NOT Found in current path. will download from Internet"
            input = raw_input("Please check network and input correct URL [Default:{0}]".format(url))
            if "input".startswith("http"):
                url = input
            urllib.urlretrieve(url, "Miniconda2-latest-Windows-x86_64.exe")


def install(filename="Miniconda2-latest-Windows-x86_64.exe"):
    download()
    print "Installing to C:\ProgramData\Miniconda2"
    #os.popen('''start /wait "" Miniconda2-latest-Windows-x86_64.exe /InstallationType=AllUsers /AddToPath=1 /RegisterPython=0 /S /D=C:\ProgramData\Miniconda2''')
    #/AddToPath= 将conda 加到path中
    # 将python路径加到path中，0代表添加到当前用户的path ，1代表添加到系统的path--对所有用户起效。
    #因为全局切换的实质就是配置环境变量，为了避免影响，这里这两个选项都不启用
    os.popen('''start /wait "" Miniconda2-latest-Windows-x86_64.exe /InstallationType=AllUsers /S /D=C:\ProgramData\Miniconda2''')
    #如果默认将C:\ProgramData\Miniconda2中的python加入到path，将导致冲突，后续的全局切换将不起作用。
    print "Install Complete!"

def config():
    print "start config"
    open("C:\ProgramData\Miniconda2\Scripts\global_switch.py","w").writelines(global_switch)
    open("C:\ProgramData\Miniconda2\Scripts\\activate.bat", "a").writelines(activate_bat_add)
    open("C:\ProgramData\Miniconda2\Scripts\RefreshEnv.cmd", "w").writelines(RefreshEnv_cmd)
    print "config complete. \nCommon used commands:\n conda update conda \n conda env list \n conda create -n py27 python=2.7"

def uninstall(filename= "C:\ProgramData\Miniconda2\Uninstall-Miniconda2.exe"):
    if os.path.exists(os.path.abspath(filename)):
        while True:
            choice = raw_input("the Miniconda Already Exist in {0} \nDo you want to uninstall firstly?[Yes/no]".format(os.path.abspath(filename)))
            if choice.lower() in ["y","yes",""]:
                try:
                    cmd = os.popen('''taskkill  /IM  python.exe /F'''.format(filename)).read()
                    cmd = os.popen('''taskkill  /IM  conda.exe /F'''.format(filename)).read()
                except Exception,e:
                    pass
                cmd = os.popen('''start /wait "" {0} /S'''.format(filename)).read()
                cmd = os.remove(os.path.abspath(filename))
            elif choice.lower() in ["n","no"]:
                break

def update():
    os.popen("conda update conda")

if __name__ == "__main__":
    #filename = raw_input("Please Input the Minicoda filename[Fefault:Miniconda2-latest-Windows-x86_64.exe]")
    #uninstall()
    #install()
    config()