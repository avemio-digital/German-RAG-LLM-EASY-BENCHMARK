import json
import huggingface_hub
from datasets import load_dataset

HF_TOKEN = "hf_[...]"
hf_repo = "avemio/GRAG-LLM-EASY-BENCHMARK"
config_names = [
    'reasoning', 
    'classification-json', 
    'extraction-recall', 
    'qa-without-timedifference', 
    'qa-with-timedifference', 
    'qa-with-multiple-references', 
    'questions', 
    'relevant-context', 
    'summarizations', 
    'ocr-correction'
]

# Authenticate with Hugging Face Hub
huggingface_hub.login(HF_TOKEN)

# Iterate over all configurations
for config_name in config_names:
    # Load the dataset with the specified configuration
    dataset = load_dataset(hf_repo, config_name)
    
    # Iterate over all splits
    for split_name in dataset:
        split = dataset[split_name]
        # Check if the split is a test split
        if 'test' in split_name:
            # Check if the required columns are present
            if all(col in split.column_names for col in ["System", "Instruction", "Response"]):
                # Save the split as a CSV file
                csv_filename = f"{config_name}_{split_name}.csv"
                split.to_csv(csv_filename, sep=';', index=False, encoding='utf-8')
                print(f"Saved {csv_filename}")