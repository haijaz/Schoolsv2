import camelot

def extract_student_performance_data(pdf_file_path):
  """
  Extracts student performance data from a PDF file using Camelot.

  Args:
      pdf_file_path: The path to the PDF file.

  Returns:
      A list of pandas DataFrames containing the extracted tables.
  """

  # Extract tables from the PDF
  tables = camelot.read_pdf(pdf_file_path, flavor='stream', pages='all')

  # Filter tables based on relevant keywords in the first row (header)
  relevant_tables = [table.df 
                     for table in tables 
                     if any(keyword in table.df.iloc[0].astype(str).tolist() 
                            for keyword in ["STAAR", "TELPAS", "ACP", "SAT", "PSAT", "AP"])
                    ]

  return relevant_tables

# Example usage
file_path = 'downloads/DP1.pdf'  # Replace with your PDF file path
extracted_tables = extract_student_performance_data(file_path)

# Display or process the extracted tables
for table in extracted_tables:
  print(table)
  # Further processing or analysis can be done here