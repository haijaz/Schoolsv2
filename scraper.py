import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # Import urljoin to handle relative URLs
from pdf_handler import download_pdf, analyze_all_pdfs

def scrape_and_download_pdfs():
    url = "https://mydata.dallasisd.org/SL/SD/cdp.jsp"
    print(f"Scraping URL: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get absolute URLs for PDF links
    pdf_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
    print(f"Found {len(pdf_links)} PDF links.")

    # Download all PDFs first
    for link in pdf_links:
        print(f"Downloading PDF: {link}")
        download_pdf(link)  # Download each PDF

    print("All PDFs downloaded. Now processing them...")
    analyze_all_pdfs()
    return pdf_links  # Return the list of PDF links for further processing
