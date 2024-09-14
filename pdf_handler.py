import os
import requests
from PyPDF2 import PdfReader
from database import save_school_performance_data

DOWNLOAD_DIR = 'downloads/'


def download_pdf(url):
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    pdf_name = os.path.join(DOWNLOAD_DIR, url.split('/')[-1])

    if not os.path.exists(pdf_name):
        print(f"Downloading PDF: {pdf_name} from {url}")  # Show URL being downloaded
        response = requests.get(url)
        with open(pdf_name, 'wb') as f:
            f.write(response.content)
        print(f"Download complete: {pdf_name}")  # Confirm download
    else:
        print(f"PDF already exists: {pdf_name}")


def analyze_all_pdfs():
    print("Analyzing downloaded PDFs...")
    pdf_count = 0  # Keep track of how many PDFs are processed
    for pdf_file in os.listdir(DOWNLOAD_DIR):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(DOWNLOAD_DIR, pdf_file)
            analyze_pdf(pdf_path)
            pdf_count += 1
    print(f"Finished analyzing {pdf_count} PDFs.")  # Summary


def analyze_pdf(pdf_path):
    print(f"Analyzing PDF: {pdf_path}")
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        text = ''
        for page_num, page in enumerate(reader.pages):  # Get page number
            text += page.extract_text() or ''
            print(f"  Extracted text from page {page_num + 1}")  # Show page progress

        if 'high school' in text.lower():  # Check if it's a high school report
            print("  High school report found.")
            extract_performance_data(text)
        else:
            print("  Not a high school report.")


def extract_performance_data(text):
    # Implement logic to parse performance data and save to the database
    performance_data = {}  # Extracted data
    print("  Extracting performance data...")
    # Add more specific print statements here as you implement data extraction
    save_school_performance_data(performance_data)