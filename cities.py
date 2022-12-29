import requests
from bs4 import BeautifulSoup
from math import ceil
from datetime import datetime
import pandas as pd

# Set the header to mimic a browser
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
}

# Get the cities from the page 
def get_cities(soup, colombia_cities, num):
    if num == 0:
        cities = soup.find_all('div', class_='geo_wrap')
    else:
        cities = soup.find_all('a', class_='city')
        
    for city in cities:
        if num == 0:
            link = 'https://www.tripadvisor.com'+city.a['href']
            name = city.a.text
        else:
            link = 'https://www.tripadvisor.com'+city.get('href')
            name = city.find('span', class_='name').text.split('(')[0]
        name = list(name)
        name = name[:-7]
        name = ''.join(name).lower()
        city_data = {'name': name, 'link': link}
        colombia_cities.append(city_data)

# Scrape the data for each page
def scrap(header=header):

    # Initialize a list to store the hotel data
    colombia_cities = []
    # Number of pages to scrape
    num_pages = 24  ## corregido el numero de paginas

    # Scrape the data for each page
    for page in range(num_pages):
        # Send an HTTP GET request to the website
        url = f'https://www.tripadvisor.com/Hotels-g294073-oa{page*20}-Colombia-Hotels.html#LEAF_GEO_LIST' # 20 is the number of hotels per page
        response = requests.get(url, headers=header)

        # Parse the HTML of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        get_cities(soup, colombia_cities, page)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(colombia_cities)
    df.to_csv('colombian_cities.csv', index=False)

if __name__ == '__main__':
    # Set the header to mimic a browser
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    }

    # Initialize a list to store the hotel data
    scrap(header)

