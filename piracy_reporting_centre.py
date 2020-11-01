#!/usr/bin/env python
# coding: utf-8

# In[98]:


# If you don't have Beautiful Soup, install with 'conda install beautifulsoup' in terminal
# Python requires us to explicitly load the libraries that we want to use:
import requests
import bs4
import re


# In[99]:


# Load a webpage into python so that we can parse it and manipulate it.
URL = 'https://www.icc-ccs.org/index.php/piracy-reporting-centre/live-piracy-report'


# In[100]:


# Control of Connection
# We just turned the website code into a Python object. 
response = requests.get(URL)
soup = bs4.BeautifulSoup(response.text, "html.parser")


# In[101]:


# find all the tags with class city or number
data = soup.findAll(attrs={'class':['jos_fabrik_icc_ccs_piracymap2016___narrations']})


# In[102]:


f = open('piracy_reporting_centre.csv','w') # open new file, make sure path to your data file is correct
f.write("Date\tTime\tPosition\tArea\tCountry" + "\n") # write headers


# In[103]:


# Clear HTML tag and insert text in array
results = []                              # Inicializa arreglo results
for element in data:                      # Itera sobre el arreglo data
     TAG_RE = re.compile(r'<[^>]+>')      # Prepara patron para limpiar tag html de las cadenas str(element)
     text = TAG_RE.sub('', str(element))  # Aplica patron y limpia tag html de text
     results.append(text)                 # Insert text in array


# In[104]:


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


# In[105]:


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


# In[106]:


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


# In[107]:


# Close file
f.close() # close file


# In[ ]:




