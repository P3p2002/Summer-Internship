# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 12:59:48 2023

@author: pep

Si teniu dubtes sobre el codi escriviu a l'autor del codi en el correu peprubi@gmail.com
"""


import urllib.request
from datetime import datetime, date, timedelta
from astral.sun import sun
from astral import LocationInfo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from urllib.error import HTTPError
import scienceplots
plt.style.use(["science","no-latex"])


# # *****************************************************************************

#                                 FUNCTIONS
# # *****************************************************************************

#Aquesta funcio m'obra els links, provant primer el mes avitual i despres el que alguns cops es fa sevrir
#Ja que alguns messos escampats va canviant( sense un patro aparent)
def open_link_with_condition(year, month):
    month=int(month)
    year=int(year)
    # Define a list of URLs to try
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_name = month_list[int(month)-1]
    urls = [ f'http://www.obsebre.es/php/geomagnetisme/dhorta/{year}/{month_name}/ebr{year}{month:02d}dhor.hor', 
            f'http://www.obsebre.es/php/geomagnetisme/dhorta/{year}/' +
    f'{month_name}/ebr'+'20'+f'{year}dhor.hor'
        # Add more URLs here if needed
    ]

    # hdr required to access the files
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    for url in urls:
        try:
            req = urllib.request.Request(url, headers=hdr)
            response = urllib.request.urlopen(req)

            # Check if the response status code is 200 (OK) before processing data
            if response.status == 200:
                data = response.read().decode('utf-8')
                # Process the data from the response here
                print("Data retrieved successfully:")
                file = urllib.request.urlopen(req)
                return file
                break  # Break the loop if a valid response is obtained

        except HTTPError as http_err:
            if http_err.code == 404:
                print(f"The link was not found for URL: {url}")
            else:
                print(f"HTTP error occurred for URL: {url}, Error: {http_err}")
        except urllib.error.URLError as url_err:
            print(f"URL error occurred for URL: {url}, Error: {url_err}")

    else:
        # The loop completed without a successful response from any URL
        print("Failed to retrieve data from all URLs.")

# *****************************************************************************

def read_file(d, m, y):
    print('>>>>>>>>>>>>>> El bucle de llegir el dia', d, m, y, 'ha comencat <<<<<<<<<<<<<<')
    day = d
    month = m
    year = y
    route = f'C:/Users/pep/OneDrive - UAB/Escritorio/Variacio de D/Dades anys antics/{year}/ebr{year}{month}dhor.hor'
    if float(year) > 2011:
        file_type = 'new'
        if (year == '2019' or year == '2018' or year == '2017' or year == '2016' or  year == '2014' or year == '2013'):
            data = pd.read_csv(route, skiprows=24, delimiter='\\s+')
        elif year=='2015' and (float(month)==6):
            data = pd.read_csv(route, skiprows=32, delimiter='\\s+')
        elif year == '2015' and (float(month)!=6):
            data = pd.read_csv(route, skiprows=24, delimiter='\\s+')
        elif year == '2012':
            data = pd.read_csv(route, skiprows=26, delimiter='\\s+')

        elif (year == '2020' or year == '2022'):
            data = pd.read_csv(route, skiprows=25, delimiter='\\s+')
            
        elif (year == '2021' and (float(month) >= 9 and float(month)<11)):
            data = pd.read_csv(route, skiprows=24, delimiter='\\s+')
            
        elif (year=='2021' and (float(month) <9 or float(month)>11)):
            data = pd.read_csv(route, skiprows=25, delimiter='\\s+')
            
        elif (year=='2021' and  float(month)==11):
            data = pd.read_csv(route, skiprows=25, delimiter='\\s+')
    elif float(year) > 2022:
        file_type = 'current'
    elif 1980 <= float(year) < 2000:
        file_type = 'old'
        if float(year) < 1995:
            data = pd.read_csv(route, skiprows = 24, delimiter='\\s+')
        elif float(year) >= 1995:
            data = pd.read_csv(route, skiprows = 26, delimiter='\\s+')
    else:
        file_type = 'old'
        if float(year) == 2000 and float(month) <= 4:
            data = pd.read_csv(route, skiprows=12, delimiter='\\s+', skip_blank_lines=True)            
        elif ((float(year) == 2000 and float(month) >= 4) or float(year) > 2000) :
            data = pd.read_csv(route, skiprows=12, delimiter='\\s+', skip_blank_lines=True)        
    #print(f'\n>>>>>>>>>>>>>> {day}-{month}-{year} <<<<<<<<<<<<<<')
    print('>>>>>>>>>>>>>> El bucle de llegir el dia', d, m, y, 'ha acabat <<<<<<<<<<<<<<')
    print('\n')
    print('\n')

    return data, file_type, day
"""
#L'unic que fa aquesta funcio es llegir les dades
def read_file(d, m, y):
    print('>>>>>>>>>>>>>> El bucle de llegir el dia', d, m, y, 'ha comencat <<<<<<<<<<<<<<')
    day = d
    month = m
    year = y
    if float(year) >= 2000:
        file = open_link_with_condition(year, month)
    
        if float(year) > 2011:
            file_type = 'new'
            if (year == '2019' or year == '2018' or year == '2017' or year == '2016' or  year == '2014' or year == '2013'):
                data = pd.read_csv(file, skiprows=24, delimiter='\\s+')
            elif year=='2015' and (float(month)==6):
                data = pd.read_csv(file, skiprows=32, delimiter='\\s+')
            elif year == '2015' and (float(month)!=6):
                data = pd.read_csv(file, skiprows=24, delimiter='\\s+')
            elif year == '2012':
                data = pd.read_csv(file, skiprows=26, delimiter='\\s+')
    
            elif (year == '2020' or year == '2022'):
                data = pd.read_csv(file, skiprows=25, delimiter='\\s+')
                
            elif (year == '2021' and (float(month) >= 9 and float(month)<11)):
                data = pd.read_csv(file, skiprows=24, delimiter='\\s+')
                
            elif (year=='2021' and (float(month) <9 or float(month) >= 11)):
                data = pd.read_csv(file, skiprows=25, delimiter='\\s+')
                
            elif (year=='2021' and  float(month)==11):
                data = pd.read_csv(file, skiprows=25, delimiter='\\s+')
        elif float(year) > 2022:
            file_type = 'current'
        else:
            file_type = 'old'
            data = pd.read_csv(file, skiprows=12, delimiter='\\s+')
    elif 1980 <= float(year) < 2000:
        route = f'C:/Users/pep/OneDrive - UAB/Escritorio/Variacio de D/Dades anys antics/{year}/ebr{year}{month}dhor.hor'
        if float(year) < 1995:
            data = pd.read_csv(route, skiprows = 24, delimiter='\\s+')
        elif float(year) >= 1995:
            data = pd.read_csv(route, skiprows = 26, delimiter='\\s+')
        file_type = 'old'
    #print(f'\n>>>>>>>>>>>>>> {day}-{month}-{year} <<<<<<<<<<<<<<')
    print('>>>>>>>>>>>>>> El bucle de llegir el dia', d, m, y, 'ha acabat <<<<<<<<<<<<<<')
    print('\n')
    print('\n')
    return data, file_type, day
    """
# *****************************************************************************

#Aquesta funcio esta creada perque totes les llistes tinguin
#les mateixes dades
#Ja que segons quina epoca es llegeixi, les dades que dona 
#l'observatori son unes o unes altres
def data_treatment(data, file_type):
    if file_type == 'new' or file_type == 'current':
        data['EBRD'] = np.rad2deg(np.arctan(data['EBRY']/data['EBRX']))*60
        return data
    elif file_type == 'old':
        EBRx = [] 
        EBRy = []
        for i in range(len(data['EBRD'])):
            EBRx.append(np.cos(data['EBRD'][i]*2*math.pi/360)*data['EBRH'][i])
            EBRy.append(np.sin(data['EBRD'][i]*2*math.pi/360)*data['EBRH'][i])
        EBRx = pd.DataFrame(np.transpose(EBRx))
        EBRy = pd.DataFrame(np.transpose(EBRy))
        headers = ['DATE', 'TIME', 'EBRD', 'EBRX', 'EBRY']
        dades = pd.DataFrame({})
        dades = pd.concat([data['DATE'], data['TIME'], data['EBRD'], EBRx, EBRy], axis=1)
        dades.columns = headers
        return dades

# *****************************************************************************

#Aquesta funcio nomes em retorna les hores, i tot i que no  es 
#necessaria la del migdia
#S'ha deixat ja que la tinc implementada en tot el codi i vull 
#evitar els possibles errors que surgeixin per treure-la
def notable_times2(y, m, d):
    latitude, longitude = 40.820817, 0.495186
    city = LocationInfo("EBR", "Catalunya", "Europe", latitude, longitude)
    date = datetime.strptime(str(y) + '-'+ str(m) + '-' + str(d), '%Y-%m-%d')

    s = sun(city.observer, date=datetime.date(date))

    if s['sunrise'].minute >= 30:
        sunrise_index = (s['sunrise'].hour)+1
    elif s['sunrise'].minute < 30:
        sunrise_index = (s['sunrise'].hour)
    noon_index = (s['noon'].hour)
    if s['sunset'].minute >= 30:
        sunset_index = (s['sunset'].hour)+1
    elif s['sunset'].minute < 30:
        sunset_index = (s['sunset'].hour)
 

    t_indexes = [sunrise_index, noon_index, sunset_index]

    return t_indexes

# *****************************************************************************

#Aquesta funcio em retorna l'hora de la sortida i posta de 
#sol aixi com els minuts
#Mes endavant ja es veura perque es necessaria
def notable_minutes(y, m, d ):
    latitude, longitude = 40.820817, 0.495186
    city = LocationInfo("EBR", "Catalunya", "Europe", latitude, longitude)
    date = datetime.strptime(str(y) + '-'+ str(m) + '-' + str(d), '%Y-%m-%d')

    s = sun(city.observer, date=datetime.date(date))

    sunrise = s['sunrise'].minute
    sunset = s['sunset'].minute
    
    if s['sunrise'].minute >= 30:
        sunrise_h = (s['sunrise'].hour)+1
    elif s['sunrise'].minute < 30:
        sunrise_h = (s['sunrise'].hour)
    if s['sunset'].minute >= 30:
        sunset_h = (s['sunset'].hour)+1
    elif s['sunset'].minute < 30:
        sunset_h = (s['sunset'].hour)
    t_indexes = [sunrise, sunrise_h, sunset, sunset_h]

    return t_indexes

# *****************************************************************************

#Aquesta funcio serveix per filtrar les dades, primer segons el 
#dia i despres segons la hora
#Tot i que es una mica ineficient es el que em semblava mes facil
# per no provocar possibles
#errors alhora de seleccionar els indexos
def filter_data(raw_data, file_type, day, a, b, secular):
    
    i_start, i_end = ((int(day)-1)*24), ((int(day))*24)#Primer torno els dies
    filtered_data = pd.DataFrame({})
    filtered_data = [raw_data['DATE'][i_start:i_end+1],
                     raw_data['TIME'][i_start:i_end+1],
                     raw_data['EBRD'][i_start:i_end+1],
                     raw_data['EBRX'][i_start:i_end+1],
                     raw_data['EBRY'][i_start:i_end+1]]

    headers = ['DATE', 'TIME', 'EBRD', 'EBRX', 'EBRY']
    data = pd.concat(filtered_data, axis=1, keys=headers)
    data = data.reset_index()
    data['HOURS'] = data.index
    contador_random = tercer_filtre(data, file_type)
    if contador_random == 1:
        return data,i_start, contador_random
    
    dades_00 = data['EBRD'][0] - secular
    dades_23 = data['EBRD'][23] - secular
    
    coefficients = regressio_magnetosfera(dades_00, dades_23)
    model = np.poly1d(coefficients)
    for j in range(len(data['EBRD'])):
        data['EBRD'][j] -= (model(j)+secular)
    i_start_2, i_end_2 = a,b#Ara torno les hores
    filtered_data_2 = pd.DataFrame({})
    filtered_data_2 = [data['DATE'][i_start_2:i_end_2+1],
                      data['TIME'][i_start_2:i_end_2+1],
                      data['EBRD'][i_start_2:i_end_2+1],
                      data['EBRX'][i_start_2:i_end_2+1],
                      data['EBRY'][i_start_2:i_end_2+1]]

    headers = ['DATE', 'TIME', 'EBRD', 'EBRX', 'EBRY']
    data_2 = pd.concat(filtered_data_2, axis=1, keys=headers)
    data_2 = data_2.reset_index()
    data_2['HOURS'] = data_2.index
    return data_2, i_start, contador_random

# *****************************************************************************

#Aquesta funcio serveix per filtrar les dades nomes segons el dia
def filter_data_2(raw_data, file_type, day, secular):
    
    i_start, i_end = ((int(day)-1)*24), ((int(day))*24)
    filtered_data = pd.DataFrame({})
    filtered_data = [raw_data['DATE'][i_start:i_end+1],
                     raw_data['TIME'][i_start:i_end+1],
                     raw_data['EBRD'][i_start:i_end+1],
                     raw_data['EBRX'][i_start:i_end+1],
                     raw_data['EBRY'][i_start:i_end+1]]

    headers = ['DATE', 'TIME', 'EBRD', 'EBRX', 'EBRY']
    data = pd.concat(filtered_data, axis=1, keys=headers)
    data = data.reset_index()
    data['HOURS'] = data.index
    
    dades_00 = data['EBRD'][0] - secular
    dades_23 = data['EBRD'][23] - secular
    
    coefficients = regressio_magnetosfera(dades_00, dades_23)
    model = np.poly1d(coefficients)
    for j in range(len(data['EBRD'])):
        data['EBRD'][j] -= (model(j)+secular)

    return data

# *****************************************************************************

#Segon filtre serveix per si hi ha alguna dada malament, pero no surt un numero molt gran
#Per aixo es comprova la pendent i s'estableix un limit de 5 cops major a l'anterior
#Cal notar que el 5 es arbitrari pero s'ha fet amb la consciencia que solucionava algun problema
def segon_filtre(dades, dades_anterior):
    Slope_actual = []
    Slope_anterior = []
    contador_pendent = 0
    for j in range(len(dades['EBRD'])-1):
        #Faig aixo ja que se que estic agafant dades cada hora i per tant x_i-x_i+1=1
        slope = (dades['EBRD'][j]-dades['EBRD'][j+1])
        Slope_actual.append(slope)
    for j in range(len(dades_anterior['EBRD'])-1):
        slope_anterior = (dades_anterior['EBRD'][j]-dades_anterior['EBRD'][j+1])
        Slope_anterior.append(slope_anterior)
        
    #Imposo que el pendent del dia actual sigui similar al del dia 
    #anterior bo amb un rang,amb un range de 5 cops l'anterior
    if max(Slope_actual) > 5*max(Slope_anterior):
        contador_pendent = 1
    return contador_pendent

# *****************************************************************************

#Aixo es basicament un filtre per comprovar que les dades siguin 
#bones o no
#ja que pot haver dies on les dades siguin grans ja que hi ha hagut
#algun problema
#I aquell dia no s'han pogut agafar o algo
def tercer_filtre(data, file_type):
    contador_random=0
    if file_type=='current' or file_type=='new':
    #Diferencio si es nou o no ja que en l'OBS de l'Ebre 
    #posen notacio diferent segons
    #L'any que estiguem mirant i per tant es important 
    #fer aquesta diferenciacio
        for i in range(len(data['EBRX'])):
            if ((data['EBRX'][i]) >= 99999.00 and (data['EBRY'][i]) <= 99999.00) :
            #Miro que sigui major a aquest valor ja que es el que hi ha 
            #A la pagina web pels valors no acceptables
                data=data.drop([i], axis = 0)
                contador_random += 1
                break
            elif ((data['EBRX'][i]) <= 99999.00 and (data['EBRY'][i]) >= 99999.00):
                contador_random += 1
                data=data.drop([i], axis = 0)
                break
            elif ((data['EBRX'][i]) >= 99999.00 and (data['EBRY'][i]) >= 99999.00) and i%60!=0:
                contador_random += 1
                data=data.drop([i], axis = 0)
                break
    elif file_type=='old':
        for i in range(len(data['EBRD'])):
            if (data['EBRD'][i]) >= 90000.00:
                print('Dades massa grans')
                data=data.drop([i], axis = 0)
                contador_random += 1
                print(contador_random)
                break
    return contador_random

# *****************************************************************************

#Aquesta funcio simplement retorna el dia de l'any
#(doy, per 'day of the year')
#( en numeros natural, sent l'1 de gener l'1) 
#que em servira per despres
#Principalment la utilitat d'aquesta funcio sera alhora de fer 
#llistes per tenir en compte que el dia X es el numero Y 
#de la llista
def dia_any(d,m,y):
    #Comenco diferenciant si l'any es o no de traspas
    if ((int(y) % 4 == 0 and int(y) % 100 != 0) or (int(y) % 100 == 0 and int(y) % 400 == 0)):
        day_of_year = date(int(y), int(m), int(d)).timetuple().tm_yday
    else:
        if int(m)>2:#Si no ho es( de traspas) miro que el mes sigui major o menor a 2
            day_of_year = date(int(y), int(m), int(d)).timetuple().tm_yday+1
        else:#Quan hagi passat Febrer li haure d'afegir un 1 al doy per comptar que m'he saltat el 29/2
            day_of_year = date(int(y), int(m), int(d)).timetuple().tm_yday
    return day_of_year
# *****************************************************************************

def day_to_date(day_number):
    date_format = '%Y-%m-%d'
    # create a datetime object for January 1st of the given year
    start_date = datetime(2000 , 1, 1)
    #Poso l'any 2000 perque tinc les dades ordenades com si fosin 
    #anys de traspas
    # add the number of days to the start date
    result_date = start_date + timedelta(days=day_number)
    # format the date string using the specified format
    return result_date.day, result_date.month

# *****************************************************************************

#Funcio per omplir els dies buits
def empty_days(Mitja_dies):
    Dies_buits = []
    for i in range(366):
        #En aquesta primera part simplement mirare quins dies estan buits i els ficare en una llista per comoditat
        Llista_dies = []
        Llista_dies_anteriors = []
        cond_1 = all(Mitja_dies[i][k] == 0 for k in range(24))#Imposo primer la condicio que el dia que estic mirant estigui buit
        if cond_1 == True:
            print('El dia buit es:', [day_to_date(i)] )
            Llista_dies.append([Mitja_dies[i],i])
            Dies_buits.append([day_to_date(i)])
            j = i+1#El +1 es important per no comptar dos cops el mateix dia
            if j >= 366:#Aquesta condicio s'imposa per si ens trobem amb l'ultim dia de l'any
                j = 0
            numero_dies_superior = 0
            while True:
                cond_1_2 = all(Mitja_dies[j][k] == 0 for k in range(24))#Imposo la condicio de que el seguent dia de l'any tambe estigui buit
                #I vaig guardant els dies de l'any buits
                if cond_1_2 == True:
                    numero_dies_superior += 1
                    Llista_dies.append([Mitja_dies[j],j])
                    Dies_buits.append([day_to_date(j)])
                    print('Un altre dia buit seguit:', [day_to_date(j)])
                    j += 1
                    if j >= 366:#S'imposa pel mateix motiu que s'ha imposat a dalt
                        j = 0
                else:#Quan el seguent dia esta ple l'afegeixo a la llista i surto del while
                    Llista_dies.append([Mitja_dies[j],j])
                    break
            l=i-1
            if l <= -1:#Aquesta condicio s'imposa per si es dona el cas del primer dia de l'any
                l = 365
            numero_dies_inferior = 0
            #Repeteixo el mateix procediment pero disminuint els dies. Cal notar que aquesta condicio no s'hauria d'activar si no es que s'esta treballant amb el primer dia de l'any ja que en principi ja agafo el primer dia buit
            while True:
                cond_1_3 = all(Mitja_dies[l][k] == 0 for k in range(24))
                if cond_1_3 == True:
                    numero_dies_superior += 1
                    Llista_dies_anteriors.append([Mitja_dies[l],l])
                    Dies_buits.append([day_to_date(l)])
                    l -= 1
                    if l <= -1:#S'imposa pel mateix motiu que s'ha imposat la de dalt
                        l = 365
                else:
                    Llista_dies_anteriors.append([Mitja_dies[l],l])
                    break
            Llista_dies_anteriors2 = []
            for m in range(len(Llista_dies_anteriors)):
                Llista_dies_anteriors2.append(Llista_dies_anteriors[len(Llista_dies_anteriors)-1-m])
            Llista_dies_total = Llista_dies_anteriors2 + Llista_dies
            numero_d_buit = len(Llista_dies_total)-2
            #La idea que he seguit aqui ha estat omplir els dies que hi havia buits amb els dos mes propers que hi havia plens
            #per aixo s'ha separat el proces en dues parts depenen de si el numero de dies buits era parell o no, i es sumara
            #per omplir el dia buit es tindran en compte diferents pesos dels dies ja plens mes propers segons quin es trobi mes proper
            
            dia_1 = day_to_date(Llista_dies_total[0][1])
            times_1 = notable_times2(2000, dia_1[1], dia_1[0])
            dia_2 = day_to_date(Llista_dies_total[-1][1])
            times_2 = notable_times2(2000, dia_2[1], dia_2[0])
            if times_1[0] >times_2[0]:
                hora_inici = times_2[0]
            elif times_1[0] <= times_2[0]:
                hora_inici = times_1[0]
                
            if times_1[2] > times_2[2]:
                hora_final = times_1[2]
            elif times_1[2] <= times_2[2]:
                hora_final = times_2[2]
                
            if numero_d_buit%2 == 0:#Cas amb els dies buits parells
                for m in range(int(numero_d_buit/2)):
                    frac = (numero_d_buit-(1+m))/(numero_d_buit)#Aqui em declaro la fraccio que sera el meu pes alhora de fer els calculs
                    #La idea d'aquesta fraccio es dividir l'interval buit en fragments que estiguin pessats depenent de com de separats estan dels dies plens
                    #Anem a veure un exemple: si tenim els dies a, b, c, d, e, f on NOMES a i f estan plens, els dies s'ompliran de la seguent forma:
                    #c i d com estan en el centre tindran (a+f)/2 per altre banda b sera a*3/4+f*1/4 i e sera f*3/4+a*1/4
                    #La idea d'aquest fragment es fer aixo per qualsevol numero de dies buits 
                    for n in range(len(Llista_dies_total[int(numero_d_buit/2)][0])):
                        Llista_dies_total[1+m][0][n] = frac*Llista_dies_total[0][0][n]+Llista_dies_total[numero_d_buit+1][0][n]*(1-frac)
                        Llista_dies_total[numero_d_buit-m][0][n] = Llista_dies_total[0][0][n]*(1-frac)+Llista_dies_total[numero_d_buit+1][0][n]*frac
                    #Estic imposant condicions per evitar problemes en els canvis d'hora, ja que es possible tenir entre mig d'un buit dies que tinguin hores diferents
                    if Llista_dies_total[0][0][hora_inici] != 0 and Llista_dies_total[-1][0][hora_inici] == 0:
                        Llista_dies_total[1+m][0][hora_inici] = Llista_dies_total[0][0][hora_inici]
                        Llista_dies_total[numero_d_buit-m][0][hora_inici] = Llista_dies_total[0][0][hora_inici]
                    elif Llista_dies_total[0][0][hora_inici] == 0 and Llista_dies_total[-1][0][hora_inici] != 0:
                        Llista_dies_total[1+m][0][hora_inici] = Llista_dies_total[-1][0][hora_inici]
                        Llista_dies_total[numero_d_buit-m][0][hora_inici] = Llista_dies_total[-1][0][hora_inici]
                    if Llista_dies_total[0][0][hora_final] != 0 and Llista_dies_total[-1][0][hora_final] == 0:
                        Llista_dies_total[1+m][0][hora_final] = Llista_dies_total[0][0][hora_final]
                        Llista_dies_total[numero_d_buit-m][0][hora_final] = Llista_dies_total[0][0][hora_final]
                    elif Llista_dies_total[0][0][hora_final] == 0 and Llista_dies_total[-1][0][hora_final] != 0:
                        Llista_dies_total[1+m][0][hora_final] = Llista_dies_total[-1][0][hora_final]
                        Llista_dies_total[numero_d_buit-m][0][hora_final] = Llista_dies_total[-1][0][hora_final]

            else:#Aqui es segueix el mateix procediment per un numero de dies buits senar
                for n in range(len(Llista_dies_total[int(np.ceil(numero_d_buit/2))][0])):
                    #Aqui s'omple el dia del mig(cal notar que ara nomes hi ha un mentres que abans hi havia dos)
                    Llista_dies_total[int(np.ceil(numero_d_buit/2))][0][n] = (Llista_dies_total[0][0][n]+Llista_dies_total[numero_d_buit+1][0][n])/2
                for m in range(int(numero_d_buit/2)):
                    frac = (numero_d_buit-(1+m))/(numero_d_buit)
                    for n in range(len(Llista_dies_total[0][0])):
                        Llista_dies_total[1+m][0][n] = frac*Llista_dies_total[0][0][n]+Llista_dies_total[numero_d_buit+1][0][n]*(1-frac)
                        Llista_dies_total[numero_d_buit-m][0][n] = Llista_dies_total[0][0][n]*(1-frac)+Llista_dies_total[numero_d_buit+1][0][n]*frac
                        
                    #Estic imposant condicions per evitar problemes en els canvis d'hora
                    if Llista_dies_total[0][0][hora_inici] != 0 and Llista_dies_total[-1][0][hora_inici] == 0:
                        Llista_dies_total[1+m][0][hora_inici] = Llista_dies_total[0][0][hora_inici]
                        Llista_dies_total[numero_d_buit-m][0][hora_inici] = Llista_dies_total[0][0][hora_inici]
                    elif Llista_dies_total[0][0][hora_inici] == 0 and Llista_dies_total[-1][0][hora_inici] != 0:
                        Llista_dies_total[1+m][0][hora_inici] = Llista_dies_total[-1][0][hora_inici]
                        Llista_dies_total[numero_d_buit-m][0][hora_inici] = Llista_dies_total[-1][0][hora_inici]
                    if Llista_dies_total[0][0][hora_final] != 0 and Llista_dies_total[-1][0][hora_final] == 0:
                        Llista_dies_total[1+m][0][hora_final] = Llista_dies_total[0][0][hora_final]
                        Llista_dies_total[numero_d_buit-m][0][hora_final] = Llista_dies_total[0][0][hora_final]
                    elif Llista_dies_total[0][0][hora_final] == 0 and Llista_dies_total[-1][0][hora_final] != 0:
                        Llista_dies_total[1+m][0][hora_final] = Llista_dies_total[-1][0][hora_final]
                        Llista_dies_total[numero_d_buit-m][0][hora_final] = Llista_dies_total[-1][0][hora_final]
                        
            for h in range(int(np.ceil(numero_d_buit/2))):
                index = Llista_dies_total[h+1][1]
                for g in range(24):
                    Mitja_dies[index][g] = Llista_dies_total[h+1][0][g]
    return Mitja_dies, Dies_buits
# *****************************************************************************

def fun(x, A, w, phi): 
    return A*np.sin(w*x+phi)

#Funcio per fer ajustar dies
def funct_curvefit_dies(Mitja_dies, Dies_buits, Dies_mal_min):
    def fun(x, A, w, phi): 
        return A*np.sin(w*x+phi)
    Limits_mitja_dies = np.zeros((366,2))#Aquesta donal'interval on la mitja no es nula per tal de que es puguin plotejar be les grafiques, el primer elements es el maxim i el segon el minim
    Max_min_Md = np.zeros((366,2))#Aquesta llista dona els maxims i minims per tal de que es puguin plotejar be les grafiques, el primer elements es el maxim i el segon el minim
    hores = []
    llegenda = ['Fit', 'Data', 'Difference']
    for j in range(24):
        hores.append(str(j)+':'+'30')
    As = []
    Freqs = []
    Phis = []
    Curve_fit = np.zeros((367,24))
    for i in range(24):
        Curve_fit[366][i] = i
    for i in range(366):
        llista_dies = []
        Md_no_nuls = []
        for j in range(len(Mitja_dies[0])):
            if Mitja_dies[i][j] != 0:
                llista_dies.append(j)
                Md_no_nuls.append(Mitja_dies[i][j])
        dia, mes = day_to_date(i)
        for j in Dies_mal_min:
            if int(j[0]) == dia and int(j[1]) == mes:
                sunrise = j[-2]
                sunset = j[-1]
                break
            else:
                times = notable_minutes(2000, mes, dia)
                sunrise = times[1]
                sunset = times [3]
                #No importa l'any que utilitzi ja que els casos que donen problemes no els tinc en compte aqui
        #El primer maxim i minim es amb el qual plotejare
        max_1 = int(sunset)
        min_1 = int(sunrise)
        #Els segons maxims i minims son els que utilitzare per donar un bon guess de l'amplitud per fer el curve fit
        max_2 = max(Md_no_nuls)
        min_2 = min(Md_no_nuls)
        for j in range(len(Dies_buits)):
            if int(dia) ==int(Dies_buits[j][0][0]) and int(mes) == int(Dies_buits[j][0][1]):
                dia_omplert = 'Y'
                break
            else:
                dia_omplert = 'N'
        print('<<<<<<<' + 'Dia' + str(dia) + '\t ,mes' + str(mes) + '>>>>>>>\n')#Aqui he de posar el dia i el mes que estic fent
        Amplitud=(max_2-min_2)/2
        #Estic imposant les condicions que m'interesen, que son que en els extrems trobi un valor de 0,
        #Per fer aixo he imposat que w*t_1+phi = 0 i w*t_2+phi = 2*pi, on t_1 es la primera hora amb sol, i t_2 la ultima
        #Per com treballo es important que per calcular la fase i la freq no tingui en compte que la hora es les 7:30( per exemple)
        #Ja que aixo fara que el grafic no quedi exactament en el 0
        freq = 2*math.pi/(max_1-min_1)
        fase = -2*math.pi*min_1/(max_1-min_1)
        #Fico el +1 en el max_1 per tal de que m'arribi on vull, ja que el for es queda un per sota del maxim
        As.append(Amplitud)
        Freqs.append(freq)
        Phis.append(fase)
        Curve_fit[i][min_1:max_1+1]=fun(Mitja_dies[366][min_1:max_1+1],Amplitud, freq, fase)
        dif = []
        for j in range(len(Curve_fit[i])):
            dif.append(-Curve_fit[i][j]+Mitja_dies[i][j])
        plt.plot(hores[min_1:max_1+1],Curve_fit[i][min_1:max_1+1], color = 'r')
        plt.plot(hores[min_1:max_1+1], Mitja_dies[i][min_1:max_1+1])
        plt.plot(hores[min_1:max_1+1], dif[min_1:max_1+1], color = 'g')
        plt.yticks(fontsize = 15)
        plt.xticks(rotation=45, fontsize = 15)       
        plt.xlabel('Time(Hours)', fontsize = 17)
        plt.ylabel('D(min)', fontsize = 17)
        if dia_omplert == 'Y':
            plt.title('Mean of D(t) of ' + 'Dia' + str(dia)+',mes' + str(mes) + 'Aquest dia ha estat creat', fontsize = 15 )
        else:
            plt.title('Mean of D(t) of ' + 'Dia' + str(dia)+ ',mes' + str(mes), fontsize = 15 )
        plt.legend(llegenda, fontsize = 12)
        plt.rcParams['xtick.major.size'] = 10
        plt.rcParams['ytick.major.size'] = 10
        plt.rcParams['xtick.minor.size'] = 7
        plt.rcParams['ytick.minor.size'] = 7
        plt.rcParams['xtick.top'] = False
        plt.rcParams['ytick.right'] = False
        plt.rcParams["figure.figsize"] = (7,7)
        plt.show()
    return Curve_fit, As, Freqs, Phis

# *****************************************************************************
# *****************************************************************************

def Classificacio_dies(Dades1):
    #Comenco llegint els dies que son bons depenent de l'index i mels guardo
    Dies_bons=[]
    n=0
    Dades_bones=0
    Dades_totals=0
    Dades_dolentes=0
    while n<len(Dades1[0]):
        Dades=Dades1[:,n:n+8]
        estat_dada='neutre'
        for i in Dades[3]:
            if i!='0+' and i!='0-' and i!='0o' and i!='1+' and i!='1-' and i!='1o' and i!=-1:
                Dades_dolentes+=1
                print('Dd', Dades_dolentes)
                estat_dada='Dada dolenta'
                Dades_totals+=1
                print('Dt', Dades_totals)
            elif i=='0+' or i=='0-' or i=='0o' or i=='1+' or i=='1-' or i=='1o'  or i==-1:
                if estat_dada=='neutre' or estat_dada=='bona':
                    estat_dada='bona'
        if estat_dada=='bona':
            Dies_bons.append(Dades[0][0])
            Dades_bones+=1
            Dades_totals+=1
            print('Dt', Dades_totals)
        n+=8#Vaig augmentat de 8 en 8 per avancar tot el dia, ja que cada dia nomes s'agafen 8 mesures
    Dies_Bons_2=[]#Canvio el format a un que em sigui mes util
    for i in Dies_bons:
        if i.day<10 and i.month<10:
            Dies_Bons_2.append([str(0)+str(i.day),str(0)+str(i.month), str(i.year)]) 
        elif i.day<10 and i.month>=10:
            Dies_Bons_2.append([str(0)+str(i.day),str(i.month), str(i.year)]) 
        elif i.day>=10 and i.month<10:
            Dies_Bons_2.append([str(i.day),str(0)+str(i.month), str(i.year)]) 
        elif i.day>=10 and i.month>=10:
            Dies_Bons_2.append([str(i.day),str(i.month), str(i.year)])
    return Dies_Bons_2
# *****************************************************************************
#Funcio que mira quins dies tenen dades dolentes i em torna els dies bons
#En aquesta funcio s'ajunten diversos filtres que he creat en altres funcions, ja que es una de les funcions 'mare' d'aquest codi
def Llistat_dades_dies(Dies_Bons_2, Dades2, Coeficients, Anys):
    
    dies_concrets = input('Do you want to look at some day?(y/n) ')
    if dies_concrets == 'y':
        LLista_dia_con = []
        day = input('Which day do you want to look at?').zfill(2)
        month = input('Of Which month?').zfill(2)
    shape = (366, 24)  # (dimension 0, dimension 1)
    
    # Generar la matriz tridimensional vacia
    Mitja_dies_l = [[[] for _ in range(shape[1])] for _ in range(shape[0])]
    Mitja_dies_l.append([])
    for i in range(24):
        Mitja_dies_l[366].append(i)
    
    Dies_bons_filtrats = []
    dies_dolents = 0
    i = 0
    Dies_pendent_gran = []
    Secular = []
    #Llegeixo les dades i vaig guardant les dades comprovant les diverses condicions que ja s'ha imposat
    #Com la del pendent o la que les dades siguin bones
    while True:
        if i == 0:
            
            in_coef, dif_dies = index_coef(int(Dies_Bons_2[i][2]), int(Dies_Bons_2[i][1]), int(Dies_Bons_2[i][0]), Anys)
            model = np.poly1d(Coeficients[in_coef])
            secular = model(dif_dies)
            Secular.append(secular)
            
            dades, file_type, day  = read_file(Dies_Bons_2[i][0], Dies_Bons_2[i][1], Dies_Bons_2[i][2])
            day = Dies_Bons_2[i][0]
            times = notable_times2(Dies_Bons_2[i][2], Dies_Bons_2[i][1], Dies_Bons_2[i][0])
            dades = data_treatment(dades,file_type)
            dades,start_time, contador_random = filter_data(dades, file_type,day, times[0], times[2], secular)
            if contador_random > 0 and i != (len(Dies_Bons_2)-1):
                dies_dolents += 1
                print('El bucle ha acabat')
                print(i, len(Dies_Bons_2))
                Dies_Bons_2.pop(i)
                continue
            elif contador_random>0 and i == (len(Dies_Bons_2)-1):
                print('El bucle ha acabat')
                print(i, len(Dies_Bons_2))
                Dies_Bons_2.pop(i)
                dies_dolents += 1
                break
            #Aquesta part pot ser una bona idea comentarla si no s'esta segur de quins dies son dolents ja que el que fa es mirar els dies que son dolents i no els te en compte
            #Pero cal aclarir que els dies dolents s'han vist de forma manual ja que es veien un grafics dolents pero en principi els dies eren calmats
            contador_dd = eliminador_dies(Dies_Bons_2[i][0], Dies_Bons_2[i][1], Dies_Bons_2[i][2])
            if contador_dd > 0 and i != (len(Dies_Bons_2)-1):
                print(i, len(Dies_Bons_2))
                Dies_Bons_2.pop(i)
                dies_dolents += 1
                print('Dia dolent')
                continue
            elif contador_dd > 0 and i == (len(Dies_Bons_2)-1):
                print('El bucle ha acabat')
                print(i, len(Dies_Bons_2))
                Dies_Bons_2.pop(i)
                dies_dolents += 1
                print('pendent massa gran')
                break
            
            dades_anterior=dades
            Dies_bons_filtrats.append([Dies_Bons_2[i][0], Dies_Bons_2[i][1], Dies_Bons_2[i][2]])
            
            for j in range(len(dades)):
                index_dia = dia_any(Dies_Bons_2[i][0], Dies_Bons_2[i][1], Dies_Bons_2[i][2])-1#Per tenir en compte que la llista comenca en el 0 li resto 1
                index_hora = dades['index'][j]
                (Mitja_dies_l[index_dia][index_hora]).append(dades['EBRD'][j])
                if i == (len(Dies_Bons_2)-1):
                    print('El bucle ha acabat')
                    break
            if dies_concrets == 'y' and (day == Dies_Bons_2[i][0] and month == Dies_Bons_2[i][1]):
                LLista_dia_con.append([Dies_Bons_2[i][0], Dies_Bons_2[i][1], Dies_Bons_2[i][2]])
            i += 1
        if i >= 1:
            
            in_coef, dif_dies = index_coef(int(Dies_Bons_2[i][2]), int(Dies_Bons_2[i][1]), int(Dies_Bons_2[i][0]), Anys)
            model = np.poly1d(Coeficients[in_coef])
            secular = model(dif_dies)
            
            dades, file_type, day = read_file(Dies_Bons_2[i][0], Dies_Bons_2[i][1], Dies_Bons_2[i][2])
            day=Dies_Bons_2[i][0]
            dades = data_treatment(dades,file_type)
            times = notable_times2(Dies_Bons_2[i][2], Dies_Bons_2[i][1], Dies_Bons_2[i][0])
            dades,start_time, contador_random = filter_data(dades, file_type, day, times[0], times[2], secular)
            if contador_random > 0  and i != (len(Dies_Bons_2)-1):
                dies_dolents += 1
                print(i,len(Dies_Bons_2))
                Dies_Bons_2.pop(i)
                continue
            elif contador_random > 0 and i == (len(Dies_Bons_2)-1):
                print('El bucle ha acabat')
                print(i, len(Dies_Bons_2))
                Dies_Bons_2.pop(i)
                dies_dolents+=1
                break
                    
            #Segon filtre, serveix per si hi ha alguna dada malament, pero no surt un numero molt gran
            contador_pendent = segon_filtre(dades, dades_anterior)
            if contador_pendent > 0 and i != (len(Dies_Bons_2)-1):
                print(i, len(Dies_Bons_2))
                Dies_pendent_gran.append(Dies_Bons_2[i])
                Dies_Bons_2.pop(i)
                dies_dolents += 1
                print('pendent massa gran')
                continue
            elif contador_pendent > 0 and i == (len(Dies_Bons_2)-1):
                print('El bucle ha acabat')
                print(i, len(Dies_Bons_2))
                Dies_pendent_gran.append(Dies_Bons_2[i])
                Dies_Bons_2.pop(i)
                dies_dolents += 1
                print('pendent massa gran')
                break
            #Aquesta part pot ser una bona idea comentarla si no s'esta segur de quins dies son dolents ja que el que fa es mirar els dies que son dolents i no els te en compte
            #Pero cal aclarir que els dies dolents s'han vist de forma manual ja que es veien un grafics dolents pero en principi els dies eren calmats
            contador_dd = eliminador_dies(Dies_Bons_2[i][0], Dies_Bons_2[i][1], Dies_Bons_2[i][2])
            if contador_dd > 0 and i != (len(Dies_Bons_2)-1):
                print(i, len(Dies_Bons_2))
                Dies_Bons_2.pop(i)
                dies_dolents += 1
                print('Dia dolent')
                continue
            elif contador_dd > 0 and i == (len(Dies_Bons_2)-1):
                print('El bucle ha acabat')
                print(i, len(Dies_Bons_2))
                Dies_Bons_2.pop(i)
                dies_dolents += 1
                print('pendent massa gran')
                break
    
            dades_anterior = dades
            Dies_bons_filtrats.append([Dies_Bons_2[i][0], Dies_Bons_2[i][1], Dies_Bons_2[i][2]])
            for j in range(len(dades)):
                index_dia = dia_any(Dies_Bons_2[i][0], Dies_Bons_2[i][1], Dies_Bons_2[i][2])-1#Per tenir en compte que la llista comenca en el 0 li resto 1
                index_hora = dades['index'][j]
                (Mitja_dies_l[index_dia][index_hora]).append(dades['EBRD'][j])
            Secular.append(secular)
            if dies_concrets == 'y' :
                if day == Dies_Bons_2[i][0] and month == Dies_Bons_2[i][1]:
                    LLista_dia_con.append([Dies_Bons_2[i][0], Dies_Bons_2[i][1], Dies_Bons_2[i][2]])
            i += 1
        if dies_concrets == 'y':
            print(LLista_dia_con)
        print(i, len(Dies_Bons_2)-1)
        if i == (len(Dies_Bons_2)):#L'hi he tret el -1 ja que crec que em pot donar problemes per l'ultim dia
            print('El bucle ha acabat')
            break
    return Mitja_dies_l, Dies_bons_filtrats, Secular, Dies_pendent_gran
# *****************************************************************************
#Funcio que em comprova que tots els dies tinguin el mateix numero de dades
#En cas de que tots els dies no tinguin el mateix numero de dades em retorna els dies 
#Que donen problemes
def comprovacio_num_dies(Mitja_dies_l, Dies_bons_filtrats):
    Dies_dolents = []
    numero_dies = np.zeros((367,24))
    for i in range(366):
        for j in range(24):
            numero_dies[i][j] = len(Mitja_dies_l[i][j])
        ind = [k for k in range(len(numero_dies[i])) if numero_dies[i][k] != 0]
        if len(ind) != 0:
            element_0 = numero_dies[i][ind[0]]
            cond_1 = all(numero_dies[i][k] == element_0 for k in ind)
            if cond_1 == False:
               #print('Algo falla en el dia', day_to_date(i), i)#El +1 es per tenir en compte com esta ordenada la llista
               Dies_dolents.append( day_to_date(i))
    Dies_comprovar=[]
    for j in range(len(Dies_dolents)):
        for i in Dies_bons_filtrats:
            y = int(i[2])
            if int(i[0]) == int(Dies_dolents[j][0]) and int(i[1]) == int(Dies_dolents[j][1]):
                #print('El dia', i ,'es dolent')
                Dies_comprovar.append(i)
    
    for i  in range(len(Dies_comprovar)):
        
        in_coef, dif_dies = index_coef(int(Dies_comprovar[i][2]), int(Dies_comprovar[i][1]), int(Dies_comprovar[i][0]), Anys)
        model = np.poly1d(Coeficients[in_coef])
        secular = model(dif_dies)
            
        dades, file_type, day  = read_file(Dies_comprovar[i][0], Dies_comprovar[i][1], Dies_comprovar[i][2])
        times = notable_times2(Dies_comprovar[i][2], Dies_comprovar[i][1], Dies_comprovar[i][0])
        
        dades=data_treatment(dades,file_type)
        dades,start_time, contador_random = filter_data(dades, file_type, day, times[0], times[2], secular)

        Dies_comprovar[i].append([len(dades), times[0], times[2]])
    
    """
    #Aixo es un plot opcional per visualtizar el problema que estan donant les dades, pero es podria eliminar perfectament
    for i in Dies_comprovar:
        
        in_coef, dif_dies = index_coef(int(i[2]), int(i[1]), int(i[0]), Anys)
        model = np.poly1d(Coeficients[in_coef])
        secular = model(dif_dies)
        
        dades, file_type, day = read_file(i[0], i[1], i[2])
        day=i[0]
        times = notable_times2(i[2], i[1], i[0])
        dades=data_treatment(dades,file_type)
        dades,start_time, contador_random = filter_data(dades, file_type, day, times[0], times[2], secular)
        plt.scatter(dades['TIME'], dades['EBRD'])
        plt.title(dades['DATE'][0])
        plt.show()
    """
    return Dies_comprovar, numero_dies

# *****************************************************************************
#Creo una funcio per intentar arreglar un problema que hi ha amb els minuts:
#La cosa es que alguns anys els dies el sol surt en el minut 29 i alguns altres en el 30
#Aixo provoca, que de la forma que estan filtrades les hores les llistes tinguin longituds diferents
#Per tant el que faig es eliminar les dades extres en cas que hi hagi
def arreglar_minuts(Dies_comprovar, Mitja_dies_l):
    i = 0
    while True:
        if len(Dies_comprovar) == 0:
            break
        D_malament = []
        sunrises = []
        sunrises_h = []
        sunsets = []
        sunsets_h = []
        D_malament.append(Dies_comprovar[i])
        doy = dia_any(int(Dies_comprovar[i][0]), int(Dies_comprovar[i][1]), 2000)-1#El -1 es perque la llista comenca a 0
        j = i+1
        times = notable_minutes(int(Dies_comprovar[i][2]), int(Dies_comprovar[i][1]), int( Dies_comprovar[i][0]))
        sunrises.append(times[0])
        sunrises_h.append(times[1])
        sunsets.append(times[2])
        sunsets_h.append(times[3])
        
        while True:
            if Dies_comprovar[i][0] == Dies_comprovar[j][0] and Dies_comprovar[i][1] == Dies_comprovar[j][1]:
                D_malament.append(Dies_comprovar[j])
                times = notable_minutes(int(Dies_comprovar[j][2]), int(Dies_comprovar[j][1]), int( Dies_comprovar[j][0]))
                sunrises.append(times[0])
                sunrises_h.append(times[1])
                sunsets.append(times[2])
                sunsets_h.append(times[3])
                Dies_comprovar.pop(j)
            else:
                break#Poso el break aqui perque se que estan ordenats per dies i mesos
            if  j >= len(Dies_comprovar)-1:
                  break
        if len(D_malament) > 1:
            Dies_comprovar.pop(i)
        else:
            i += 1
        cond_1 = all(sunrises[0] == sunrises[j]  and (sunrises[j] == 30 or sunrises[j] == 29 or sunrises[j] == 31) for j in range(len(sunrises)))
        cond_2 = all(sunsets[0] == sunsets[j] and (sunsets[j] == 30 or sunsets[j] == 29 or sunsets[j] == 31) for j in range(len(sunsets)))
        if cond_1 == False and cond_2 == False:
            Mitja_dies_l[doy][min(sunrises_h)] = []
            Mitja_dies_l[doy][max(sunsets_h)] = []
        elif cond_1 == True and cond_2 == False:
            Mitja_dies_l[doy][max(sunsets_h)] = []
        elif cond_1 == False and cond_2 == True:
            Mitja_dies_l[doy][min(sunrises_h)] = []
        if i >= len(Dies_comprovar)-1:
            break
    return Mitja_dies_l 

# *****************************************************************************
#La idea darrera  d'aquesta funcio no es arreglar els dies que estiguin malament pel tema dels minuts( el mateix que en la funcio de dalt) perque per casualitat no hi son, sino que es tornar una llista que em digui en general quins son els dies que donen problemes
def dies_min_dolent():
    Dies_mal_min = []
    for i in range(366):
        dia, mes = day_to_date(i)
        times = notable_minutes(2000, mes, dia)
        sunrise_h = times[1]
        sunset_h = times[3]
        sunrise = times[0]
        sunset = times [2]
        cond_1 = (sunrise == 29 or sunrise == 30)
        cond_2 = (sunset == 29 or sunset == 30)
        if cond_1 == True and cond_2 == True:
            if sunrise == 29:
                Sunrise_def = sunrise_h+1
            elif sunrise == 30:
                Sunrise_def = sunrise_h
            if sunset == 29:
                Sunset_def = sunset_h
            elif sunset == 30:
                Sunset_def = sunset_h-1
            #La primera dada despres del mes es la hora que haure d'agafar el sunrise
            #La segona dada despres del mes es el sunset que haure d'agafar
            Dies_mal_min.append([str(dia).zfill(2), str(mes).zfill(2), Sunrise_def, Sunset_def])
        elif cond_1 == True and cond_2 == False:
            if sunrise == 29:
                Sunrise_def = sunrise_h+1
            elif sunrise == 30:
                Sunrise_def = sunrise_h
            Dies_mal_min.append([str(dia).zfill(2), str(mes).zfill(2), Sunrise_def, sunset_h])

        elif cond_1 == False and cond_2 == True:
            if sunset == 29:
                Sunset_def = sunset_h
            elif sunset == 30:
                Sunset_def = sunset_h-1
            Dies_mal_min.append([str(dia).zfill(2), str(mes).zfill(2), sunrise_h, Sunset_def])
    return Dies_mal_min
# *****************************************************************************
#Aqui busco crearme una llista dels coeficients de la regressio
def Coeff_secu(y_1, m_1, d_1, y_2, m_2, d_2, Dades2, dia_mig_extra, year_extra):
    degree = 1  # Grado del polinomio a ajustar
    Coef_list = []
    Anys = []
    #Primer miro les condicions inicials sota les que he de crear la llista, depenent de si el primer i ultim dia es troben abans o despres de juny
    if(( m_1 < 6 or (m_1 == 6 and d_1 < 15)) and (m_2 > 6 or (m_2 == 6 and d_2 >= 15))):
        for i in range(y_1-1,y_2+1):
            Anys.append(i)
            index_any = i-math.floor(Dades2[0][0])#Es important agafar aquest any com el primer ja que es on comenca la llista de Dades2
            #En el cas que l'ultim dia es trobi despres de juny he d'anar a buscar les dades per internet ja que no 
            #son definitives i no les tinc descarregades
            if index_any >= len(Dades2[0])-1:
                print('He de buscar les dades per internet i em canvia tot')
                final_day = dia_any(31, 12, year_extra-1)- dia_any(1, 6, year_extra-1) + dia_mig_extra#Estic agafant el numero total de dies fent: dies totals de l'any que estic mirant - dies que portem fins al 1 de juny+ dies que te per la mesura de l'any seguent
                #M'estableixo quin es el rang en les x que he d'agafar per fer el plot:
                #per fer aixo li resto a 365 el primer dia que comenco(l'1 de juny de l'any anterior) i li sumo els dies extres que poso
                X = [1,final_day]
                #Aqui agafo les dues dades que m'interesen
                Y = [Dades2[1][index_any]*60, Dades2[1][-1]*60]
            else:
                #Pels altres casos miro si es un any de traspas o no i poso les X en funcio d'aixo
                if (((int(i)-1) % 4 == 0 and (int(i)-1) % 100 != 0) or ((int(i)-1) % 100 == 0 and (int(i)-1) % 400 == 0)):
                    X = [1,366]
                else: 
                    X = [1,365]
                #Agafo les Y dels dos anys que toca
                Y = [Dades2[1][index_any]*60,Dades2[1][index_any+1]*60]
            coefficients = np.polyfit(X, Y, degree)
            Coef_list.append(coefficients)
    elif (((m_1 == 6 and d_1 >= 15) or m_1 > 6) and ((m_2 == 6 and d_2 >= 15) or m_2 > 6)):#No es comenten els seguents elif ja que son identics al primer if
        for i in range(y_1,y_2+1):
            Anys.append(i)
            index_any = i-math.floor(Dades2[0][0])
            if index_any >=len(Dades2[0])-1:
                print('He de buscar les dades per internet i em canvia tot')
                final_day = dia_any(31, 12, year_extra-1)- dia_any(1, 6, year_extra-1) + dia_mig_extra#Estic agafant el numero total de dies fent: dies totals de l'any que estic mirant - dies que portem fins al 1 de juny+ dies que te per la mesura de l'any seguent
                X = [1,final_day]
                Y = [Dades2[1][index_any]*60, Dades2[1][-1]*60]
            else:
                if (((int(i)-1) % 4 == 0 and (int(i)-1) % 100 != 0) or ((int(i)-1) % 100 == 0 and (int(i)-1) % 400 == 0)):
                    X = [1,366]
                else: 
                    X = [1,365]
                Y = [Dades2[1][index_any]*60,Dades2[1][index_any+1]*60]
            coefficients = np.polyfit(X, Y, degree)
            Coef_list.append(coefficients)
    elif (((m_1 == 6 and d_1 >= 15) or m_1 > 6) and (m_2 < 6 or (m_2 == 6 and d_2 < 15))):
        for i in range(y_1,y_2):
            Anys.append(i)
            index_any = i-math.floor(Dades2[0][0])
            if (((int(i)-1) % 4 == 0 and (int(i)-1) % 100 != 0) or ((int(i)-1) % 100 == 0 and (int(i)-1) % 400 == 0)):
                X = [1,366]
            else: 
                X = [1,365]
            index_any = i-y_1
            Y = [Dades2[1][index_any]*60,Dades2[1][index_any+1]*60]
            coefficients = np.polyfit(X, Y, degree)
            Coef_list.append(coefficients)
    elif ((m_1 < 6 or (m_1 == 6 and d_1 < 15)) and (m_2 < 6 or (m_2 == 6 and d_2 < 15))):
        for i in range(y_1-1,y_2):
            Anys.append(i)
            index_any = i-math.floor(Dades2[0][0])
            if (((int(i)-1) % 4 == 0 and (int(i)-1) % 100 != 0) or ((int(i)-1) % 100 == 0 and (int(i)-1) % 400 == 0)):
                X = [1,366]
            else: 
                X = [1,365]
            index_any = i-y_1
            Y = [Dades2[1][index_any]*60,Dades2[1][index_any+1]*60]
            coefficients = np.polyfit(X, Y, degree)
            Coef_list.append(coefficients)
    return Coef_list, Anys
# *****************************************************************************
#Funcio que em mira quins coeficients he d'agafar de la llista de la funcio anterior
def index_coef(y, m, d, Anys):#Aquesta funcio s'hauria de generalitzar una mica mes fent una dependencia de quins mesos comencen i tal
    for i in range(len(Anys)):
        if y == Anys[i]:
            if ((m == 6 and d >= 15) or (m > 6)):#Aqui imposo que em torni un index o un altre depenent de l'any que estic mirant i del mes
            #Si estic mirant l'any 2020 i estic en el mes 4 l'index sera el mateix que el del 2020 per com s'ha creat la llista de coeficient
            #En canvi si estic en el mes 6 ja es un index major al del 2020
                dia_inicial = date(Anys[i], 6, 1)
                dia_final = date(Anys[i], m, d)
                #Alhora li demano que em torni la diferencia de dies entre l'1 de juny de l'any que toqui
                #Per ferho servir a la regressio
                dif = (dia_final-dia_inicial).days
                index = i#He d'afegir una constant per tenir en compte si comenca abans o despres del mes 6
                #Aqui no va un +1 ja que la idea es que si tinc que el primer any comenca pel mes 7 l'element sigui el 0
            elif ((m < 6) or (m == 6 and d < 15)):
                dia_inicial = date(Anys[i]-1, 6, 1)
                dia_final = date(Anys[i], m, d)
                dif = (dia_final-dia_inicial).days
                index = i-1
            break
    return index, dif
# *****************************************************************************
#Aquesta funcio em torna una regressio entre les 00:30 i les 23:30 per eliminar
#les contribucions magnetosferiques que apareixen. NOTA IMPORTANT:
#Aquesta funcio s'ha creat ja que s'ha vist que les dades no queden centrades en el 0
#Pero si es veigues que a primeres( amb aixo em refereico sense aquesta funcio pel mig)
#queden centrades en el 0 aixo vol dir que la contribuacio d'aquesta funcio hauria de ser despreciable
def regressio_magnetosfera(dades_00, dades_23):
    X = [0, 23]
    Y = [dades_00, dades_23]
    degree = 1
    
    coefficients = np.polyfit(X, Y, degree)
    return coefficients

# *****************************************************************************
#Aquesta funcio simplement em dona una dada que necessito de la secular per fer una mitja que no tinc en la llista que va facilitar curto
def dada_extra_secular():
    url = 'http://www.obsebre.es/php/geomagnetisme/qdhorta/2023/ebr2023qmon.mon'
            

    # hdr required to access the files
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' }

    req = urllib.request.Request(url, headers=hdr)
    file = urllib.request.urlopen(req)
    data = pd.read_csv(file, skiprows=26, delimiter='\\s+')
    EBRD = []
    for j in range(len(data['EBRX'])):
        EBRD.append(np.rad2deg(np.arctan(data['EBRY'][j]/data['EBRX'][j])))
    ebrd = np.mean(EBRD)
        
    #Condicio per tenir en compte si l'any es de traspas o no
    year = datetime.strptime(data['DATE'][0], '%Y-%m-%d').year
    if (((int(year)-1) % 4 == 0 and (int(year)-1) % 100 != 0) or ((int(year)-1) % 100 == 0 and (int(year)-1) % 400 == 0)):
        c = 0
    else:
        c = 1
    dia_mig = np.ceil((data['DOY'][len(data['DOY'])-1] + c))/2
    return ebrd, dia_mig, year

# *****************************************************************************
#Aquesta funcio esta pensada per comprovar els dies que no acabao de veure bons, ja que mirare els magnetogrames i comprovare si hi ha algun any que es salvi o no, per despres cridar una altre funcio que eliminara els dies dolents
def selector_anys(Dies_Bons_2):
    #No li demano per pantalla els dies que vull mirar ja que son bastants i sera mes facil fer-ho a ma
    #Dies_mirar = [['10', '01'], ['17', '01'], ['18','01'], ['21' ,'01'], ['23', '01'], ['24', '01'], ['28', '01'], ['31','01'], ['02', '02'],['08', '02'], ['09', '02'], ['10', '02'], ['14', '02'], ['15', '02'], ['18', '02'], ['02', '03'], ['12', '03'], ['25', '12']]
    Dies_mirar = [['07', '01'], ['08', '01'], ['09', '01'], ['10', '01'], ['12', '01'], ['13','01'], ['15' ,'01'],  ['04', '02'],['07', '02'], ['08', '02'], ['09', '02'], ['10', '02'], ['12', '02'], ['14', '02'], ['15', '02'], ['16', '02'], ['18', '02'], ['25', '12']]

    #He creat una llista de llistes en la que cada subllista consta del dia i el mes(en aquest ordre)
    Anys_comprovar = []
    for j in range(len(Dies_mirar)):
        Anys_comprovar.append([Dies_mirar[j][0], Dies_mirar[j][1]])
        for k in range(len(Dies_Bons_2)):
            if Dies_mirar[j][0] == Dies_Bons_2[k][0] and Dies_mirar[j][1] == Dies_Bons_2[k][1]:
                Anys_comprovar[j].append(Dies_Bons_2[k][2])
    return Anys_comprovar

# *****************************************************************************
#Aquesta funcio em retorna un contador que val 1 si el dia que miro coincideix amb un de la llista i amb aquest contador passare al dia seguent en la funcio 'mare'
#I cal aclarir que els dies dolents s'han vist i imposat a pic i pala, ja que els grafics es veien com si no fossin calmats tot i que ho eren
def eliminador_dies(d , m, y):
    Llista_dies_dolents = [['07', '01', '1991'],  ['07', '01', '2022'], ['08', '01', '1984'], ['08', '01', '2007'], ['08', '01', '2021'],  ['09', '01', '1980'], ['09', '01', '1994'], ['09', '01', '2006'], ['09', '01', '2010'], ['09', '01', '2021'], ['10', '01', '1980'], ['10', '01', '1994'], ['10', '01', '2006'], ['10', '01', '2013'], ['10', '01', '2021'], ['12', '01', '2009'],  ['12', '01', '2018'],  ['12', '01', '2019'], ['13', '01', '2009'],  ['13', '01', '1982'], ['13', '01', '1986'],  ['13', '01', '2007'], ['13', '01', '2019'], ['13', '01', '2021'], ['13', '01', '2022'], ['15', '01', '1998'],  ['17', '01', '2009'], ['17', '01', '2010'], ['17', '01', '2016'], ['17', '01', '2018'], ['17', '01', '2020'], ['17', '01', '2021'], ['18','01', '2009'], ['18','01', '2010'], ['18','01', '2014'], ['18','01', '2018'], ['21' ,'01', '2021'], ['23', '01', '2009'],['23', '01', '2011'], ['24', '01', '2007'], ['24', '01', '2009'], ['28', '01', '2009'], ['31','01', '2006'],  ['31','01', '2013'], ['31','01', '2014'], ['31','01', '2021'], ['02', '02', '2009'],  ['04', '02', '2001'],  ['04', '02', '2007'],  ['07', '02', '1998'], ['08', '02', '2009'], ['09', '02', '2006'], ['09', '02', '2010'], ['09', '02', '2011'], ['10', '02', '1981'], ['10', '02', '2009'], ['10', '02', '2010'], ['10', '02', '2021'], ['12', '02', '1980'], ['14', '02', '1981'], ['14', '02', '2006'], ['14', '02', '2017'],['14', '02', '2018'],  ['15', '02', '2017'], ['16', '02', '1992'], ['16', '02', '1998'], ['18', '02', '2000'],  ['18', '02', '2001'], ['18', '02', '2021'], ['02', '03', '2006'],  ['02', '03', '2009'], ['12', '03', '2018'], ['25', '12', '1997'], ['25', '12', '2007'], ['25', '12', '2012']]
    for j in range(len(Llista_dies_dolents)):
        if Llista_dies_dolents[j][0] == d and Llista_dies_dolents[j][1] == m and Llista_dies_dolents[j][2] == y:
            contador = 1
            break
        else:
            contador = 0
    return contador

# *****************************************************************************
#Com el nom indica, aquesta funcio nomes es per plotejar els dies extres
def plot_dies_extres(As, Freqs, Phis, Dies_seleccionats, Coefficients, Anys, Dies_mal_min):
    def fun(x, A, w, phi):
        return A*np.sin(w*x+phi)
    j = 0
    while True:
        EBRD = []
        doy = dia_any(Dies_seleccionats[j][0], Dies_seleccionats[j][1], Dies_seleccionats[j][2])
        in_coef, dif_dies = index_coef(int(Dies_seleccionats[j][2]), int(Dies_seleccionats[j][1]), int(Dies_seleccionats[j][0]), Anys)
        model = np.poly1d(Coeficients[in_coef])
        secular = model(dif_dies)
            
        dades, file_type, day  = read_file(Dies_seleccionats[j][0], Dies_seleccionats[j][1], Dies_seleccionats[j][2])
        for k in Dies_mal_min:
            #Aqui comprovo si he de vigilar amb les hores de sortida i posta de Sol
            if int(Dies_seleccionats[j][0]) == int(k[0]) and int(Dies_seleccionats[j][1]) == int(k[1]):
                    sunrise = k[-2]
                    sunset = k[-1]
                    contador_srss = 1#Em poso aquest contador per fer un if fora del bucle
                    break
            else:
                contador_srss = 0
        if contador_srss == 1:
            X = []
            Hores = []
            for l in range(sunrise, sunset+1):
                Hores.append(str(l)+':'+str(30))
                X.append(l)
            dades = data_treatment(dades,file_type)
            dades,start_time, contador_random = filter_data(dades, file_type, day, sunrise , sunset, secular)
        else:
            times = notable_times2(Dies_seleccionats[j][2], Dies_seleccionats[j][1], Dies_seleccionats[j][0])
            dades = data_treatment(dades,file_type)
            dades,start_time, contador_random = filter_data(dades, file_type, day, times[0] , times[2], secular)
           
            X = []
            Hores = []
            for l in range(times[0], times[2]+1):
                Hores.append(str(l)+':'+str(30))
                X.append(l)
        for p in range(len(dades['EBRD'])):
            EBRD.append(dades['EBRD'][p])
        Fit = []
        for n in range(len(X)):
            Fit.append(fun(X[n], As[doy], Freqs[doy], Phis[doy]))
        dif = []
        for m in range(len(Fit)):
            dif.append(EBRD[m]-Fit[m])
        plt.plot(Hores, Fit, color = 'r')
        plt.plot(Hores, EBRD)
        plt.plot(Hores, dif, color = 'g')
        plt.xticks(rotation=45)       
        plt.xlabel('Time(Hours)')
        plt.ylabel('D(min)')
        plt.title('Dia'+ Dies_seleccionats[j][0]+'Mes'+Dies_seleccionats[j][1]+ 'Any'+Dies_seleccionats[j][2])
        plt.show()
    return Dies_seleccionats


# *****************************************************************************
#Aquesta funcio el que fara sera demanar quins indexos k vull mirar i em seleccionara els dies que tinguin aquests indexos
def Classificacio_dies_kps(Dades1):
    #Demano per pantalla quins son els indexos que es vol mirar
    #k_inf =int( input('What will be the inferior limit of K_P?(number between 0 to 9)'))
    #k_sup = int(input('What will be the inferior limit of K_P?(number between 0 to 9 and bigger than the previous  one)'))
    Dies_bons = [[], [], [], []]
    ks = [[2,3],[4,5], [6,7], [8,9]]#Creo una llista amb tots els indexos
    kps = [[], [], [], []]
    for j in range(len(ks)):#Aqui creo els diferents kps que tinc amb la notacio que fa servir l'excel
        for k in range(len(ks[j])):
            kps[j].append(str(ks[j][k])+'+')
            kps[j].append(str(ks[j][k])+'o')
            kps[j].append(str(ks[j][k])+'-')
            kps[j].append(-1*ks[j][k])
    n = 0
    #En aquesta part simplement vaig comprovant els criteris que hem donat per 
    #dir quin dia pertany a quin index. La idea es que perque pertanyi al rang
    #8-9 de kp necessita 2 valors entre 8 i 9, pel rang 6-7 en necessita 3 
    #valors dins d'aquest rang, pel 4-5 en necessita 4 i pel 2-3 en necessita 5
    while n<len(Dades1[0]):
        Dades=Dades1[:,n:n+8]
        contador_2 = 2
        for j in range(len(kps)):
            contador_1 = 0
            for l in range(len(kps[len(kps)-1-j])):
                for i in Dades[3]:
                    if i == kps[len(kps)-1-j][l]:
                        contador_1 += 1
            if contador_1 >= contador_2:
                contador_3 = 1
                break#Aquets break es important ja que la funcio ha de parar un 
                #cop ha triat un index, i se li dona mes importancia a l'index 
                #que sigui mes gran
            else:
                contador_3 = 0
            contador_2 += 1
        if contador_3 == 1:
            Dies_bons[len(Dies_bons)-1-contador_2+2].append(Dades[0][0])
        n += 8#Vaig augmentat de 8 en 8 per avancar tot el dia, ja que cada dia nomes s'agafen 8 mesures
    Dies_Bons_2 = [[], [], [], []]#Canvio el format a un que em sigui mes util
    for i in range(len(Dies_bons)):
        for j in range(len(Dies_bons[i])):
            dia = pd.Timestamp(Dies_bons[i][j])
            Dies_Bons_2[i].append([str(dia.day).zfill(2), str(dia.month).zfill(2), str(dia.year).zfill(2)])
    return Dies_Bons_2

# *****************************************************************************
#Aqui simplement filtro les dades per saber si son bones o no com ja s'ha fet 
#anteriorment
def filtre_dies_seleccionats(Dies_seleccionats, Coeficients, Anys, Dies_mal_min):
    def fun(x, A, w, phi):
        return A*np.sin(w*x+phi)
    Dies_seleccionats_filtrats = []
    for i in range(len(Dies_seleccionats)):
        Dies_seleccionats2 = Dies_seleccionats[i]
        j = 0
        while True:
            in_coef, dif_dies = index_coef(int(Dies_seleccionats2[j][2]), int(Dies_seleccionats2[j][1]), int(Dies_seleccionats2[j][0]), Anys)
            model = np.poly1d(Coeficients[in_coef])
            secular = model(dif_dies)
                
            dades, file_type, day  = read_file(Dies_seleccionats2[j][0], Dies_seleccionats2[j][1], Dies_seleccionats2[j][2])
            for k in Dies_mal_min:
                if int(Dies_seleccionats2[j][0]) == int(k[0]) and int(Dies_seleccionats2[j][1]) == int(k[1]):
                        sunrise = k[-2]
                        sunset = k[-1]
                        contador_srss = 1#Em poso aquest contador per fer un if fora del bucle
                        break
                else:
                    contador_srss = 0
            if contador_srss == 1:
                dades = data_treatment(dades,file_type)
                dades,start_time, contador_random = filter_data(dades, file_type, day, sunrise , sunset, secular)
            else:
                times = notable_times2(Dies_seleccionats2[j][2], Dies_seleccionats2[j][1], Dies_seleccionats2[j][0])
                dades = data_treatment(dades,file_type)
                dades,start_time, contador_random = filter_data(dades, file_type, day, times[0] , times[2], secular)
            
            if j == 0:
                if contador_random > 0 and j != (len(Dies_seleccionats2)-1):
                    print(j, len(Dies_seleccionats2))
                    Dies_seleccionats2.pop(j)
                    continue
                elif contador_random > 0 and j == (len(Dies_seleccionats2)-1):
                    print('El bucle ha acabat')
                    print(j, len(Dies_seleccionats2))
                    Dies_seleccionats2.pop(j)
                    break
                j += 1
            elif j >= 1:
                if contador_random > 0 and j != (len(Dies_seleccionats2)-1):
                    print(j, len(Dies_seleccionats2))
                    Dies_seleccionats2.pop(j)
                    continue
                elif contador_random > 0 and j == (len(Dies_seleccionats2)-1):
                    print('El bucle ha acabat')
                    print(j, len(Dies_seleccionats2))
                    Dies_seleccionats2.pop(j)
                    break
                j += 1
            if j == (len(Dies_seleccionats2)):#L'hi he tret el -1 ja que crec que em pot donar problemes per l'ultim dia
                print('El bucle ha acabat')
                break
        Dies_seleccionats_filtrats.append(Dies_seleccionats2)
    return Dies_seleccionats_filtrats
        
# *****************************************************************************
#Aqui afegeixo els valors dels dies ja filtarts a una llista 
# per poder calcular les mitjes
def Mitjes_anuals( Dies_seleccionats, Coefficients, Anys, Dies_mal_min, As, Freqs, Phis):
    shape = (4, 24)  # (dimension 0, dimension 1)
    
    # Generar la matriz tridimensional vacia
    Mitja = [[[] for _ in range(shape[1])] for _ in range(shape[0])]
    Mitja.append([])
    for j in range(24):
        Mitja[-1].append(j)
    for i in range(len(Dies_seleccionats)):
        Dies_seleccionats2 = Dies_seleccionats[i]
        j = 0
        while True:
            in_coef, dif_dies = index_coef(int(Dies_seleccionats2[j][2]), int(Dies_seleccionats2[j][1]), int(Dies_seleccionats2[j][0]), Anys)
            model = np.poly1d(Coeficients[in_coef])
            secular = model(dif_dies)
            doy = dia_any(Dies_seleccionats2[j][0], Dies_seleccionats2[j][1], Dies_seleccionats2[j][2])
            dades, file_type, day  = read_file(Dies_seleccionats2[j][0], Dies_seleccionats2[j][1], Dies_seleccionats2[j][2])
            for k in Dies_mal_min:
                if int(Dies_seleccionats2[j][0]) == int(k[0]) and int(Dies_seleccionats2[j][1]) == int(k[1]):
                        sunrise = k[-2]
                        sunset = k[-1]
                        contador_srss = 1#Em poso aquest contador per fer un if fora del bucle
                        break
                else:
                    contador_srss = 0
            if contador_srss == 1:
                dades = data_treatment(dades,file_type)
                dades = filter_data_2(dades, file_type, day, secular)
                for l in range(sunrise, sunset+1):
                    Mitja[i][l].append(dades['EBRD'][l]-fun(l, As[doy-1], Freqs[doy-1], Phis[doy-1]))

            else:
                times = notable_times2(Dies_seleccionats2[j][2], Dies_seleccionats2[j][1], Dies_seleccionats2[j][0])
                dades = data_treatment(dades,file_type)
                dades = filter_data_2(dades, file_type, day, secular)
                for l in range(times[0], times[2]+1):
                    Mitja[i][l].append(dades['EBRD'][l]-fun(l, As[doy-1], Freqs[doy-1], Phis[doy-1]))

            j += 1
            if j == (len(Dies_seleccionats2)):#L'hi he tret el -1 ja que crec que em pot donar problemes per l'ultim dia
                print('El bucle ha acabat')
                break

    return Mitja
        
# *****************************************************************************

Dades1 = pd.read_excel("Dades dels indexos 40 anys.xlsx")
Dades1 = np.transpose(np.array(Dades1))

Dades3 = pd.read_excel("Dades dels indexos 20 anys antics.xlsx")
Dades3 = np.transpose(np.array(Dades3))

Dades2 = pd.read_excel("VSEC_AN.xlsx")
Dades2 = np.transpose(np.array(Dades2))
Dades2 = Dades2.tolist()
ebrd, dia_mig_extra, year_extra = dada_extra_secular()

for j in range(len(Dades2)):
    if j == 0:
        Dades2[0].append(int(year_extra))
    elif j == 1:
        Dades2[1].append(ebrd)
    else:
        Dades2[j].append(0)
        
Dies_Bons_2 = Classificacio_dies(Dades1)

Anys_comprovar = selector_anys(Dies_Bons_2)

y_1 = int(Dies_Bons_2[0][2])
m_1 = int(Dies_Bons_2[0][1])
d_1 = int(Dies_Bons_2[0][0])
y_2 = int(Dies_Bons_2[-1][2])
m_2 = int(Dies_Bons_2[-1][1])
d_2 = int(Dies_Bons_2[-1][0])

Coeficients, Anys = Coeff_secu(y_1, m_1, d_1, y_2, m_2, d_2, Dades2, dia_mig_extra, year_extra)

Mitja_dies_l, Dies_bons_filtrats, Secular, Dies_pendent_gran = Llistat_dades_dies(Dies_Bons_2, Dades2, Coeficients, Anys)

Dies_comprovar, numero_dies = comprovacio_num_dies(Mitja_dies_l, Dies_bons_filtrats)
Mitja_dies_l = arreglar_minuts(Dies_comprovar, Mitja_dies_l)
Dies_mal_min = dies_min_dolent()
#Aqui simplement faig la mitja 
Mitja_dies = np.zeros((367,24))
for i in range(24):
    Mitja_dies[366][i] = i
    
for k in range(366):
    for l in range(len(Mitja_dies_l[0])):
        if len(Mitja_dies_l[k][l]) == 0:
            Mitja_dies[k][l] = 0
        else:
            Mitja_dies[k][l] = np.mean(Mitja_dies_l[k][l])
            
Mitja_dies, Dies_buits = empty_days(Mitja_dies)

#Aqui estic agafant les regressions i nomes les dades que no son 0
Primers_ajustos, As, Freqs, Phis = funct_curvefit_dies(Mitja_dies, Dies_buits, Dies_mal_min)


fig = plt.figure(figsize=(30,30))
X = []
Xs = []
Ys = []
a = 1
for j in range(24):
    X.append(str(j)+':30')
for j in range(12):
    doy = dia_any(1, j+1, 2000)
    for l in Dies_mal_min:
        if  l[0] == '01' and l[1] == str(j+1):
            sunrise = l[2]
            sunset = l[3]
            break
        else:
            sunrise, noon, sunset = notable_times2(2000, j+1, 1)
    plot = []
    plot_1 = []
    plot_2 = []
    for l in range(sunrise, sunset+1):
        plot.append(fun(l, As[doy],Freqs[doy], Phis[doy]))
    for l in range(sunrise+1):
        plot_1.append(fun(l, As[doy],Freqs[doy], Phis[doy]))
    for l in range(sunset, 24):
        plot_2.append(fun(l, As[doy],Freqs[doy], Phis[doy]))
    ax = fig.add_subplot(12,1,j+1)
    if j < 11:
        ax.xaxis.set_ticks([])
    ax.plot(X[0:sunrise+1],plot_1, color = 'b')
    ax.plot(X[sunrise:sunset+1], plot, color = 'r')
    ax.plot(X[sunset: 24], plot_2, color = 'b')
    ax.axvline(sunrise, c = 'r', label = 'sunrise')
    ax.axvline(sunset, c = 'b', label = 'sunset')
    ax.axvline(11.5, c = 'k', label = 'noon')
    Ys.append(plot)
    Xs.append(X[sunrise: sunset+1])
plt.rcParams["figure.figsize"] = (7,7) 
plt.rc('xtick', labelsize=22) 
plt.rc('ytick', labelsize=22) 
plt.rcParams['xtick.top'] = False
plt.rcParams['ytick.right'] = False
plt.rcParams['xtick.major.size'] = 20
plt.rcParams['ytick.major.size'] = 20
plt.rcParams['xtick.minor.size'] = 15
plt.rcParams['ytick.minor.size'] = 15
plt.savefig('Grafiques')
plt.show()


Primers_ajustos_net=[]
for j in range(366):
    llista_brut=[]
    dia, mes = day_to_date(j)
    
    for i in range(len(Dies_mal_min)):
        if dia == int(Dies_mal_min[i][0]) and mes == int(Dies_mal_min[i][1]):
            times = [Dies_mal_min[i][-2], 0, Dies_mal_min[i][-1]]
            break
        else:
            times = notable_times2(2000, mes, dia)
    for k in range(24):
        if times[2] >= k >= times[0]:
            llista_brut.append(Primers_ajustos[j][k])
    Primers_ajustos_net.append(llista_brut)
    
Dies_seleccionats = Classificacio_dies_kps(Dades1)
Dies_seleccionats = filtre_dies_seleccionats( Dies_seleccionats, Coeficients, Anys, Dies_mal_min)
Mitjes_seleccio_ll = Mitjes_anuals( Dies_seleccionats, Coeficients, Anys, Dies_mal_min, As, Freqs, Phis)
"""
Dies_seleccionats_2 = Classificacio_dies_kps(Dades3)
Dies_seleccionats_2 = filtre_dies_seleccionats(Dies_seleccionats_2, Coeficients, Anys, Dies_mal_min)
Mitjes_seleccio_ll_2 = Mitjes_anuals( Dies_seleccionats_2, Coeficients, Anys, Dies_mal_min, As, Freqs, Phis)
"""

"""
#Aquesta part del codi era per veure quins dies donaven errors, pero ja no en donen
for j in Dies_seleccionats_2[1]:
    dia1 = j[0]
    mes1 = j[1]
    any1 = j[2]
    in_coef, dif_dies = index_coef(int(j[2]), int(j[1]), int(j[0]), Anys)
    model = np.poly1d(Coeficients[in_coef])
    secular = model(dif_dies)
    doy = dia_any(j[0], j[1], j[2])
    dades, file_type, day  = read_file(j[0], j[1], j[2])
    for k in Dies_mal_min:
        if int(j[0]) == int(k[0]) and int(j[1]) == int(k[1]):
                sunrise = k[-2]
                sunset = k[-1]
                contador_srss = 1#Em poso aquest contador per fer un if fora del bucle
                break
        else:
            contador_srss = 0
    if contador_srss == 1:
        dades = data_treatment(dades,file_type)
        dades = filter_data(dades, file_type, day, sunrise, sunset, secular)
        plt.plot(X[sunrise: sunset+1], dades)
        plt.title('Dia'+ dia1 + 'Mes' + mes1 + 'Any' + any1)
        plt.show()
    else:
        times = notable_times2(j[2], j[1], j[0])
        dades = data_treatment(dades,file_type)
        dades = filter_data(dades, file_type, day, times[0], times[2], secular)
        plt.plot(X[times[0]:times[2]+1], dades)
        plt.title('Dia'+ dia1 + 'Mes' + mes1 + 'Any' + any1)
        plt.show()
   """ 
   
Mitjes_seleccio = [[], [], [], []]
Mitjes_seleccio.append(Mitjes_seleccio_ll[-1])
Hores_sol = []
llegenda = ['2-3', '4-5', '6-7', '8-9']
for j in range(len(Mitjes_seleccio_ll)-1):
    for i in range(len(Mitjes_seleccio_ll[j])):
        if len(Mitjes_seleccio_ll[j][i]) != 0:
            Mitjes_seleccio[j].append(np.mean(Mitjes_seleccio_ll[j][i]))
        else:
            Mitjes_seleccio[j].append(0)
    ind = [k for k in range(len(Mitjes_seleccio[j])) if Mitjes_seleccio[j][k] != 0]
    Hores_sol.append([min(ind), max(ind)])
for j in range(len(Mitjes_seleccio)-1):
    plt.plot(Mitjes_seleccio[-1][Hores_sol[j][0]:Hores_sol[j][1]],Mitjes_seleccio[j][Hores_sol[j][0]:Hores_sol[j][1]])
plt.legend(llegenda, fontsize = 17)
plt.title('Anys 1980-2022', fontsize = 25)
plt.ylabel('Diff(min)', fontsize = 22)
plt.xlabel('Time of the day(hours)', fontsize = 22)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.rcParams["figure.figsize"] = (7,7)

plt.savefig('Resultats_finals_1980_2022.png')
plt.show()
"""
Mitjes_seleccio2 = [[], [], [], []]
Mitjes_seleccio2.append(Mitjes_seleccio_ll_2[-1])
Hores_sol = []
llegenda = ['2-3', '4-5', '6-7', '8-9']
for j in range(len(Mitjes_seleccio_ll_2)-1):
    for i in range(len(Mitjes_seleccio_ll_2[j])):
        if len(Mitjes_seleccio_ll_2[j][i]) != 0:
            Mitjes_seleccio2[j].append(np.mean(Mitjes_seleccio_ll_2[j][i]))
        else:
            Mitjes_seleccio2[j].append(0)
    ind = [k for k in range(len(Mitjes_seleccio2[j])) if Mitjes_seleccio2[j][k] != 0]
    Hores_sol.append([min(ind), max(ind)])
