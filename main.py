import csv
import cities
import scraper
import pandas as pd
from fastapi import FastAPI, Response

app = FastAPI()

@app.get('/')
def index():
  return 'Hello World'

@app.get("/scrape/{city_name}")
async def scrape(city_name):
  city = city_name
  data = await scrape_data_for_city(city)
  csv_data = await convert_to_csv(data, city)
  csv_data = open(f'{city}-hotels.csv', 'r').read()
  return Response(
    csv_data,
    headers={"Content-disposition": f"attachment; filename={city}.csv"}
  )

async def scrape_data_for_city(city):
  link = ''
  try:
    link = await open_file(city)
  except:
    cities.scrap()
    link =  open_file(city)
  # Scrape the data for the city
  print('link: ', link)
  ret = await scraper.scrap(base_url=link)
  return ret
 

async def convert_to_csv(data, city):
  # Convert the data to a CSV file
  df =  pd.DataFrame(data)
  file =  df.to_csv(f'{city}-hotels.csv', index=False)
  return file

def open_file(city):
  f = open("colombian_cities.csv")
  reader = csv.reader(f)
  for row in reader:
    if row[0] == city:
      return row[1]

if __name__ == '__main__':
  app.run()
