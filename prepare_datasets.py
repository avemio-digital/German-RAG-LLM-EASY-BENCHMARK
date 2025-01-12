import csv
import glob
import re
import pandas as pd
import os

# Define file name lists
special_file_names = [
    "qa-with-timedifference_test.csv", 
    "qa-without-timedifference_test.csv", 
    "qa-with-multiple-references_test.csv",
    "relevant-context_test.csv",
    "extraction-recall_test.csv"
]

normal_file_names = [
    "classification-json_test.csv",
    "ocr-correction_test.csv",
    "reasoning_test.csv",
    "summarizations_test.csv"
]

# Regular expressions for extracting integers
qa_reference_pattern = r'\[(\d+)\]'
qa_time_difference_pattern = r'(\d+)\s*(?:Tage|Tag|Stunden|Stunde)'
extraction_recall_pattern = r'ID (\d+)'
relevant_context_pattern = r'im (\d+)\. Kontext-Abschnitt'

# Create directory for prepared normal files
os.makedirs('prepared', exist_ok=True)

# Process special files
for file_name in special_file_names:
    # Read the CSV file
    df = pd.read_csv(file_name, sep=';')

    # Initialize new columns
    df['References'] = df['Response'].apply(lambda x: re.findall(qa_reference_pattern, x))
    
    if 'qa-with-timedifference_test.csv' in file_name:
        df['Time-Differences'] = df['Response'].apply(lambda x: re.findall(qa_time_difference_pattern, x))
    elif 'relevant-context_test.csv' in file_name:
        df['References'] = df['Response'].apply(lambda x: re.findall(relevant_context_pattern, x))
    elif 'extraction-recall_test.csv' in file_name:
        df['References'] = df['Response'].apply(lambda x: re.findall(extraction_recall_pattern, x))

    # Save the modified DataFrame to a new CSV file
    new_file_name = os.path.join('prepared', f"prepared_{file_name}")
    df.to_csv(new_file_name, sep=';', index=False, encoding='utf-8')
    print(f"Saved {new_file_name}")

# Process normal files
for file_name in normal_file_names:
    # Read the CSV file
    df = pd.read_csv(file_name, sep=';')

    # Save the DataFrame to the prepared folder with a new name
    new_file_name = os.path.join('prepared', f"prepared_{file_name}")
    df.to_csv(new_file_name, sep=';', index=False, encoding='utf-8')
    print(f"Saved {new_file_name}")