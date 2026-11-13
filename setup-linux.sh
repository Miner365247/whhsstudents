pip install pypdf[image] pdfquery
if [ -d "./pdfs/" ]; then 
	echo "Extracting names from PDFs via parser.py..."
	python3 parser.py
else
	echo "Couldn't find the \"pdfs\" folder. Make sure that it exists and is filled with the PDF files."
	exit 1
fi
mkdir ./jpgs
mkdir ./jpgs/grade7
mkdir ./jpgs/grade8
mkdir ./jpgs/grade9
mkdir ./jpgs/grade10
mkdir ./jpgs/grade11
mkdir ./jpgs/grade12
python3 imgextractor.py
