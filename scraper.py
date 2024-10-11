import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # Import urljoin to handle relative URLs
from pdf_handler import download_pdf, analyze_all_pdfs
import os

def scrape_and_download_pdfs():
    url = "https://mydata.dallasisd.org/SL/TAKS/index.jsp"
    print(f"Scraping URL: {url}")
    response = requests.get(url)
    print(f"Response code: {response.status_code}") # Check if request was successful
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get absolute URLs for PDF links
    pdf_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
    print(f"Found {len(pdf_links)} PDF links.")

    # Download all PDFs first
    for link in pdf_links:
        pdf_name = os.path.join("files", link.split('/')[-1])
        if not os.path.exists(pdf_name):
            print(f"Downloading PDF: {link}")
            download_pdf(link)  # Download each PDF
        else:
            print(f"PDF already exists: {pdf_name}. Skipping download.")

    print("All PDFs downloaded")
    return True