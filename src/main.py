import json
import argparse, sys
import os
from dotenv import load_dotenv
import uuid
from db_handler import DBHandler

load_dotenv()

parser=argparse.ArgumentParser()

parser.add_argument("--output", type=str, required=True, help="Output file for the generated data")

# Ensure Scrapy project is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../links_resolver'))

def parse_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def clean_data(data):
    outputTreks = {}
    treksData = data
    
    print(f"Found {len(treksData["list"])} treks")
    URL = treksData["meta"]["baseURL"]
    KEY = treksData["meta"]["key"]
    generatedTreks = []
    for trekInfo in treksData["list"]:
        generatedTreks.append({
            "uuid": str(uuid.uuid4()),
            "title": trekInfo["title"],
            "uid": trekInfo["uid"],
            "url": URL + "/" + trekInfo["uid"],
            "elevation": trekInfo["elevation"],
            "duration": trekInfo["duration"],
            "cost": trekInfo["cost"],
            "difficulty": trekInfo["difficulty"],
            "location": trekInfo["location"],
            "distance": trekInfo["distance"],
            "bestTimeToTarget": "",
            "tags": []
        })
    outputTreks["org"] = KEY
    outputTreks["treks"] = generatedTreks
    return outputTreks

def save_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_all_data_files(base_path):
    file_paths = []
    for root, _, files in os.walk(base_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def main(output_path):
    print("Skipping File Download")
    input_path_list = get_all_data_files("./data")

    complied_output = []
    for i in range(len(input_path_list)):
        parsed_data = parse_json(input_path_list[i])
        cleaned_data = clean_data(parsed_data)
        complied_output.append(cleaned_data)

    save_json(complied_output, output_path)

    db_handler = DBHandler(complied_output)
    db_handler.update_data()

if __name__ == "__main__":
    args=parser.parse_args()

    main(args.output)