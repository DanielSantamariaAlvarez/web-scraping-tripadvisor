import requests
from bs4 import BeautifulSoup
from math import ceil
from datetime import datetime
import pandas as pd

# Set the header to mimic a browser
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
}
# Send an HTTP GET request to the website
base_url = 'https://www.tripadvisor.com/Hotels-g294073-Colombia-Hotels.html#LEAF_GEO_LIST'

# Get the cities from the home page
def get_cities_home(soup, colombia_cities):
    cities = soup.find_all('div', class_='geo_wrap')
    for city in cities:
        link = 'https://www.tripadvisor.com'+city.a['href']
        name = city.a.text
        name = list(name)
        name = name[:-7]
        name = ''.join(name)
        colombia_cities.append({'name': name, 'link': link})

# Get the cities from the other pages
def get_cities(soup, colombia_cities):
    cities = soup.find_all('a', class_='city')
    for city in cities:
        name = list(city.find('span', class_='name').text.split('(')[0])
        name = name[:-7]
        name = ''.join(name)
        link = 'https://www.tripadvisor.com'+city.get('href')
        city_data = {'name': name, 'link': link}
        colombia_cities.append(city_data)

# Scrape the data for each page
def scrap(header=header, base_url= base_url):
    # Initialize a list to store the hotel data
    colombia_cities = []

    # Set the number of pages to scrape
    response = requests.get(base_url, headers=header)
    # Parse the HTML of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the number of pages
    num_pages = soup.find('span', class_='qrwtg').text
    num_pages = ceil(int(num_pages.split(' ')[0].replace(',', ''))/30)
    centinel = True

    # Scrape the data for each page
    for page in range(num_pages+1):
        # Send an HTTP GET request to the website
        url = f'{base_url}-oa{page * 30}'
        response = requests.get(url, headers=header)

        # Parse the HTML of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        if centinel:
            get_cities_home(soup, colombia_cities)
            centinel = False
        else:
            get_cities(soup, colombia_cities)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(colombia_cities)
    df.to_csv('colombia_cities.csv', index=False)

if __name__ == '__main__':
    # Set the header to mimic a browser
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    }
    # Send an HTTP GET request to the website
    base_url = 'https://www.tripadvisor.com/Hotels-g294073-Colombia-Hotels.html#LEAF_GEO_LIST'

    # Initialize a list to store the hotel data
    scrap(header, base_url)

