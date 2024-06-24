import requests
import json
import argparse, sys
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dotenv import load_dotenv
import uuid
from scraper import parseToJson, get_all_links
from db_handler import DBHandler

load_dotenv()

parser=argparse.ArgumentParser()

parser.add_argument("--org", type=str, required=True, help="Organisation for which the generator would run")
parser.add_argument("--input", type=str, required=True, help="Input for the generator")
parser.add_argument("--output", type=str, required=True, help="Output file for the generated data")

# Ensure Scrapy project is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../links_resolver'))

from links_resolver.spiders.example_spider import ExampleSpider

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
    # TODO:: add clean json logic
    outputTreks = []

    if org == "IH":
        treksList = data["pageProps"]["trekInfoToSearch"]
        print(f"Found {len(treksList)} treks")
        URL = os.getenv('IH_URL')

        for trekInfo in treksList:
            outputTreks.append({
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
    elif org == "TTH":
        treksList = data
        print(f"Found {len(treksList)} treks")
        URL = os.getenv('TTH_URL')
        for trekInfo in treksList:
            outputTreks.append({
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

    return outputTreks

def save_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ExampleSpider)
    process.start()

def main(org, input_path, output_path):
    print("Skipping File Download")
    print(f"Performing the operation for {org}")

    data = parse_json(input_path)
    print("JSON file parsed")

    cleaned_data = clean_data(org, data)
    print("Data cleaned")

    save_json(cleaned_data, output_path)
    print(f"Cleaned data saved to {output_path}")

    result = DBHandler.builk_upsert(cleaned_data, "title")
    print(result)

    # links_list = get_all_links("https://trekthehimalayas.com/interest/trekking")
    # print("Parsed links list")
    # print(links_list)

if __name__ == "__main__":
    args=parser.parse_args()

    main(args.org, args.input, args.output)

    # run_spider()