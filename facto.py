
import pandas as pd
import json
from Modules import cargar_tarifas, verificar_archivo, Procesar_archivo
from openpyxl import load_workbook
import emoji


def run():
    class bcolors:
        OK = '\033[92m' #GREEN
        WARNING = '\033[93m' #YELLOW
        FAIL = '\033[91m' #RED
        RESET = '\033[0m' #RESET COLOR

    nombre=input("Introduce el nombre del archivo de consumos a procesar:  ")
    print('\n\n')
    print(emoji.emojize(f":hourglass_not_done: {bcolors.WARNING}El archivo esta siendo procesado ...{bcolors.RESET}"))
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
       
        nombre_procesado= nombre[0:len(nombre)-4]+'_procesado.xlsx'

        archivo.to_excel(nombre_procesado, "Datos")
        book = load_workbook(nombre_procesado)
        writer = pd.ExcelWriter(nombre_procesado, engine='openpyxl')
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
        print(emoji.emojize(f':check_mark_button: {bcolors.OK} Archivo procesado correctamente {bcolors.RESET} '))
        print(emoji.emojize(f':check_mark_button: {bcolors.OK} Archivo guardado correctamente {bcolors.RESET}'))
        print(emoji.emojize(f':check_mark_button: {bcolors.OK} Terminado con normalidad {bcolors.RESET}'))
        print('\n\n')
        


                   
    except Exception as e :
        print('\n\n')
        print(emoji.emojize(f":cross_mark: {bcolors.FAIL}Algo ha salido mal al procesar el archivo...{bcolors.RESET}"))
        print(emoji.emojize(f":cross_mark: {bcolors.FAIL}{e}: {nombre}{bcolors.RESET}"))
        print('\n\n')


if __name__ =='__main__':
    class bcolors:
        OK = '\033[92m' #GREEN
        WARNING = '\033[93m' #YELLOW
        FAIL = '\033[91m' #RED
        RESET = '\033[0m' #RESET COLOR
    print('\n\n')
    print(f"{bcolors.OK}*******************************************************************************{bcolors.RESET}")
    print(f"{bcolors.OK}**                  Ejecutable de facturacion a corrugados                   **{bcolors.RESET}")
    print(f"{bcolors.OK}*******************************************************************************{bcolors.RESET}")
    print('\n\n')
    run()

        