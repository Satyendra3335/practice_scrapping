import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

user_input = input("Enter the date (YYYY-MM-DD): ")

try:
    selected_date = datetime.strptime(user_input, "%Y-%m-%d")
except ValueError:
    print(" Invalid date format. Please enter in YYYY-MM-DD format.")
    exit()

url = "https://en.wikipedia.org/wiki/Python_(programming_language)"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')  

    paragraphs = soup.find_all('p')
    data = []

    for para in paragraphs:
        text = para.get_text(strip=True)
        if text:
            data.append({
                'date': selected_date.strftime('%Y-%m-%d'),
                'paragraph': text
            })

    # Print the number of paragraphs collected
    print(f" Total paragraphs collected: {len(data)}")

    # Save to Excel
    df = pd.DataFrame(data)
    file_name = 'scraped_data.xlsx'
    df.to_excel(file_name, index=False)
    print(f" Data saved to {file_name}")



else:
    print(f" Failed to retrieve the page. Status code: {response.status_code}")
