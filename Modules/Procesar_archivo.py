from contextlib import nullcontext
import pandas as pd 
from datetime import date, datetime, timedelta
import time
from pandas._libs.tslibs.timestamps import Timestamp
from pandas.core.frame import DataFrame
from pandas.io.sql import DatabaseError

def procesar(dataframe, periodo, tarifas): 

    if periodo =="quince_minutal": 
        
        registro_ultimo = len(dataframe)-1

        tarifas_df= pd.concat({k: pd.Series(v) for k, v in tarifas[1].items()}).reset_index()
        festivos= tarifas[0]
        periodos_tarifa1 = tarifas[1]
        periodos_tarifa2 = tarifas[2]
        periodos_tarifa3 = tarifas[3]
        periodos_tarifa4 = tarifas[4]

        tarifa_inicio=[]
        tarifa_final= []
        tarifa =[]

        periodos=[]

        eliminar_vacios(periodos_tarifa1)
        eliminar_vacios(periodos_tarifa2)
        eliminar_vacios(periodos_tarifa3)
        eliminar_vacios(periodos_tarifa4)
        

        for cont in range(1, len(tarifas),1):
            tarifa_inicio.append(datetime.strptime(tarifas[cont]['vigencia_inicial'],'%d/%m/%Y'))
            tarifa_final.append(datetime.strptime(tarifas[cont]['vigencia_final'],'%d/%m/%Y'))
        
        
        for cont in range (0, len(dataframe),1):

            for cont2 in range (len(tarifa_inicio)-1,-1,-1):
                pivote=dataframe['Fecha/hora'][cont].to_pydatetime()

                if pivote >= tarifa_inicio[cont2]:

                    tarifa.append(cont2+1)
                    break

        dataframe['tarifas']= tarifa    

        for cont in range (0, len(dataframe),1):
            if dataframe['tarifas'][cont]==1:
                periodos.append(cal_periodo(dataframe['Fecha/hora'][cont],periodos_tarifa1, festivos))
            elif dataframe['tarifas'][cont]==2:
                periodos.append(cal_periodo(dataframe['Fecha/hora'][cont],periodos_tarifa2, festivos))
            elif dataframe['tarifas'][cont]==3:
                periodos.append(cal_periodo(dataframe['Fecha/hora'][cont],periodos_tarifa3, festivos))
            elif dataframe['tarifas'][cont]==4:
                periodos.append(cal_periodo(dataframe['Fecha/hora'][cont],periodos_tarifa4, festivos))
        
        dataframe['Periodos']= periodos
        

        
                    
def cal_periodo(fecha, tarifa, festivos):
    #obtener dia de la fecha 
    dia_semana=fecha.isoweekday()
    tar=[]
    festivos_piv = festivos.get('festivos').values()
    periodos= []

    for fecha_festivo in festivos_piv: 
        
        fecha_piv = datetime.strptime(fecha_festivo, '%d/%m/%Y')
        
        if (fecha.day == fecha_piv.day and fecha.month == fecha_piv.month and fecha.year == fecha_piv.year ):
            dia_semana = 7
            break

    if dia_semana <= 5: 
        
        tar.append(tarifa.get('periodo_base'))
        tar.append(tarifa.get('periodo_intermedia'))
        tar.append(tarifa.get('periodo_punta'))
        return sel_tarifa(fecha,dia_semana, tar )
    elif dia_semana == 6 : 
        tar.append(tarifa.get('periodo_base_sabado'))
        tar.append(tarifa.get('periodo_inter_sabado'))
        tar.append(tarifa.get('periodo_punta_sabado'))
        return sel_tarifa(fecha, dia_semana, tar )
        
    elif dia_semana == 7: 
        tar.append(tarifa.get('periodo_base_domingo'))
        tar.append(tarifa.get('periodo_inter_domingo'))
        tar.append(tarifa.get('periodo_punta_domingo'))
        return sel_tarifa(fecha, dia_semana, tar )
    else : 
        return "La fecha es inadecuada"


def sel_tarifa(fecha, dia_semana, tar):
    
    piv_eliminar_dic=[]
    for element in range(0,len(tar),1):
        
        if not bool(tar[element]):
            piv_eliminar_dic.append(element)


    for element in piv_eliminar_dic:
        tar.pop(element)

    peri =1
    for element in tar : 
        
        horario = list(element.items())
        
        for hora in range (0, len(horario),2):
                   
            inicio_tupla= time.strptime(horario[hora][1],'%H:%M')
            final_tupla= time. strptime(horario[hora+1][1], '%H:%M')
            timestamp_inicio=(inicio_tupla.tm_hour, inicio_tupla.tm_min)
            timestamp_final= (final_tupla.tm_hour, final_tupla.tm_min)
            
            registro_tupla= (fecha.hour, fecha.minute)
            registro_final = (fecha.hour*60) + fecha.minute
            timestamp_inicio_completo= (timestamp_inicio[0]*60)+ timestamp_inicio[1]
            timestamp_final_completo= (timestamp_final[0]*60)+ timestamp_final[1]

            if (registro_final>= timestamp_inicio_completo and registro_final<= timestamp_final_completo):

                if peri ==1 :
                   return "base"
                elif peri ==2: 
                    return "intermedia"
                elif peri == 3: 
                    return "punta"
        peri= peri+1      

def eliminar_vacios(diccionario):
    
    piv_eliminar=[]
    piv_eliminar_dic=[]
    
    for dic in diccionario:

        for element in diccionario.get(dic):
           
            if len(element)>1:


                if diccionario[dic][element] == None :

                    piv_eliminar.append([dic, element])
            else: 
                break
    
    for element in piv_eliminar:
        
        diccionario[element[0]].pop(element[1])
  
    for element in diccionario:

        if not bool(diccionario[element]):
            piv_eliminar_dic.append(element)
    
    

def dem_max (dataframe):
    id_max= dataframe.loc[dataframe['Activa (KWh)'].idxmax()]
    id_min= dataframe.loc[dataframe['Activa (KWh)'].idxmin()]
    consumo_total = dataframe['Activa (KWh)'].sum() 
    reactivos_total = dataframe['TR1.E.Reactiva'].sum()

    consumo= [consumo_total, reactivos_total]

    serie_consumo = pd.Series(consumo) 

    df_max = pd.DataFrame(id_max)
    df_min = pd.DataFrame(id_min)
    df_consumo = pd.DataFrame(serie_consumo)
    

    df_dm = pd.concat([df_max, df_min, df_consumo], axis =1)
    df_dm.columns=["Demanda Maxima", "Demanda Minima", "consumo total" ]
   
    return df_dm


  
