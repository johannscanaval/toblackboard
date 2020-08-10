#!/usr/bin/env python
# coding: utf-8




def pasar(ruta_sicua, ruta_forms, column_name):
    import pandas as pd
    import re
    import math


    #Archivos a leer, el de Forms y Sicua+
    ms_forms = pd.read_excel (ruta_forms) 
    with open(ruta_sicua, encoding='utf-16-le') as f:
        sicua = pd.read_table(f)
    ms_forms_dic=ms_forms.to_dict()
    sicudic=sicua.to_dict()
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
    keys=list(ms_forms_dic.keys())
    Forms_Names=keys[6:]
    Forms_Grades=[]
    for index in range (len(keys)-6):
        student_grade=0
        iteration=0
        for index_2 in range (len(ms_forms_dic[list(ms_forms_dic)[index+6]])):
            if not math.isnan(ms_forms_dic[list(ms_forms_dic)[index+6]][index_2]):
                iteration+=1
                student_grade+=ms_forms_dic[list(ms_forms_dic)[index+6]][index_2]
        if (iteration>0):
            Forms_Grades.append(student_grade/iteration)
        else:
            Forms_Grades.append(0)
    def findNameIDinForms(name):
        found= False
        for index in range (len(Forms_Names)):
            if ((Forms_Names[index])==name):
                found=True
                break;
        if (found==True):
            return index
        else:
            return None
    NewColumn={}
    notfoundnames=[]
    for index in range (len(sicudic["Nombre"])):
        IDForms=findNameIDinForms(sicudic["Nombre"][index]+" "+sicudic["Apellidos"][index])
        if (IDForms==None):
            NewColumn.update({index:0})
            notfoundnames.append(sicudic["Nombre"][index]+" "+sicudic["Apellidos"][index])
        else:
            NewColumn.update({index:Forms_Grades[IDForms]})

    sicudic.update({column_name: NewColumn})
    newsicuadata=pd.DataFrame.from_dict(sicudic)
    newsicuadata.to_excel('Salida a Sicua Excel.xlsx', index=False) #Se guarda en Excel
    newsicuadata.to_csv('Salida a Sicua csv.xls', index=False, sep='\t')

    #Función que verifica si un nombre está en Sicua
    def IsInSicua_qm(name):
        found= False
        for index in range (len(sicudic["Nombre"])):
            if ((sicudic["Nombre"][index]+" "+sicudic["Apellidos"][index])==name):
                found=True
                break;
        return found
    NotFoundCodesInSicua={}
    NotFoundGradesInSicua={}
    NotFoundInSicua={}
    nnoenc=0
    for index in range (len(Forms_Names)):
        if (IsInSicua_qm(Forms_Names[index])==False):
            nnoenc+=1
            NotFoundCodesInSicua.update({index:Forms_Names[index]})
            NotFoundGradesInSicua.update({index:Forms_Grades[index]})
    if nnoenc!=0:
        NotFoundInSicua.update({'Nombres no encontrados':NotFoundCodesInSicua})
        NotFoundInSicua.update({'Nota':NotFoundGradesInSicua})    
        NotFoundData=pd.DataFrame.from_dict(NotFoundInSicua)  
        NotFoundData.to_excel('Nombres no encontrados.xlsx')     

