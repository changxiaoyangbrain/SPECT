@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo          SPECT Project One-Click Deployment
echo ========================================================
echo.

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

:: 2. Setup Virtual Environment
if not exist "venv" (
    echo [INFO] Creating virtual environment 'venv'...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Virtual environment 'venv' already exists.
)

:: 3. Install Dependencies
echo [INFO] Installing/Updating dependencies...
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: 4. Run Main Pipeline
echo.
echo [INFO] Running Main Reconstruction Pipeline...
.\venv\Scripts\python.exe main_pipeline.py
if %errorlevel% neq 0 (
    echo [ERROR] Main pipeline execution failed.
    pause
    exit /b 1
)

:: 5. Generate Visualizations
echo.
echo [INFO] Generating Visualizations...
.\venv\Scripts\python.exe visualize_results.py
if %errorlevel% neq 0 (
    echo [ERROR] Visualization generation failed.
    pause
    exit /b 1
)

:: 6. Generate Report
echo.
echo [INFO] Generating Final Report...
.\venv\Scripts\python.exe generate_refined_report.py
if %errorlevel% neq 0 (
    echo [ERROR] Report generation failed.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo [SUCCESS] All tasks completed successfully!
echo ========================================================
echo.
echo Outputs:
echo - Reconstruction: MyRecon.dat, MyFiltered.dat
echo - Visualizations: pictures/ folder
echo - Reports:        reports/ folder
echo.
pause
