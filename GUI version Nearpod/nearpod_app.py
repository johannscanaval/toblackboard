#!/usr/bin/env python
# coding: utf-8


def pasar(ruta_sicua, ruta_nearpod, column_name):
    import pandas as pd
    import re
    #Aquí se leen y procesan los datos
    with open(ruta_sicua, encoding='utf-16-le') as f:
        sicua_file = pd.read_table(f)    
    with open(ruta_nearpod, encoding='cp1252') as f:
        nearpod_file = pd.read_table(f, delimiter=',')
    nearpod_dic=nearpod_file.to_dict()
    nearpod_data = list(nearpod_dic.items())
    sicudic=sicua_file.to_dict()

    #--------------------------------------------------FUNCIÓN EXPERIMENTAL--------------------------------------------------------
    # Por alguna razón, en algunos archivos, Blackboard pone unos espacios de sobra al final de cada línea. Esto es leído como una 
    # nueva columna. Esta función busca eliminar esas columnas basura.
    nombres_columnas_basura=[]
    key_names=list(sicudic.keys())
    busqueda_de_basura='Unnamed:'
    for index in range (len(sicudic)):
        if (busqueda_de_basura==key_names[index][:len(busqueda_de_basura)]):
            nombres_columnas_basura.append(key_names[index]) 
    for index in range (len(nombres_columnas_basura)):
        sicudic.pop(nombres_columnas_basura[index], None) 
#-------------------------------------------------------------------------------------------------------------------------------
    # Aquí se buscaran las columnas que tienen inicios tipo 'Cuestionario Correctas %',
    # que es donde se guardan las calificaciones: 0 o 100% para el caso de cuestionarios
    # individuales en Nearpod. El término puesto es el que por defecto pone Nearpod a
    # los cuestionarios en Español. Sin embargo, si quiere cambiar el término a buscar,
    # modifique la variable 'busqueda'.

    busqueda='Cuestionario Correctas %'

    columnas_validas=[nearpod_data[0][1]] #Aquí el primer dato es un diccionario con los códigos.
    for index in range (len(nearpod_data)):
        if (busqueda==nearpod_data[index][0][0:len(busqueda)]):
            columnas_validas.append(nearpod_data[index][1]) #El resto serán diccionarios con los puntajes por cuestionario

    # Aquí se sumarán, calcularán y guardarán las notas de cada código
    CodigosNearpod=[]
    NotasNearpod=[]
    numeronotas=(len(columnas_validas))-1
    for index in range (len(columnas_validas[0])):
        CodigosNearpod.append(columnas_validas[0][index])
        suma_estudiante=0
        for index_2 in range (numeronotas):
            suma_estudiante+=columnas_validas[index_2+1][index]
        NotasNearpod.append((suma_estudiante)/(numeronotas*20))

    #Se buscarán los códigos de Sicua en Nearpod, se crearán los diccionarios que luego se añadirán al DataFrame nuevo.
    def findCodeIDinNearpod(codigo):
        found = False
        for index in range (len(CodigosNearpod)):
            if ((CodigosNearpod[index])==codigo):
                found=True
                break;
        if (found==True):
            return index
        else:
            return None
    NewColumn={}
    notfoundcodes=[]
    for index in range (len(sicudic["ID de alumno"])):
        IDNearpod=findCodeIDinNearpod(sicudic["ID de alumno"][index])
        if (IDNearpod==None):
            NewColumn.update({index:0})
            notfoundcodes.append(sicudic["ID de alumno"][index])
        else:
            NewColumn.update({index:NotasNearpod[IDNearpod]})        
    sicudic.update({column_name: NewColumn})
    newsicuadata=pd.DataFrame.from_dict(sicudic)
    newsicuadata.to_excel('Salida a Sicua Excel.xlsx', index=False) #Se guarda en Excel
    newsicuadata.to_csv('Salida a Sicua csv.xls', index=False, sep='\t')

    # Esta parte busca sacar un archivo de Excel con los códigos y las notas de las personas cuyo código no está en Sicua+
    # Función que verifica si un código está en Sicua
    def IsInSicua_qm(code):
        found= False
        for index in range (len(sicudic["ID de alumno"])):
            if (sicudic["ID de alumno"][index]==code):
                found=True
                break;
        return found
    NotFoundCodesInSicua={}
    NotFoundGradesInSicua={}
    NotFoundInSicua={}
    nnoenc=0
    for index in range (len(CodigosNearpod)):
        if (IsInSicua_qm(CodigosNearpod[index])==False):
            nnoenc+=1
            NotFoundCodesInSicua.update({index:CodigosNearpod[index]})
            NotFoundGradesInSicua.update({index:NotasNearpod[index]})
    if nnoenc!=0:
        NotFoundInSicua.update({'Códigos no encontrados':NotFoundCodesInSicua})
        NotFoundInSicua.update({'Nota':NotFoundGradesInSicua})    
        NotFoundData=pd.DataFrame.from_dict(NotFoundInSicua)  
        NotFoundData.to_excel('Códigos no encontrados.xlsx')     

