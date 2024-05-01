import pandas as pd
import logging

# Set up basic logging configuration to help debug and track operations.0
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ExcelReader:
    def __init__(self, file_path, sheet_name):
        """Initialize the ExcelReader with the path and sheet name of the Excel file."""
        self.file_path = file_path
        self.sheet_name = sheet_name

    def read_excel(self):
        """Read an Excel file into a pandas DataFrame.

        This method attempts to read the specified sheet from an Excel file.
        If successful, it logs the success; if it fails, it logs the error and raises an exception.
        """
        try:
            df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            logging.info("Excel file read successfully.")
            print(df.head)
            return df
        except Exception as e:
            logging.error(f"Failed to read Excel file: {e}")
            raise


class JSONWriter:
    def __init__(self, data):
        """Initialize the JSONWriter with a pandas DataFrame."""
        self.data = data

    def to_json(self):
        """Convert the pandas DataFrame to a JSON string using a record orientation."""
        return self.data.to_json(orient='records', force_ascii=False)

    def save_json(self, output_path):
        """Save the JSON string to a file with UTF-8 encoding.

        This method attempts to convert the DataFrame to JSON and save it to a specified path.
        It logs the success of the operation or an error if the saving process fails.
        """
        try:
            json_data = self.to_json()
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(json_data)
            logging.info(f"JSON data saved to {output_path}")
        except Exception as e:
            logging.error(f"Failed to save JSON data: {e}")
            raise


def excel_to_json(excel_file_path, sheet_name, json_output_path):
    """Convert an Excel file to a JSON file.

    This function reads an Excel file using the ExcelReader class and writes the resulting DataFrame to a JSON file
    using the JSONWriter class.It logs the steps and any potential errors encountered during the reading and writing
    processes.
    """
    # Reading Excel file
    excel_reader = ExcelReader(excel_file_path, sheet_name)
    dataframe = excel_reader.read_excel()

    # Writing to JSON
    json_writer = JSONWriter(dataframe)
    json_writer.save_json(json_output_path)
