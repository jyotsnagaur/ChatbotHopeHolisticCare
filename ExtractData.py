import PyPDF2
import os
import re
import json
from read_excel_file import ExcelReader, excel_to_json  # Import function to convert Excel files to JSON
from combine_file import combine_json_files  # Import function to combine JSON files


class PDFTextExtractor:
    def __init__(self, patterns_to_remove=None):
        """Initialize the PDFTextExtractor with optional regex patterns to remove unwanted text."""
        if patterns_to_remove is None:
            patterns_to_remove = [
                r'\nPage \d+ of \d+\n',  # Removes pagination text
                r'\n\d+\n'  # Removes lone numbers (often page numbers)
            ]
        self.patterns_to_remove = patterns_to_remove

    def clean_text(self, text):
        """Apply regex patterns to remove unwanted text from extracted PDF text."""
        for pattern in self.patterns_to_remove:
            text = re.sub(pattern, '\n', text)
        return text

    def extract_text_from_pdf(self, pdf_file_path):
        """Extract and clean text from a PDF file."""
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            extracted_text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                page_text_cleaned = self.clean_text(page_text)
                extracted_text += page_text_cleaned + "\n"
            return extracted_text

    def process_folder(self, folder_path, output_text_file_path, output_json_file_path):
        """Process all PDF files in a folder, extract text, and save it to a single output file. Additionally,
        convert text to JSON."""
        all_text = ""
        data_json = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                pdf_file_path = os.path.join(folder_path, filename)
                print(f"Extracting text from: {filename}")
                extracted_text = self.extract_text_from_pdf(pdf_file_path)
                all_text += extracted_text + "\n"
                # Convert extracted text to JSON (modify this based on your specific data structure)
                data_json.append({'filename': filename, 'content': extracted_text})

        # Save all extracted text to one text file
        with open(output_text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(all_text)
        print(f"Saved all extracted text to: {output_text_file_path}")

        # Save JSON data
        with open(output_json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data_json, json_file, indent=4)
        print(f"Saved JSON data to: {output_json_file_path}")


# Usage example within the script
if __name__ == '__main__':
    extractor = PDFTextExtractor()
    # Define the folder path - Where all PDF files are located
    folder_path = '/Users/abshasan/PycharmProjects/Go/HH Care/Home Care Staff 2023'

    # No Need to do anything here, file will be saved locally on the project folder
    output_text_file_path = 'pdf_file1.txt'
    output_json_file_path = 'pdf_file1.json'# Output path for the combined text from all PDFs
    extractor.process_folder(folder_path, output_text_file_path, output_json_file_path) # Read pdf file



    # Define the folder path - Where Excel file is located
    excel_file_path = '/Users/abshasan/PycharmProjects/Go/HH Care/Knack_S05_Incidents Complaints Feedback CI.xlsx'
    sheet_name = 'records_rows_per_page=1000'  # Name of the Excel sheet to process


    # No Need to do anything here, file will be saved locally on the project folder
    json_output_path = 'excel_data.json'  # Output path for the converted JSON
    excel_to_json(excel_file_path, sheet_name, json_output_path)

    files_to_combine = [
        ('pdf_file1.json', 'Policy'),
        ('excel_data.json', 'Incidents')
    ]
    combined_json_output_path = 'combined.json'
    combine_json_files(combined_json_output_path, files_to_combine)  # Combine specified JSON files into one
