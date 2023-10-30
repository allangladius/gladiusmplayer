from back_front_gmp import RenderGui
from tkinter import *




#Instanciando o Tk
root = Tk()
#Argumento passado a classe RenderGui para ser a janela principal
RenderGui(root)
#Mantém a janela aberta ouvindo eventos e só fecha ao fechar a janela
root.mainloop()
