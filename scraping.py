import requests
from bs4 import BeautifulSoup
import csv


def scrape_data(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize an empty list to store extracted data
        data_list = []

        # Find all exhibitor-info divs
        exhibitors = soup.find_all('div', class_='exhibitor-info')

        for exhibitor in exhibitors:
            # Extract the exhibitor name
            name = exhibitor.find('h3').text.strip()

            # Extract the URL
            exhibitor_url = exhibitor.find('a')['href']

            # Extract booth information (assuming the first <p> tag contains it)
            booth_info = exhibitor.find_all('p')[0].text.strip()

            # Extract type information (assuming the second <p> tag contains it)
            type_info = exhibitor.find_all('p')[1].text.strip()

            # Append extracted information to the data list
            data_list.append({
                'name': name,
                'url': exhibitor_url,
                'booth_info': booth_info,
                'type_info': type_info
            })

        return data_list
    else:
        print("Failed to retrieve the webpage")
        return []


def save_to_csv(data, filename):
    # Define CSV file headers
    headers = ['name', 'url', 'booth_info', 'type_info']

    # Open a CSV file for writing
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV DictWriter object
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the headers to the CSV file
        writer.writeheader()

        # Write the data to the CSV file
        for row in data:
            writer.writerow(row)


# Example usage
url = "https://vapexpo-france.com/en/exhibitors-and-brands-list/"  # Replace with the actual URL you want to scrape
data = scrape_data(url)

# Specify the filename for the CSV output
filename = "exhibitors_data.csv"

# Save the scraped data to a CSV file
save_to_csv(data, filename)

print(f"Data successfully saved to {filename}")
