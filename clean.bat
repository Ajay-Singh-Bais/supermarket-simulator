@echo off
echo Cleaning Python Temporary Files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc *.pyo
echo Cleanup complete!
pause