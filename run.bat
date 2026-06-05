@echo off
REM ============================================================================
REM  run.bat - Task runner for the SSC/GBS Agent Suite
REM  Mirrors the three tasks defined in .claude\launch.json
REM
REM  Usage:
REM    run.bat update       Refresh CR market data from CINDE/PROCOMER (writes files)
REM    run.bat update-dry   Preview the CR data refresh (no files written, verbose)
REM    run.bat build        Regenerate the Excel templates into templates\
REM    run.bat help         Show this help
REM ============================================================================
setlocal

REM Always run from the directory this script lives in (handles spaces in path).
pushd "%~dp0"

REM Resolve a Python launcher: prefer the 'py' launcher, fall back to 'python'.
where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py"
) else (
    set "PY=python"
)

if "%~1"=="" goto :help
if /i "%~1"=="help"       goto :help
if /i "%~1"=="-h"         goto :help
if /i "%~1"=="--help"     goto :help
if /i "%~1"=="/?"         goto :help
if /i "%~1"=="update"     goto :update
if /i "%~1"=="update-dry" goto :update_dry
if /i "%~1"=="build"      goto :build

echo [run] Unknown command: "%~1"
echo.
goto :help

:update
echo [run] Refreshing Costa Rica data from CINDE/PROCOMER...
%PY% scripts\update_cr_data.py
goto :done

:update_dry
echo [run] Previewing Costa Rica data refresh (dry-run)...
%PY% scripts\update_cr_data.py --dry-run --verbose
goto :done

:build
echo [run] Rebuilding Excel templates into templates\...
%PY% scripts\build_excel_templates.py
goto :done

:help
echo.
echo SSC/GBS Agent Suite - task runner
echo.
echo   run.bat update       Refresh CR market data from CINDE/PROCOMER (writes files)
echo   run.bat update-dry   Preview the CR data refresh (no files written, verbose)
echo   run.bat build        Regenerate the Excel templates into templates\
echo   run.bat help         Show this help
echo.
echo Python launcher in use: %PY%
echo.
goto :done

:done
set "RC=%errorlevel%"
popd
endlocal & exit /b %RC%
