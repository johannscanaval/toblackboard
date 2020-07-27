#!/usr/bin/env python
# coding: utf-8

# In[4]:


from appJar import gui
import nearpod_app as api

app = gui()
app.addLabel("title", "Hola, bienvenido")
app.setLabelBg("title", "red")
app.addLabelEntry("Nombre de la columna")
def press(button):
    if button == "Salir":
        app.stop()
    else:
        ruta_nearpod=app.openBox(title="Por favor, ingresa el archivo de salida de Nearpod", dirName=None, fileTypes=None, asFile=False, parent=None, multiple=False, mode='r')
        ruta_sicua=app.openBox(title="Por favor, ingresa el archivo del Centro de Calificaciones", dirName=None, fileTypes=None, asFile=False, parent=None, multiple=False, mode='r')
        column_name = app.getEntry("Nombre de la columna")
        api.pasar(ruta_sicua, ruta_nearpod, column_name)
        app.infoBox("Información", "Aparentemente, todo se hizo", parent=None)
app.addButtons(["Ingresar archivos", "Salir"], press)
app.go()


# In[ ]:




