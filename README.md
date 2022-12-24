# Prueba técnica de Daniel Santamaría Para aplicar a Iceberg Data

## Archivos:
- app.py
- cities.py
- scraper.py
- tripadvisor.csv

## Explicación de cada archivo:
### app.py
Aplicación hecha en flask para poder obtener la lista de los hoteles de la ciudad que se ingrese por parámetro.

Para correr la aplicación utilice: flask run

En el endpoint que se maneja es de tipo GET y retorna el archivo csv con los hoteles de la ciudad que se escogió por parámetro. 

### cities.py
Este archivo .py genera un documento csv con todas las ciudades que se encuentran en TripAdvisor con su nombre y su respectivo link para poder encontrar en un paso posterior los hoteles de dicha ciudad.
Genera un csv ya que es mejor que na primera ves haga todos los request y se almacenes en un archivo para poder generar consultas más rápidas.

### scraper.py
Se encarga de encontrar los hoteles de la ciudad que se decee buscar. Si no se le pasa una ciudad por parámetro esta busca por defecto los hoteles en la ciudad de bogotá.
Correr la aplicación: python3 scraper.py

### tripadvisor.csv
Archivo de ejemplo generado con scraper.py para los hoteles de la ciudad de Bogotá.