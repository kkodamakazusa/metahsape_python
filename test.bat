rem @echo off
set METASHAPE_PATH="C:\Program Files\Agisoft\Metashape Pro\metashape.exe"
set SCRIPT_DIR=%~dp0

%METASHAPE_PATH% -r %SCRIPT_DIR%\make_align.py
%METASHAPE_PATH% -r %SCRIPT_DIR%\set_drone_coord.py
rem %METASHAPE_PATH% -r %SCRIPT_DIR%\c_test2.py
rem %METASHAPE_PATH% -r %SCRIPT_DIR%\bdens.py
pause
