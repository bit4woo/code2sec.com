echo "install python evironment with Miniconda2"


if exist C:\ProgramData\Miniconda2\Uninstall-Miniconda2.exe (

set uninstall=
set /p uninstall="echo the miniconda already installed. Do you want to uninstall ?<yes/NO>"

)

if (%uninstall%==y or %uninstall%==yes) (

C:\ProgramData\Miniconda2\Uninstall-Miniconda2.exe /S

) else ( break )


rd/s/q C:\ProgramData\Miniconda2
:rem del folder and subfolder forcely



if exist Miniconda2-latest-Windows-x86_64.exe ( 

start /wait "" Miniconda2-latest-Windows-x86_64.exe /InstallationType=AllUsers /AddToPath=1 /RegisterPython=1 /S /D=C:\ProgramData\Miniconda2
copy ./ C:\ProgramData\Miniconda2\Scripts /y
explorer C:\ProgramData\Miniconda2\Scripts

)

if %USERPROFILE%\Downloads\Miniconda2-latest-Windows-x86_64.exe (

%USERPROFILE%\Downloads\Miniconda2-latest-Windows-x86_64.exe
copy ./ C:\ProgramData\Miniconda2\Scripts /y
explorer C:\ProgramData\Miniconda2\Scripts

) else (

start https://repo.continuum.io/miniconda/Miniconda2-latest-Windows-x86_64.exe

)
pause
