#!/bin/bash

# Install dependencies (quotes are required in macOS/Zsh for square brackets)
pip3 install "pypdf[image]" pdfquery

# Check if the pdfs folder exists (with correct spacing)
if [ -d "./pdfs/" ]; then
    echo "Extracting names from PDFs via parser.py..."
    python3 parser.py
else
    echo "Couldn't find the \"pdfs\" folder. Make sure that it exists and is filled with the PDF files."
    exit 1
fi

# Create the output directories (-p prevents errors if they already exist)
mkdir -p ./jpgs
mkdir -p ./jpgs/grade7
mkdir -p ./jpgs/grade8
mkdir -p ./jpgs/grade9
mkdir -p ./jpgs/grade10
mkdir -p ./jpgs/grade11
mkdir -p ./jpgs/grade12


# Run the image extractor
python3 imgextractor.py
