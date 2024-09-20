from flask import Flask, render_template
from scraper import scrape_and_download_pdfs
from database import get_worst_performing_high_schools
from pdf_handler import *

app = Flask(__name__)

@app.route('/')
def index():
    #scrape_and_download_pdfs()  # Scrape and download PDFs
    analyze_all_pdfs()  # Analyze downloaded PDFs

    worst_schools = get_worst_performing_high_schools()  # Get data from the database
    return render_template('index.html', schools=worst_schools)

if __name__ == '__main__':
    app.run(debug=True)
