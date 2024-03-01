"""
Project title: API client application
Author: Piotr Frydman
"""
import requests
import json
import csv
import time
from plotly.graph_objs import Bar
from plotly import offline

if __name__=="__main__":
    #make an API call and process the response
    url = 'https://danepubliczne.imgw.pl/api/data/synop'
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        print("Błąd połączenia z API")

    else:
        response_dict = response.json()
        
        #saving data from response to file
        data = []
        current_date = time.strftime("%d-%m-%Y", time.localtime())
        filename = f"dane_imgw_{current_date}.csv"
        with open(filename, 'w',newline="") as file:
            csvwriter=csv.writer(file, delimiter=";")
            headers=['Lokalizacja','Temperatura','Ciśnienie','Wiatr','Opady']
            csvwriter.writerow(headers)
        
            for station in response_dict:
                data.append(station['stacja'])
                #replace - swapping signs to correct format insert in Excel
                data.append(station['temperatura'].replace(".", ","))
                data.append(station['cisnienie'])
                data.append(station['predkosc_wiatru'])
                data.append(station['suma_opadu'].replace(".", ","))
                csvwriter.writerow(data)
                data.clear()
        file.close()

        #sort data 
        raw_dict = {}
        stations, temperature = [], []
        for station in response_dict:
            raw_dict[station['stacja']] = station['temperatura']
            sort_dict = sorted(raw_dict.items(),key=lambda x: x[1])
        for elements in sort_dict:
            stations.append(elements[0])
            temperature.append(elements[1])
         
        #creating visualisation
        data = [{
            'type':'bar',
            'x': stations,
            'y': temperature,
            'marker':{
                'color':'rgb(180,20,20)',
                'line':{'width':1.5,'color': 'rgb(50,25,25)'}
                },
            'opacity':0.6,
            }]
        layout={
            'title': f'Temperatura we wszystkich stacjach IMGW ({current_date})',
            'titlefont': {'size':28},
            'xaxis': {
                'title':'Temperatura',
                'titlefont':{'size':24},
                'tickfont':{'size':14},
                },
            'yaxis': {
                'title': 'Lokalizacja stacji',
                'titlefont':{'size':24},
                'tickfont':{'size':14},
                },
            }
        fig={'data':data,'layout': layout}
        offline.plot(fig, filename='temperature_imgw.html')
