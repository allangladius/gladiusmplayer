from tkinter import *
import pygame
import os
from tkinter import filedialog
from tkinter import ttk
from time import strftime, gmtime

#Instanciando o Tk
root = Tk()

timeline_max = 0
root = root
#Define o titulo do Player
root.title("Gladius MPlayer")
#Define as dimensões do Player
root.geometry("1000x250")
#Impede redimensionamento na horizontal e vertical
root.resizable(False, False)
#Inicializa os módulos do Pygame junto com o módulo mixer
pygame.init()
pygame.mixer.init()
# StringVar permite definir um valor de texto para recuperar quando for necessário(Usando .set para alterar e .get para puxar)
track = StringVar()
status = StringVar()
# Container pai que exibe os rótulos(nome da música e o status da música) em uma determinada área da borda
trackframe = LabelFrame(root, 
                        text="Song Track", 
                        font=("arial", 15, "bold"), 
                        bg="#8F00FF",
                        fg="white",
                        bd=5,
                        relief=GROOVE)
trackframeplace(x=0,width=600,height=100)

songtrack = Label(trackframe, 
                    textvariable=.track, 
                    width=45, 
                    font=("arial",12,"bold"),
                    bg="#8F00FF",
                    fg="white",
                    bd=5,
                    # .grid() organiza os widgets (rótulos, botões e etc)
                    relief=GROOVE).grid(row=0,column=0,padx=10,pady=5)

trackstatus = Label(trackframe, 
                    textvariable=status, 
                    font=("arial", 20, "bold"), 
                    bg="#8F00FF",
                    fg="#B0FC38").grid(row=0,column=1,padx=10,pady=5)

# Container pai que exibe os botões play,pause,unpause e stop
buttonframe = LabelFrame(root, #Janela pai que será passada como argumento na classe MusicPlayer
                            text="Control Panel", 
                            font=("arial",15,"bold"),
                            bg="#8F00FF",
                            fg="white",
                            bd=5,
                            relief=GROOVE)


# Configura espaçamento entre as colunas
buttonframe.grid_columnconfigure(0, minsize=100)
buttonframe.grid_columnconfigure(1, minsize=100)
buttonframe.grid_columnconfigure(2, minsize=100)
buttonframe.grid_columnconfigure(3, minsize=100)
# Configura espaço entre a row 1 e a row 0 e row 2
buttonframe.rowconfigure(1, pad=50)

# Define as dimensões do Container "Control Panel"
buttonframe.place(x=0,y=100,width=600,height=200)

# Slider para Linha do tempo para mostrar o progresso da musica
timeline_slider = ttk.Scale(buttonframe, from_=0, to=timeline_max, orient="horizontal", length=380)
timeline_slider.grid(row=1, column=0, columnspan=4)


time_label = Label(buttonframe, text="00:00")
time_label.grid(row=1, column=6)


volume_label = Label(buttonframe, text="30%")
volume_label.grid(row=1, column=10)

# Slider para controle de volume
volume_slider = ttk.Scale(buttonframe, from_=0, to=100, orient="horizontal", length=100, command=setvolume)
volume_slider.set(30)
volume_slider.grid(row=1, column=8, columnspan=2)


controlbtn1 = Button(buttonframe, 
                    text="PLAY", 
                    command=playsong, 
                    width=6, 
                    height=1, 
                    font=("arial",12,"bold"),
                    fg="navyblue", 
                    bg="#B0FC38").grid(row=0,column=0,padx=0,pady=0)

controlbtn2 = Button(buttonframe, 
                    text="PAUSE", 
                    command=pausesong, 
                    width=6, 
                    height=1, 
                    font=("arial",12,"bold"),
                    fg="navyblue", 
                    bg="#B0FC38").grid(row=0,column=1,padx=0,pady=0)

controlbtn3 = Button(buttonframe, 
                    text="UNPAUSE", 
                    command=unpausesong, 
                    width=6, 
                    height=1, 
                    font=("arial",12,"bold"),
                    fg="navyblue", 
                    bg="#B0FC38").grid(row=0,column=2,padx=0,pady=0)

