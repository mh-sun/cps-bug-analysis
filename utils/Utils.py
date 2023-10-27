import pandas as pd
import json


def json_to_xml(inputLocation, outputLocation):
    # Load JSON data from a local file
    with open(inputLocation, 'r') as file:
        json_data = json.load(file)
    # Create a DataFrame from JSON data
    df = pd.DataFrame(json_data)
    print(df)
    # Write DataFrame to Excel
    df.to_excel(outputLocation, index=False)
    print('Excel file created successfully!')


def xlsx_to_json(inputLocation, outputLocation):
    df = pd.read_excel(inputLocation, engine="openpyxl")
    df.to_json(outputLocation, orient="records")

    print(f"Data from {inputLocation} has been converted and saved to {outputLocation} in JSON format.")


def merge_json_files(file1_path, file2_path, output_file_path):
    with open(file1_path, 'r', encoding='utf-8') as file:
        json_data1 = json.load(file)

    with open(file2_path, 'r', encoding='utf-8') as file:
        json_data2 = json.load(file)

    merged_data = json_data1.copy()

    for project in json_data2:
        duplicate_found = False
        for existing_project in merged_data:
            if (existing_project["project_name"] == project["project_name"] and
                    existing_project["source_link"] == project["source_link"]):
                duplicate_found = True
                break

        if not duplicate_found:
            merged_data.append(project)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, ensure_ascii=False, indent=4)

    print(f"Data merged and saved to {output_file_path}")
