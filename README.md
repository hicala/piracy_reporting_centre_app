# The 21st Century Piracy Phenomenon. Exploring Contemporary Sea Piracy

## Summary

In this study the main goal is to evaluate the concentrations of the modern piracy incidents around the world.
Modern-day pirates around the world share the legal designation of their historic brethren as “enemies of all mankind” because they disrupt and hinder the safe navigation of maritime vessels containing goods and people. 

Piracy is a global crime which impedes the free movement of ships containing people and goods, with its attendant economic ramifications. The perpetrators are usually heavily armed, with sophisticated weapons to enable them to hijack a vessel or vessels and redirect them to their desired location for the payment of an expected ransom.

I am using Beautiful Soup for this Python app. Beautiful Soup is a Python library for parsing data out of HTML and XML files (aka webpages). It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree. 

The major concept with Beautiful Soup is that it allows you to access elements of your page by following the CSS structures, such as grabbing all links, all headers, specific classes, or more. It is a powerful library. Once we grab elements, Python makes it easy to write the elements or relevant components of the elements into other files, such as a CSV, that can be stored in a database or opened in other software.

The data I used came from Live Piracy & Armed Robbery Report 2020. Reference: https://www.icc-ccs.org/index.php/piracy-reporting-centre/live-piracy-report

![Home Page](images/home.png)

## Main goal

+ To access all of the content from the source code of the webpage with Python
+ Parse and extract data.
+ Save the info in CSV file for further analysis.

## Methodology

1. Import Modules
2. Get the URL link
3. Navigate the URL Data Structure
4. Testing out data requests
5. Write data to a file in pseudo-code:
    + Open up a file to write in and append data. 
    + Write headers
    + Clear HTML tag and insert text in array
    + Clear \r \n \t to prepare string variable to clear Narrations: and insert text in array
    + Prepare string variables Date, Time, Position, Area and Country, replace characters to insert character | and insert text in array
    + Split to elements to array results for character | and Write to file items Date, Time, Position, Area and Country
    + When complete, close the file
6. The output file in CSV format.

## Data info extracted:

Date, Time, Position, Area and Country of Live Piracy & Armed Robbery Report 2020

![piracy reporting centre](images/piracy_reporting_centre.png)

If you don't have Beautiful Soup, install with 'conda install beautifulsoup' in terminal.

Python requires us to explicitly load the libraries that we want to use:


```python
# If you don't have Beautiful Soup, install with 'conda install beautifulsoup' in terminal
# Python requires us to explicitly load the libraries that we want to use:
import requests
import bs4
import re
```

Load a webpage into python so that we can parse it and manipulate it.


```python
# Load a webpage into python so that we can parse it and manipulate it.
URL = 'https://www.icc-ccs.org/index.php/piracy-reporting-centre/live-piracy-report'
```

Control of Connection. We just turned the website code into a Python object. 


```python
# Control of Connection
# We just turned the website code into a Python object. 
response = requests.get(URL)
soup = bs4.BeautifulSoup(response.text, "html.parser")
```

Find all the tags with class narrations


```python
# find all the tags with class narrations
data = soup.findAll(attrs={'class':['jos_fabrik_icc_ccs_piracymap2016___narrations']})
```

![Source Code HTML](images/code.png)

Open new file, make sure path to your data file is correct.

Later, I write headers


```python
f = open('piracy_reporting_centre.csv','w') # open new file, make sure path to your data file is correct
f.write("Date\tTime\tPosition\tArea\tCountry" + "\n") # write headers
```


```python
# Clear HTML tag and insert text in array
results = []                              # Inicializa arreglo results
for element in data:                      # Itera sobre el arreglo data
     TAG_RE = re.compile(r'<[^>]+>')      # Prepara patron para limpiar tag html de las cadenas str(element)
     text = TAG_RE.sub('', str(element))  # Aplica patron y limpia tag html de text
     results.append(text)                 # Insert text in array
```


