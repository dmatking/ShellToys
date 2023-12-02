@echo off
setlocal enabledelayedexpansion

REM Create the escape character
for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

REM Check if an environment variable name and optional search word are passed as command line arguments
if "%~1"=="" (
    echo Please provide an environment variable name.
    echo Usage: %0 ENV_VARIABLE_NAME [OPTIONAL_SEARCH_WORD]
    goto :eof
)

REM Use the provided environment variable name
set "VAR_NAME=%~1"
set "VAR=!%VAR_NAME%!"

REM Check if a search word was provided
set "SEARCH_WORD=%~2"

REM Check if the variable is empty
if "!VAR!"=="" (
    echo The environment variable %VAR_NAME% is empty or does not exist.
    goto :eof
)

REM Define ANSI escape sequences for light yellow and reset
set "YELLOW=!ESC![93m"
set "RESET=!ESC![0m"

REM Loop through each item separated by a semicolon
for %%i in ("!VAR:;=" "!") do (
    set "LINE=%%~i"

    REM If a search word is provided, only process lines containing that word
    if not "!SEARCH_WORD!"=="" (
        echo !LINE! | findstr /I /C:"!SEARCH_WORD!" > nul
        if not errorlevel 1 (
            if "!LINE!" NEQ "" (
                echo !LINE!
            ) else (
                echo !YELLOW![Consecutive semicolons detected.]!RESET!
            )
        )
    ) else (
        if "!LINE!" NEQ "" (
            echo !LINE!
        ) else (
            echo !YELLOW![Consecutive semicolons detected.]!RESET!
        )
    )
)

endlocal
