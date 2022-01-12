import json
import pandas as pd 

def cargar(): 
    cfg_archivos = ['./data/festivos.json', './data/tarifa_1.json', './data/tarifa_2.json', './data/tarifa_3.json', './data/tarifa_4.json']
    tarifa_all=[]
    for archivo in cfg_archivos:
            with open (archivo) as File: 
                tarifa_all.append(json.load(File))
    
    return tarifa_all