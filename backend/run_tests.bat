
@echo off
REM Prevents the commands in the script from being printed to the command window as they are executed.



REM --------------------------------------------------------
REM run_tests.bat
REM This batch file runs  pytest test suite.
REM It stops on the first failure (--maxfail=1) and
REM disables warnings (--disable-warnings) for a cleaner output.
REM --------------------------------------------------------


REM Run pytest using Python. 
python -m pytest --maxfail=1 --disable-warnings 


@REM bat file contains series of commands that Windows will execute in the order they are written in the file

@REM they are mainly used to automate repetitive tasks

@REM in this running this script will execute the complete test_suite with all the additional commands