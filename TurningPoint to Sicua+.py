#!/usr/bin/env python
# coding: utf-8

# Hecho por: Johanns Mauricio Canaval Ruiz (jm.canaval@uniandes.edu.co)
# Bajo atribución de: Antonio Manu Forero Shelton (anforero@uniandes.edu.co)
# Con financiación de: Centro de Innovación en Tecnología y Educación de la Universidad de los Andes, Colombia.


import pandas as pd
import re

column_name='Quizz 99'  #Nombre de la prueba que aparecerá en Sicua+
#Archivos a leer, el de Turning Point y Sicua+
turning_point = pd.read_excel (r'resultados.xlsx', sheet_name='Results Detail') 
with open('sicua3.xls', encoding='utf-16-le') as f:
    sicua = pd.read_table(f)


# In[2]:


sicudic=sicua.to_dict()


# In[3]:


#Getting data from TurningPoint
TurningCodes=[]
TurningGrades=[]
for index in range (len(turning_point)-15):
    TurningCodes.append(int(re.search(r'\d+', turning_point.loc[15+index][0]).group()))
    TurningGrades.append(5*turning_point.loc[15+index][2])
    


# In[4]:


def findCodeIDinTurningPoint(codigo):
    found= False
    for index in range (len(TurningCodes)):
        if ((TurningCodes[index])==codigo):
            found=True
            break;
    if (found==True):
        return index
    else:
        return None
NewColumn={}
notfoundcodes=[]
for index in range (len(sicudic["ID de alumno"])):
    IDTurning=findCodeIDinTurningPoint(sicudic["ID de alumno"][index])
    if (IDTurning==None):
        NewColumn.update({index:0})
        notfoundcodes.append(sicudic["ID de alumno"][index])
    else:
        NewColumn.update({index:TurningGrades[IDTurning]})
        
    


# In[5]:


#Función que verifica si un código está en Sicua
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
for index in range (len(TurningCodes)):
    if (IsInSicua_qm(TurningCodes[index])==False):
        nnoenc+=1
        NotFoundCodesInSicua.update({index:TurningCodes[index]})
        NotFoundGradesInSicua.update({index:TurningGrades[index]})
if nnoenc!=0:
    NotFoundInSicua.update({'Códigos no encontrados':NotFoundCodesInSicua})
    NotFoundInSicua.update({'Nota':NotFoundGradesInSicua})    
    NotFoundData=pd.DataFrame.from_dict(NotFoundInSicua)  
    NotFoundData.to_excel('Códigos no encontrados.xlsx')     

    


# In[6]:


sicudic.update({column_name: NewColumn})


# In[7]:


newsicuadata=pd.DataFrame.from_dict(sicudic)


# In[8]:


newsicuadata.to_excel('Salida a Sicua.xlsx', index=False) #revisar formato de salida


# In[9]:


print("Los códigos no encontrados en TurningPoint pero sí en Sicua fueron:"+str(notfoundcodes)+". Se les asignó por nota 0. Ya se generó un archivo de Excel para los códigos que no se encontraron en Sicua+.")

