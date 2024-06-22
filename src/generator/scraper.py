import requests
from bs4 import BeautifulSoup
import json

def parseToJson(url, output_file):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {}
        data["url"] = url
        data["title"] = soup.title.string if soup.title else "No Title"
        data["content"] = soup.prettify()

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Data successfully saved to {output_file}")
    else:
        print(f"Failed to retrieve the URL: {url} (status code: {response.status_code})")
    