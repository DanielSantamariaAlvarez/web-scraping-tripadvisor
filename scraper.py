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
url = 'https://www.tripadvisor.com/Hotels-g294074-Bogota-Hotels.html'

def scrap(base_url, header):
    # Initialize a list to store the hotel data
    hotel_data = []

    # Set the number of pages to scrape
    response = requests.get(base_url, headers=header)
    # Parse the HTML of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the number of pages
    num_pages = soup.find('span', class_='qrwtg').text
    num_pages = ceil(int(num_pages.split(' ')[0].replace(',', ''))/30)

    # Scrape the data for each page
    for page in range(num_pages+1):
        # Send an HTTP GET request to the website
        url = f'{base_url}-oa{page * 30}'
        response = requests.get(url, headers=header)

        # Parse the HTML of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the hotel elements on the page
        hotels = soup.find_all('div', class_='listing_title')

        # Store the data for each hotel
        for hotel in hotels:
            response2 = requests.get('https://www.tripadvisor.com'+hotel.find('a', class_='property_title')['href'], headers=header)
            link = 'https://www.tripadvisor.com'+hotel.find('a', class_='property_title')['href']
            hotel_id = link.split('-')[2].replace('d', '')
            soup2 = BeautifulSoup(response2.text, 'html.parser')
            try: name = soup2.find('h1', class_='QdLfr b d Pn').text
            except: name = None
            try: rating = soup2.find('span', class_='uwJeR P').text
            except: rating = None
            try: phone = soup2.find('span', class_='zNXea NXOxh NjUDn').text
            except: phone = None
            try: address = soup2.find('span', class_='fHvkI PTrfg').text
            except: address = None
            try:
                website = 'https://www.tripadvisor.com'
                links = soup2.find_all('a', attrs={'class': 'YnKZo Ci Wc _S C pInXB _S ITocq jNmfd'})
                for link in links:
                    website += link.get('href')
            except: website = None
            try: rating_quality = soup2.find('div', attrs={'class': 'kkzVG'}).text
            except: rating_quality = None
            try:
                price = int(soup2.find('div', attrs={'class': 'JPNOn b Wi'}).text.replace(',', '').split('\xa0')[1])
            except:
                try:
                    price = soup2.find_all('div', attrs={'class': 'WXMFC'})
                    avg_price = 0
                    for i in price:
                        temp = i.text
                        temp = temp.replace(',', '')
                        temp = temp.split('\xa0')
                        avg_price += int(temp[1])
                    price = int((avg_price/len(price)))

                except:
                    price = None
            time = datetime.now()

            # Append the data to the list
            hotel_data.append({'name': name, 'rating': rating, 'phone': phone, 'address': address, 'website': website, 'rating_quality': rating_quality, 'price': price, 'hotel_id': hotel_id, 'Timestamp': time})

    # Convert the list to a Pandas DataFrame
    df = pd.DataFrame(hotel_data)

    # Save the data to a CSV file
    df.to_csv('tripadvisor.csv', index=False)
    return df

if __name__ == '__main__':
    # Set the header to mimic a browser
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    }
    # Send an HTTP GET request to the website
    base_url = 'https://www.tripadvisor.com/Hotels-g294073-Colombia-Hotels.html#LEAF_GEO_LIST'


    scrap(base_url=url, header = header)


