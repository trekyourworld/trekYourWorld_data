import requests
import json
import argparse, sys
import os
from dotenv import load_dotenv
import uuid
from db_handler import DBHandler

load_dotenv()

parser=argparse.ArgumentParser()

parser.add_argument("--org", type=str, required=True, help="Organisation for which the generator would run")
parser.add_argument("--input", type=str, required=True, help="Input for the generator")
parser.add_argument("--output", type=str, required=True, help="Output file for the generated data")

# Ensure Scrapy project is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../links_resolver'))

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def parse_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def clean_data(org, data):
    outputTreks = {}

    if org == "IH":
        treksList = data["pageProps"]["trekInfoToSearch"]
        print(f"Found {len(treksList)} treks")
        URL = os.getenv('IH_URL')
        IH_KEY = os.getenv('IH_KEY')
        generatedTreks = []
        for trekInfo in treksList:
            generatedTreks.append({
                "uuid": str(uuid.uuid4()),
                "title": trekInfo["title"],
                "uid": trekInfo["uid"],
                "url": URL + "/" + trekInfo["uid"],
                "elevation": "",
                "duration": "",
                "cost": "",
                "difficulty": "",
                "location": "",
                "bestTimeToTarget": "",
                "tags": []
            })
        outputTreks["org"] = IH_KEY
        outputTreks["treks"] = generatedTreks
    elif org == "TTH":
        treksList = data
        print(f"Found {len(treksList)} treks")
        URL = os.getenv('TTH_URL')
        TTH_KEY = os.getenv('TTH_KEY')
        generatedTreks = []
        for trekInfo in treksList:
            generatedTreks.append({
                "uuid": str(uuid.uuid4()),
                "title": trekInfo["title"],
                "uid": trekInfo["uid"],
                "url": URL + "/" + trekInfo["uid"],
                "elevation": "",
                "duration": "",
                "cost": "",
                "difficulty": "",
                "location": "",
                "bestTimeToTarget": "",
                "tags": []
            })
        outputTreks["org"] = TTH_KEY
        outputTreks["treks"] = generatedTreks

    return outputTreks

def save_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main(org, input_path, output_path):
    print("Skipping File Download")
    print(f"Performing the operation for {org}")

    orgs_list = org.split(",")
    input_path_list = input_path.split(",")

    if len(orgs_list) is not len(input_path_list):
        print("Please enter correct input")
        print(f"Orgs: {orgs_list} should be equivalent to input paths provided: {input_path_list}")
        exit(1)
    
    complied_output = []
    for i in range(len(orgs_list)):
        parsed_data = parse_json(input_path_list[i])
        cleaned_data = clean_data(orgs_list[i], parsed_data)
        complied_output.append(cleaned_data)

    save_json(complied_output, output_path)
    print(f"Cleaned data saved to {output_path}")

    # db_handler = DBHandler(complied_output)
    # db_handler.insert_data()
    # print(result)

    # links_list = get_all_links("https://trekthehimalayas.com/interest/trekking")
    # print("Parsed links list")
    # print(links_list)

if __name__ == "__main__":
    args=parser.parse_args()

    main(args.org, args.input, args.output)