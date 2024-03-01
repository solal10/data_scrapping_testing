import requests
from bs4 import BeautifulSoup
import csv

def scrape_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        data_list = []
        thumbnails = soup.find_all('div', class_='thumbnail')
        for thumb in thumbnails:
            exhibitor_info = {}
            name_tag = thumb.find('h3', class_='acadp-no-margin')
            if name_tag:
                exhibitor_info['name'] = name_tag.text.strip()
                exhibitor_info['url'] = name_tag.find('a')['href']
            img_tag = thumb.find('img')
            if img_tag:
                exhibitor_info['image_url'] = img_tag['src']
            for li in thumb.find_all('li', class_='list-group-item'):
                text_primary = li.find('span', class_='text-primary').text.strip()
                text_secondary = li.find('span', class_='text-muted').text.strip()
                exhibitor_info[text_primary.lower()] = text_secondary
            a_tags = thumb.find_all('a', href=True)
            location_tag = next((a for a in a_tags if a.string and ('Estados Unidos' in a.string or 'U.S.A' in a.string)), None)
            if location_tag:
                exhibitor_info['location'] = location_tag.text.strip()
            data_list.append(exhibitor_info)
        return data_list
    else:
        print("Failed to retrieve the webpage")
        return []

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'url', 'image_url', 'actividad', 'stand', 'location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Example usage
url = ""
data = scrape_data(url)
filename = "exhibitors_data.csv"
save_to_csv(data, filename)

print(f"Data successfully saved to {filename}")
