import csv
import glob
import re
import pandas as pd
import os

# Define file name lists
special_file_names = [
    "evaluated_qa-with-timedifference_test.csv", 
    "evaluated_qa-without-timedifference_test.csv", 
    "evaluated_qa-with-multiple-references_test.csv",
    "evaluated_relevant-context_test.csv",
    "evaluated_extraction-recall_test.csv"
]

normal_file_names = [
    "evaluated_classification-json_test.csv",
    "evaluated_ocr-correction_test.csv",
    "evaluated_reasoning_test.csv",
    "evaluated_summarizations_test.csv"
]

# Regular expressions for extracting integers
qa_reference_pattern = r'\[(\d+)\]'
qa_time_difference_pattern = r'(\d+)\s*(?:Tage|Tag|Stunden|Stunde)'
extraction_recall_pattern = r'ID (\d+)'
relevant_context_pattern = r'im (\d+)\. Kontext-Abschnitt'

# Create directory for prepared normal files
os.makedirs('extracted', exist_ok=True)

# Process special files
for file_name in special_file_names:
    # Read the CSV file
    df = pd.read_csv(file_name, sep=';')

    # Initialize new columns
    df['model_References'] = df['model_generated_output'].apply(lambda x: re.findall(qa_reference_pattern, x))
    
    if 'qa-with-timedifference_test.csv' in file_name:
        df['model_Time-Differences'] = df['model_generated_output'].apply(lambda x: re.findall(qa_time_difference_pattern, x))
    elif 'relevant-context_test.csv' in file_name:
        df['model_References'] = df['model_generated_output'].apply(lambda x: re.findall(relevant_context_pattern, x))
    elif 'extraction-recall_test.csv' in file_name:
        df['model_References'] = df['model_generated_output'].apply(lambda x: re.findall(extraction_recall_pattern, x))

    # Save the modified DataFrame to a new CSV file
    new_file_name = os.path.join('extracted', f"extracted_{file_name}")
    df.to_csv(new_file_name, sep=';', index=False, encoding='utf-8')
    print(f"Saved {new_file_name}")

# Process normal files
for file_name in normal_file_names:
    # Read the CSV file
    df = pd.read_csv(file_name, sep=';')

    # Save the DataFrame to the prepared folder with a new name
    new_file_name = os.path.join('extracted', f"extracted_{file_name}")
    df.to_csv(new_file_name, sep=';', index=False, encoding='utf-8')
    print(f"Saved {new_file_name}")