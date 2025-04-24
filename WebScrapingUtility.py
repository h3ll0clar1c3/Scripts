import requests
from bs4 import BeautifulSoup
import csv
import json

# URL of the website to scrape
url = "https://example.com"  # Replace with the target URL

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send a GET request to the website
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Example: Extract data (e.g., titles and links)
    data = []
    for item in soup.find_all("a"):  # Replace "a" with the target HTML element
        title = item.text.strip()  # Extract text
        link = item.get("href")    # Extract link
        if title and link:
            data.append({"title": title, "link": link})

    # Save data to a JSON file
    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    # Save data to a CSV file
    with open("output.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "link"])
        writer.writeheader()
        writer.writerows(data)

    print("Data has been saved to 'output.json' and 'output.csv'")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
