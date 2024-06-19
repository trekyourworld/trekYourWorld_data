import requests
import json

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
    return data

def save_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main(url, download_path, output_path):
    download_file = download_file(url, download_path)
    print(f"File downloaded to {download_file}")

    data = parse_json(download_file)
    print("JSON file parsed")

    cleaned_data = clean_data(data)
    print("Data cleaned")

    save_json(cleaned_data, output_path)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    url = ""
    download_path = "downloaded_file.json"
    output_path = "cleaned_data.json"

    main(url, download_path, output_path)