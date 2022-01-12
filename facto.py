
import pandas as pd
import json
from Modules import cargar_tarifas, verificar_archivo, Procesar_archivo
from openpyxl import load_workbook

def run():
    nombre=input("Introduce el nombre del archivo de consumos a procesar:  ")
    print('\n\n')
    print("El archivo esta siendo procesado ...")
    try: 
        archivo = verificar_archivo.abrir(nombre)
        periodo = archivo[1]
        archivo = archivo[0]
        
        tarifas = cargar_tarifas.cargar()       
        if type(archivo) != 'pandas.core.frame.DataFrame':
            if type(archivo) == 'str':
                print(type(archivo))
                raise ValueError(archivo)
        if tarifas == False:
            raise ValueError("Error en los datos de configuracion")
        
        Procesar_archivo.procesar(archivo,periodo, tarifas)

        base= archivo['Periodos']=='base'
        base_final= archivo[base]
        intermedia= archivo['Periodos']=='intermedia'
        intermedia_final=archivo[intermedia]
        punta= archivo['Periodos']=='punta'
        punta_final= archivo[punta]


        archivo.to_excel('mydata.xlsx', "Datos")
        book = load_workbook('mydata.xlsx')
        writer = pd.ExcelWriter('mydata.xlsx', engine='openpyxl')
        writer.book = book

        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        base_final.to_excel(writer,"Base")
        intermedia_final.to_excel(writer,"Intermedia")
        punta_final.to_excel(writer,"Punta")

        dm_base = Procesar_archivo.dem_max(base_final)
        dm_inter = Procesar_archivo.dem_max(intermedia_final)
        dm_punta = Procesar_archivo.dem_max(punta_final)

        dm_total = Procesar_archivo.dem_max(archivo)

        dm_total.to_excel(writer,'Resumen total')
        dm_base.to_excel(writer,'Resumen Base')
        dm_inter.to_excel(writer,'Resumen Intermedia')
        dm_punta.to_excel(writer,'Resumen punta')

        writer.save()

        print('\n\n')
        print("Archivo procesado correctamente")
        print("Archivo guardado correctamente")
        print("Todo ocurrio con normalidad")


                   
    except Exception as e :
        print("Algo ha salido mal al procesar el archivo...")
        print(e)


if __name__ =='__main__':
    print('\n\n')
    print("*******************************************************************************")
    print("**                  Ejecutable de facturacion a corrugados                   **")
    print("*******************************************************************************")
    print('\n\n')
    run()

        