controlbtn4 = Button(buttonframe, 
                    text="STOP", 
                    command=stopsong, 
                    width=6, 
                    height=1, 
                    font=("arial",12,"bold"),
                    fg="navyblue", 
                    bg="#B0FC38").grid(row=0,column=3,padx=0,pady=0)



# Container Pai que vai exibir a lista de músicas
songsframe = LabelFrame(root,
                        text="Song Playlist",
                        font=("arial",15,"bold"), 
                        bg="#8F00FF", 
                        fg="white", 
                        relief=GROOVE)
# Define as dimensões do Container pai "Song Playlist"
songsframe.place(x=600,y=0,width=400,height=250)


# Cria uma Widget para a barra de rolagem na vertical
scroll_y = Scrollbar(songsframe, orient=VERTICAL)
# A classe/widget Listbox é usada para exibir as músicas.
playlist = Listbox(songsframe, 
                        yscrollcommand=scroll_y.set,
                        selectbackground="#B0FC38",
                        selectmode=SINGLE, #Permite selecionar uma música por vez
                        font=("arial",12,"bold"),
                        bg="#CF9FFF",
                        fg="navyblue",
                        bd=5,
                        relief=GROOVE)
btnopenfolder = Button(songsframe, 
                        text="Open Folder", 
                        width=15, 
                        height=1, 
                        font=("arial", 12, "bold"), 
                        fg="black", 
                        bg="#21b3de", 
                        command=addmusic)

# Coloca a barra de rolagem no lado direito e com o fill = Y garantimos que a rolagem expandirá com a janela
scroll_y.pack(side=RIGHT,fill=Y)
scroll_y.config(command=.playlist.yview) # yview Faz com que a rolagem seja vertical
# Empacota o botão Open Folder para ocupar espaço na horizontal
btnopenfolder.pack(fill=X)
# Empacota para que a caixa de playlist ocupe espaço horizantalmente e verticalmente
playlist.pack(fill=BOTH)

    
def playsong():
    #Executa o arquivo selecionado
    pygame.mixer.music.load(playlist.get(ACTIVE))
    #Captura o nome do arquivo em execução
    track.set(playlist.get(ACTIVE))
    song_length = pygame.mixer.Sound(playlist.get(ACTIVE)).get_length()
    timeline_max = float(song_length)
    status.set("-Playing")
    #Chama o modulo mixer.music do pygame para dar play()
    pygame.mixer.music.play()
    songprogress()

def stopsong():
    status.set("-Stopped")
    pygame.mixer.music.stop()

def pausesong():
    status.set("-Paused")
    pygame.mixer.music.pause()

def unpausesong():
    status.set("-Playing")
    pygame.mixer.music.unpause()

def addmusic():
    # Função que solicita ao usuario que escolha o diretorio contendo as musicas
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)

        for song in songs:
            if song.endswith(".mp3"):
                playlist.insert(END, song)

def songprogress():

    if pygame.mixer.music.get_busy():
        # Obtém o tempo de reprodução atual em segundos
        current_time = pygame.mixer.music.get_pos() // 1000
    
        # Atualiza a posição do slider da linha do tempo
        timeline_slider.set(current_time)
        current_time_str = strftime("%M:%S", gmtime(current_time))
        # Atualize o rótulo de tempo atual
        time_label.config(text=current_time_str)
        # Atualiza a linha do tempo a cada segundo
    root.after(1000, songprogress)

def setvolume(value):
    # Converte o valor do controle deslizante para uma faixa de 0.0 a 1.0
    volume = float(value) / 100
    volume_str = "{:.0f}".format(volume*100)
    # Atualiza o volume atual da música
    volume_label.config(text=f"{volume_str}%")
    pygame.mixer.music.set_volume(volume)


#Mantém a janela aberta ouvindo eventos e só fecha ao fechar a janela
root.mainloop()
