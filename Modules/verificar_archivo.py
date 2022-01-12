
import pandas as pd 
from datetime import date, datetime, timedelta
from pandas.core.tools.datetimes import to_datetime

from pandas.core.tools.numeric import to_numeric

def verificar(archivo):

    encabezado_patron = ['Fecha/hora', 'TR1.', 'Activa (KWh)', 'TR1.E.Reactiva']
    #verificacion de encabezados# 
   
    encabezados = archivo.columns.values.tolist()
    if set(encabezado_patron) != set(encabezados):
        return "Error detectado en el ecabezado"
    
    archivo['Fecha/hora'] = archivo['Fecha/hora']+ " "+ archivo['TR1.']

   
    archivo['Fecha/hora'] = pd.to_datetime(archivo['Fecha/hora'], format ='%d/%m/%Y %H:%M:%S') 
    
    
    # verificar incremento 
    incremento = (archivo['Fecha/hora'].values[0]-archivo['Fecha/hora'].values[1]).astype('timedelta64[m]')
    incremento= incremento.astype(int)
  
    # Verificar si es minutal, quinceminutal o cincominutal
    if incremento == -1 : 
        periodo= "minutal"
    elif incremento ==-5:
        periodo = "cinco_minutal"
    elif incremento == -15:
        periodo = "quince_minutal"
    else: 
        return "No se detecto incrmento horario adecuado"
    
    #verificar hora final y hora inical 
    registro_ultimo = len(archivo)-1

    if archivo["TR1."].values[0] != "07:00:00":
        return "Error en la hora inicial"
    
    if archivo["TR1."].values[registro_ultimo] != "06:45:00":
        return "Error en la hora final"



    return True, periodo
    

def abrir(nombre ):
    archivo = pd.read_csv(nombre)
   
    piv =verificar(archivo)
   
    if type(piv) == 'str': 
        return piv
    else:
        periodo = piv[1]
        return archivo, periodo



