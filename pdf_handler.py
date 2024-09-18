import os
import requests
from PyPDF2 import PdfReader
from database import save_school_performance_data

DOWNLOAD_DIR = 'downloads/'


def download_pdf(url):
    print(f"Starting download process for PDF at URL: {url}")
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        print(f"Created directory: {DOWNLOAD_DIR}")

    pdf_name = os.path.join(DOWNLOAD_DIR, url.split('/')[-1])

    if not os.path.exists(pdf_name):
        print(f"Downloading PDF: {pdf_name} from {url}")  # Show URL being downloaded
        response = requests.get(url)
        print(f"Download status code: {response.status_code}")  # Check for successful download
        if response.status_code == 200:
            with open(pdf_name, 'wb') as f:
                f.write(response.content)
            print(f"Download complete: {pdf_name}")  # Confirm download
        else:
            print(f"Error downloading PDF: {url}. Status code: {response.status_code}")
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
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            total_pages = len(reader.pages)
            text = ''
            for page_num, page in enumerate(reader.pages):  # Get page number
                text += page.extract_text() or ''
                print(f"  Extracted text from page {page_num + 1} of {total_pages}")  # Show page progress

            if 'high school' in text.lower():  # Check if it's a high school report
                print("  High school report found.")
                extracted_data = extract_performance_data(text)
                if extracted_data:
                    print("  Data extracted successfully. Saving to database...")
                    save_school_performance_data(extracted_data)
                else:
                    print("  No data extracted from this report.")
            else:
                print("  Not a high school report.")
    except Exception as e:
        print(f"  Error analyzing PDF: {e}")


def extract_performance_data(text):
    """Extracts performance data from the text content of a PDF.

    Args:
        text (str): The extracted text content of the PDF.

    Returns:
        dict: A dictionary containing the extracted performance data.
    """

    performance_data = {}  # Initialize an empty dictionary to store the data
    print("  Extracting performance data...")

    # --- STAAR EOC Exam Results ---
    print("    Looking for STAAR EOC results...")
    performance_data['staar_eoc'] = extract_section_data(text, "STAAR EOC Results",
                                                         ["Algebra I", "Biology", "English I", "English II",
                                                          "U.S. History"],
                                                         ["Approaches Grade Level", "Meets Grade Level",
                                                          "Masters Grade Level"])

    # --- TELPAS Results ---
    print("    Looking for TELPAS results...")
    performance_data['telpas'] = extract_section_data(text, "TELPAS Results",
                                                      ["Listening", "Speaking", "Reading", "Writing"],
                                                      ["Beginning", "Intermediate", "Advanced", "Advanced High"])

    # --- Assessments of Course Performance ---
    print("    Looking for Assessments of Course Performance results...")
    # performance_data['course_performance'] = extract_section_data(text, "Assessments of Course Performance",
    #                                                                  [],  # Add specific courses if needed
    #                                                                  ["Average Score", "Passing Rate"])

    # --- Demographic Data ---
    print("    Looking for demographic data...")
    # Example (adjust keywords based on your PDF format)
    performance_data['student_enrollment'] = extract_value(text, "Total Student Enrollment:", "")
    performance_data['economically_disadvantaged'] = extract_percentage(text, "Economically Disadvantaged:")
    # ... extract other demographic data points ...

    # --- Student Progression and Averages ---
    print("    Looking for student progression and averages...")
    # Example (adjust keywords based on your PDF format)
    performance_data['attendance_rate'] = extract_percentage(text, "Average Daily Attendance:")
    performance_data['graduation_rate'] = extract_percentage(text, "Four-Year Graduation Rate:")
    # ... extract other progression and average data points ...

    # --- District-Level Comparisons ---
    print("    Looking for district-level comparisons...")
    # Example (adjust keywords based on your PDF format)
    performance_data['district_reading_avg'] = extract_value(text, "District Average - Reading:", "")
    performance_data['district_math_avg'] = extract_value(text, "District Average - Math:", "")
    # ... extract other district comparison data points ...

    return performance_data


def extract_section_data(text, section_title, subjects, performance_levels):
    """Extracts data from a specific section in the PDF text.

    Args:
        text (str): The extracted text content of the PDF.
        section_title (str): The title of the section to extract data from.
        subjects (list): A list of subjects within the section.
        performance_levels (list): A list of performance levels to extract.

    Returns:
        dict: A dictionary containing the extracted data for the section.
    """

    section_data = {}
    start_index = text.lower().find(section_title.lower())
    if start_index != -1:
        section_text = text[start_index:]
        for subject in subjects:
            subject_data = {}
            for level in performance_levels:
                keyword = f"{subject} - {level}"
                subject_data[level.lower().replace(" ", "_")] = extract_percentage(section_text, keyword)
            section_data[subject.lower().replace(" ", "_")] = subject_data
    return section_data


def extract_value(text, keyword, unit=""):
    """Extracts a value after a keyword in the text."""
    start_index = text.find(keyword)
    if start_index != -1:
        value_start = start_index + len(keyword)
        value_end = text.find(unit, value_start) if unit else text.find("\n", value_start)
        if value_end != -1:
            value = text[value_start:value_end].strip()
            print(f"      Found: {keyword} {value}")
            return value
    return None


def extract_percentage(text, keyword):
    """Extracts a percentage value after a keyword in the text."""
    value = extract_value(text, keyword, "%")
    if value is not None:
        try:
            return float(value)  # Convert to a number if possible
        except ValueError:
            return value
    return None  # Return None if percentage not found