```python
# Clear \r \n \t to prepare string variable to clear Narrations: and insert text in array
results_explode = []      # Inicializa arreglo results_explode
results_2 = []            # Inicializa arreglo results_2
for element in results:   # Itera sobre el arreglo results de la celda anterior
     item = ''            # Inicializa item
     item = str(element)  # Le asigna el valor de item a cada elemento del arreglo results
     item = item.replace('\r', '').replace('\n', '').replace('\t', '') # Reemplaza de item \r, \n, \t para limpiar cadena y poder trabajar mejor en ella
     if item != 'Narrations:':                 # Se utiliza para limpiar de la cadena la cadena Narrations:
          results_explode = item.split(".")    # Realiza explode por el . para quedarnos con los elementos de la primera linea donde estan Date, Time, Position, Area and Country y eliminar el parrafo que tiene a continuacion la linea 
          i = 0                                # Inicializa i
          for result in results_explode:       # Itera sobre el arreglo results_explode
                i = i + 1
                if i <= 5: results_2.append(result) # Guarda los elementos donde despues se pueden extraer Date, Time, Position, Area and Country 
```


```python
# Prepare string variables Date, Time, Position, Area and Country, replace characters to insert character | and insert text in array
i = 0                      # i
results = []               # Inicializa arreglo results
for element in results_2:  # Itera sobre el arreglo results_2
    i = i + 1
    if i == 1: 
        data1 = str(element)  # toma elemento data1 para conformar la fecha
    if i == 2: 
        data2 = str(data1) + '.' + str(element) # toma elemento data1 y concatena str(element) para conformar la fecha
    if i == 3: 
        date = data2 + '.' + str(element) # toma elemento date mas otras cadenas y concatena str(element) para conformar la fecha
    if i == 4: 
        position = str(element)    # toma elemento position mas otras cadenas
    if i == 5: 
        country = str(element)     # toma elemento country mas otras cadenas
        item = date.replace(': Posn : ', '|').replace(': Posn: ', '|').replace(': ', '|') + '.' + position.replace(' – ', '|') + '.' + country.replace('E, ', 'E|').replace('W, ', 'W|')
        item = item.replace('N – ', 'N|').replace('W, ', 'W|') # Realiza reeplazo de : Posn : por |, : Posn: por |, : por |,  –  por |, E, por E|, W, por W| para conformar una linea donde estan bien delimitados los elemento Date, Time, Position, Area and Country por el separador |  
        results.append(item)    # Adiciona la linea donde estan bien delimitados los elemento Date, Time, Position, Area and Country por el separador | al arreglo results
        i = 0                   # Pone  en 0 para poder tomar los sgtes 5 elementos del arreglos results_2 donde estan los elementos utiles a extraer
```


```python
# Split to elements to array results for character | and Write to file items Date, Time, Position, Area and Country
for element in results:
       item = element.split("|") # Realiza explode por el caracter | para quedarnos con los elementos Date, Time, Position, Area and Country
       i = 0
       for element1 in item:
            i = i + 1
            if i == 1: 
                date = str(element1)
                f.write(date + "\t") # fecha date and add tabulator
            if i == 2: 
                time = str(element1)
                f.write(time + "\t") # fecha time and add tabulator
            if i == 3: 
                position = str(element1)
                f.write(position + "\t") # fecha position and add tabulator
            if i == 4: 
                area = str(element1)
                f.write(area + "\t") # fecha area and add tabulator
            if i == 5: 
                country = str(element1)
                f.write(country + "\t\n") # fecha country and add tabulator                
```


```python
# Close file
f.close()
```

![cvs data](images/cvs.png)

## Conclusiones

We used Beautiful Soup as the main tool. The major concept with Beautiful Soup is that it allows you to access elements of your page by following the CSS structures, such as grabbing all links, all headers, specific classes, or more. It is a powerful library.

 Once we grab elements, Python makes it easy to write the elements or relevant components of the elements into other files, such as a CSV, that can be stored in a database or opened in other software.
