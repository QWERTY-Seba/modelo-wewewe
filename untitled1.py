# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 21:10:39 2024

@author: Seba
"""

from tkinter import *
from tkinter import Canvas
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
from pathlib import Path
from PIL import Image, ImageTk
import time
import os
import imghdr

from math import floor
#CAMBIAR A UNA CLASE

path = None

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=1)


label = ttk.Label(frm, text="Hello World!")
label.grid(column=0, row=1)


def extraer():
    path = filedialog.askdirectory()
    label["text"] = path
    
    # parent_folder = tree.insert("",END,text=path,open=True)
    # process_directory(parent_folder, path)
    # tree.grid(column=0, row=3)
    
    
    
    #REVISAR QUE HAYA ALGO
    print(path)


#HAY QUE ENCONTRAR EL PATH CON IMAGENES ANTES DE MANDAR ACA
#EL PATH DEBERIA SER ARCHIVO o PATH OBJECT?
def extraer_imagenes_path(path):
    #LEER PATH
    lista_archivos = os.listdir(path)
    imagenes = []
    
    for image in lista_archivos:       
        img = Image.open(path / image)
        
        if img.format not in ['JPEG','PNG','JPG']:
            continue
        
        # img.resize((500,500))
        imagenes.append(img)
    return imagenes


def cargar_imagenes_en_frame(path):
    imagenes = extraer_imagenes_path(path)
    #CARGAR FRAME
    
    def toggle_highlight(event):
        frame = event.widget
        if frame.highlighted:
             frame["background"] = 'white'
             frame.highlighted = False
        else:
             frame["background"] = 'red'
             frame["borderwidth"] = 10
             frame.highlighted = True
    
    columnas = 3
    for i,img in enumerate(imagenes):
        
        y = floor(i/columnas)
        x = i%columnas
        
        photo = ImageTk.PhotoImage(img)
        label = ttk.Label(frame_imagenes, image = photo)
        label.img = photo
        label.highlighted = False  # To keep track of whether the image is highlighted
        label.bind('<Button-1>', toggle_highlight)
        label.grid(column=x, row=y)
        
    
    
    

def crear_csv_labels():
    pass

def limpiar_frame_imagenes():
    pass


#LEER EL JSON Y MARCAR LOS ARCHIVOS YA TIENEN LABEL
def process_directory(parent,path):
    for i in os.listdir(path):
        abspath = os.path.join(path,i)
        isdir = os.path.isdir(abspath)
        if isdir:
            elements = tree.insert(parent,END,text=i,open=False,values=(abspath,))
            process_directory(elements,abspath)




#ITERAR HASTA LLEGAR A LAS CARPETAS CON FOTOS
#CREAR FRAME DONDE CARGAR LAS IMAGENES
tree = ttk.Treeview(root,show="tree")
frame_imagenes = ttk.Frame(width=1500, height=500)
frame_imagenes['borderwidth'] = 5
frame_imagenes['relief'] = 'sunken'

scroll = ttk.Scrollbar(frame_imagenes, orient="vertical")
# scroll.pack(side="right", fill="y")


frame_imagenes.grid(column=0, row=5)
cargar_imagenes_en_frame(Path(r'G:\ExtensionChrome\wewewe_model\growdiaries\gorilla-cookies-auto\176767'))
ttk.Button(frm, text="Seleccionar Carpeta", command=extraer).grid(column=1, row=0)

root.mainloop()


root.destroy()

