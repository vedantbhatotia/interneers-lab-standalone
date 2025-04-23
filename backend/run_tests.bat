@echo off
REM --------------------------------------------------------
REM run_tests.bat
REM This batch file runs the pytest test suite.
REM It stops on the first failure (--maxfail=1) and
REM disables warnings (--disable-warnings) for a cleaner output.
REM --------------------------------------------------------

cd /d "%~dp0"

set DJANGO_SETTINGS_MODULE=django_app.settings

set PYTHONPATH=%CD%

REM Run pytest using Python
python -m pytest --maxfail=1 --disable-warnings