for j in range(len(Mitjes_seleccio2)-1):
    plt.plot(Mitjes_seleccio2[-1][Hores_sol[j][0]:Hores_sol[j][1]],Mitjes_seleccio2[j][Hores_sol[j][0]:Hores_sol[j][1]])
plt.legend(llegenda, fontsize = 17)
plt.title('Anys 1980-1999', fontsize = 25)
plt.ylabel('Diff(min)', fontsize = 22)
plt.xlabel('Time of the day(hours)', fontsize = 22)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.rcParams['xtick.major.size'] = 10
plt.rcParams['ytick.major.size'] = 10
plt.rcParams['xtick.minor.size'] = 7
plt.rcParams['ytick.minor.size'] = 7
plt.rcParams["figure.figsize"] = (7,7)
plt.savefig('Resultats_finals_1980_2022.png')
plt.show()
"""

Dies_grafic = []
Periode = []
for j in range(366):
    Dies_grafic.append(j)
    Periode.append(2*math.pi/Freqs[j])
plt.plot(Dies_grafic, As)
plt.rcParams["figure.figsize"] = (7,7)
plt.yticks(fontsize = 15)
plt.xticks(fontsize = 15)       
plt.ylabel('A(min)', fontsize = 17)
plt.xlabel('Dies', fontsize = 17)
plt.savefig('Amplitude')
plt.show()

plt.plot(Dies_grafic, Periode)
plt.rcParams["figure.figsize"] = (7,7)
plt.ylabel('T(hores)', fontsize = 17)
plt.xlabel('Dies', fontsize = 17)
plt.yticks(fontsize = 15)
plt.xticks(fontsize = 15) 
plt.savefig('Periode')
plt.show()

plt.plot(Dies_grafic, Phis)
plt.rcParams["figure.figsize"] = (7,7)
plt.ylabel('Fase',fontsize = 17 )
plt.xlabel('Dies', fontsize = 17)
plt.yticks(fontsize = 15)
plt.xticks(fontsize = 15) 
plt.savefig('Fase')
plt.show()

