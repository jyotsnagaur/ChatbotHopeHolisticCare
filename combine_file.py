import json


class JSONCombiner:
    def __init__(self, output_file_path):
        # Initialize the JSONCombiner with the path to save the combined JSON file.
        self.output_file_path = output_file_path
        # Dictionary to hold the combined data from multiple JSON files.
        self.combined_data = {}

    def read_json_file(self, file_path, key_name):
        # Read a JSON file and add its contents to the combined dictionary under a specified key.
        try:
            with open(file_path, 'r') as file:
                self.combined_data[key_name] = json.load(file)
            print(f"Data from {file_path} added under '{key_name}'.")
        except Exception as e:
            # Print an error message if the file cannot be read.
            print(f"Error reading {file_path}: {e}")

    def save_combined_json(self):
        # Save the combined dictionary to a JSON file.
        try:
            with open(self.output_file_path, 'w') as file:
                json.dump(self.combined_data, file, indent=4)
            print(f"Combined data saved to: {self.output_file_path}")
        except Exception as e:
            # Print an error message if the file cannot be saved.
            print(f"Error saving combined JSON: {e}")


def combine_json_files(output_path, files_and_keys):
    # Function to create a combiner, read multiple JSON files, and save them into a single combined file.
    combiner = JSONCombiner(output_path)
    for file_path, key_name in files_and_keys:
        combiner.read_json_file(file_path, key_name)
    combiner.save_combined_json()
