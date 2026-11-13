@echo off

:: Install dependencies (quotes are needed around pypdf[image] so Windows doesn't misinterpret the brackets)
pip install "pypdf[image]" pdfquery

:: Check if the pdfs folder exists
if exist .\pdfs\ (
    echo Extracting names from PDFs via parser.py...
    python parser.py
) else (
    echo Couldn't find the "pdfs" folder. Make sure that it exists and is filled with the PDF files.
    exit /b 1
)

:: Create the output directories (2>nul suppresses errors if the folders already exist)
mkdir .\jpgs 2>nul
mkdir .\jpgs\grade7 2>nul
mkdir .\jpgs\grade8 2>nul
mkdir .\jpgs\grade9 2>nul
mkdir .\jpgs\grade10 2>nul
mkdir .\jpgs\grade11 2>nul
mkdir .\jpgs\grade12 2>nul


:: Run the image extractor
python imgextractor.py

pause
