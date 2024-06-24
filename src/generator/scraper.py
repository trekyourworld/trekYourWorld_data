import requests
from bs4 import BeautifulSoup
import re
import json

def parseToJson(url, output_file):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {}
        data["url"] = url
        data["title"] = soup.title.string if soup.title else "No Title"
        # Find the div with class matching "TrekInfoOverview_feeCardContainer*"
        divs = soup.find('div', class_='')

        data["divs"] = []

        available_dates = []
        for date_header in soup.find_all('p', class_=''):
            available_dates.append(date_header.text.strip())
        
        print(available_dates)
        print(divs)

        # for div in divs:
        #     # Extract relevant data from each div
        #     div_data = {
        #         'text': div.get_text(),
        #         'html': str(div)
        #     }
        #     data['divs'].append(div_data)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Data successfully saved to {output_file}")
    else:
        print(f"Failed to retrieve the URL: {url} (status code: {response.status_code})")
    
def get_all_links(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the content of the response with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all anchor tags
    links = soup.find_all('a')
    # Extract the href attribute from each anchor tag
    urls = [link.get('href') for link in links if link.get('href') is not None]
    return urls