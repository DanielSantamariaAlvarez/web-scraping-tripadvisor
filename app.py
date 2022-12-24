from flask import Flask, request, Response
import csv
import cities
import scraper
import pandas as pd

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
  city = request.args.get('city')
  data = scrape_data_for_city(city)
  csv_data = convert_to_csv(data, city)

  return Response(
    csv_data,
    mimetype="text/csv",
    headers={"Content-disposition": "attachment; filename=data.csv"}
  )

def scrape_data_for_city(city):
  link = ''
  try:
    link = open_file(city)
  except:
    cities.scrap()
    link = open_file(city)
  # Scrape the data for the city
  return scraper.scrap(base_url=link)
  

def convert_to_csv(data, city):
  # Convert the data to a CSV file
  df = pd.DataFrame(data)
  df.to_csv(f'{city}-hotels.csv', index=False)

def open_file(city):
  f = open("cities.csv")
  reader = csv.reader(f)
  for row in reader:
    if row[0] == city:
      return row[1]

if __name__ == '__main__':
  app.run()
