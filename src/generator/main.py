import requests
import json
import sys
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dotenv import load_dotenv
from scraper import parseToJson

load_dotenv()

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

def clean_data(data):
    # TODO:: add clean json logic
    treksList = data["pageProps"]["trekInfoToSearch"]
    print(f"Found {len(treksList)} treks")
    outputTreks = []
    URL = os.getenv('TARGET_URL')

    for trekInfo in treksList:
        outputTreks.append({
            "title": trekInfo["title"],
            "uuid": trekInfo["uid"],
            "url": URL + "/" + trekInfo["uid"]
        })

    return outputTreks

def save_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ExampleSpider)
    process.start()

def main(url, download_path, output_path):
    # downloaded_file = download_file(url, download_path)
    # print(f"File downloaded to {downloaded_file}")

    print("Skipping File Download")

    data = parse_json("input.json")
    print("JSON file parsed")

    cleaned_data = clean_data(data)
    print("Data cleaned")

    save_json(cleaned_data, output_path)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    url = "http://dog-api.kinduff.com/api/facts?number=5"
    download_path = "downloaded_file.json"
    output_path = "output.json"

    main(url, download_path, output_path)

    parseToJson("https://indiahikes.com/bhrigu-lake", "bhrigu.json")

    # run_spider()