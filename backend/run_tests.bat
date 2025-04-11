@echo off
REM --------------------------------------------------------
REM run_tests.bat
REM This batch file runs the pytest test suite.
REM It stops on the first failure (--maxfail=1) and
REM disables warnings (--disable-warnings) for a cleaner output.
REM --------------------------------------------------------

REM Change to the backend directory (where manage.py is)
cd /d "%~dp0"

REM Set the Django settings module
set DJANGO_SETTINGS_MODULE=django_app.settings

REM Add current directory to PYTHONPATH for Django to detect it
set PYTHONPATH=%CD%

REM Run pytest using Python
python -m pytest --maxfail=1 --disable-warnings
