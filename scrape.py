import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Get user input for date
user_input = input("Enter the date (YYYY-MM-DD): ")

# Validate date format
try:
    selected_date = datetime.strptime(user_input, "%Y-%m-%d")
except ValueError:
    print(" Invalid date format. Please enter in YYYY-MM-DD format.")
    exit()

# Format date to DD/MM/YYYY as required by the form
formatted_date = selected_date.strftime("%d/%m/%Y")

# Use HTTP (not HTTPS)
url = "http://phhc.gov.in/home.php?search_param=free_text_search_judgment"

# Form data for POST request
payload = {
    "dt1": formatted_date,  # From Date
    "dt2": formatted_date,  # To Date
    "search": "Search"
}

# Headers
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Make POST request
response = requests.post(url, headers=headers, data=payload)

# Check response
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find rows in the result table
    rows = soup.select("table tr")[1:]  # Skip header
    data = []

    for row in rows:
        cols = [col.get_text(strip=True) for col in row.find_all("td")]
        if cols:
            data.append({
                "date": user_input,
                "case_info": " | ".join(cols)
            })

    print(f"Total cases found: {len(data)}")

    if data:
        df = pd.DataFrame(data)
        file_name = "scraped_data.xlsx"
        df.to_excel(file_name, index=False)
        print(f"Data saved to {file_name}")
        for item in data:
            print(f"{item['date']}: {item['case_info']}")
    else:
        print(" No cases found for the selected date.")

else:
    print(f" Failed to retrieve the page. Status code: {response.status_code}")
