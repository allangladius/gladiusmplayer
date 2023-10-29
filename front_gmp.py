from tkinter import *
import pygame
import os
from tkinter import filedialog
from tkinter import ttk
from time import strftime, gmtime

class RenderGui():
    # Renderização do Front-End e Funções Que envolvam front-end

    def __init__(self, root):
        self.timeline_max = 0
        self.root = root
        #Define o titulo do Player
        self.root.title("Gladius MPlayer")
        #Define as dimensões do Player
        self.root.geometry("1000x250")
        #Impede redimensionamento na horizontal e vertical
        self.root.resizable(False, False)
        #Inicializa os módulos do Pygame junto com o módulo mixer
        pygame.init()
        pygame.mixer.init()
        # StringVar permite definir um valor de texto para recuperar quando for necessário(Usando .set para alterar e .get para puxar)
        self.track = StringVar()
        self.status = StringVar()
        # Container pai que exibe os rótulos(nome da música e o status da música) em uma determinada área da borda
        trackframe = LabelFrame(self.root, 
                                text="Song Track", 
                                font=("arial", 15, "bold"), 
                                bg="#8F00FF",
                                fg="white",
                                bd=5,
                                relief=GROOVE)
        trackframe.place(x=0,width=600,height=100)

        songtrack = Label(trackframe, 
                          textvariable=self.track, 
                          width=45, 
                          font=("arial",12,"bold"),
                          bg="#8F00FF",
                          fg="white",
                          bd=5,
                          # .grid() organiza os widgets (rótulos, botões e etc)
                          relief=GROOVE).grid(row=0,column=0,padx=10,pady=5)
        
        trackstatus = Label(trackframe, 
                            textvariable=self.status, 
                            font=("arial", 20, "bold"), 
                            bg="#8F00FF",
                            fg="#B0FC38").grid(row=0,column=1,padx=10,pady=5)
        
        # Container pai que exibe os botões play,pause,unpause e stop
        buttonframe = LabelFrame(self.root, #Janela pai que será passada como argumento na classe MusicPlayer
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
        self.timeline_slider = ttk.Scale(buttonframe, from_=0, to=self.timeline_max, orient="horizontal", length=380)
        self.timeline_slider.grid(row=1, column=0, columnspan=4)
        

        self.time_label = Label(buttonframe, text="00:00")
        self.time_label.grid(row=1, column=6)
        

        self.volume_label = Label(buttonframe, text="30%")
        self.volume_label.grid(row=1, column=10)
        
        # Slider para controle de volume
        self.volume_slider = ttk.Scale(buttonframe, from_=0, to=100, orient="horizontal", length=100, command=self.setvolume)
        self.volume_slider.set(30)
        self.volume_slider.grid(row=1, column=8, columnspan=2)


        self.controlbtn1 = Button(buttonframe, 
                         text="PLAY", 
                         command=self.playsong, 
                         width=6, 
                         height=1, 
                         font=("arial",12,"bold"),
                         fg="navyblue", 
                         bg="#B0FC38").grid(row=0,column=0,padx=0,pady=0)
        
        self.controlbtn2 = Button(buttonframe, 
                         text="PAUSE", 
                         command=self.pausesong, 
                         width=6, 
                         height=1, 
                         font=("arial",12,"bold"),
                         fg="navyblue", 
                         bg="#B0FC38").grid(row=0,column=1,padx=0,pady=0)
        
        self.controlbtn3 = Button(buttonframe, 
                         text="UNPAUSE", 
                         command=self.unpausesong, 
                         width=6, 
                         height=1, 
                         font=("arial",12,"bold"),
                         fg="navyblue", 
                         bg="#B0FC38").grid(row=0,column=2,padx=0,pady=0)
        
        self.controlbtn4 = Button(buttonframe, 
                         text="STOP", 
                         command=self.stopsong, 
                         width=6, 
                         height=1, 
                         font=("arial",12,"bold"),
                         fg="navyblue", 
                         bg="#B0FC38").grid(row=0,column=3,padx=0,pady=0)
        
        
        
        # Container Pai que vai exibir a lista de músicas
        songsframe = LabelFrame(self.root,
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
        self.playlist = Listbox(songsframe, 
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
                               command=self.addmusic)
        
        # Coloca a barra de rolagem no lado direito e com o fill = Y garantimos que a rolagem expandirá com a janela
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.playlist.yview) # yview Faz com que a rolagem seja vertical
        # Empacota o botão Open Folder para ocupar espaço na horizontal
        btnopenfolder.pack(fill=X)
        # Empacota para que a caixa de playlist ocupe espaço horizantalmente e verticalmente
        self.playlist.pack(fill=BOTH)
        
        
    def playsong(self):
        #Executa o arquivo selecionado
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        #Captura o nome do arquivo em execução
        self.track.set(self.playlist.get(ACTIVE))
        self.song_length = pygame.mixer.Sound(self.playlist.get(ACTIVE)).get_length()
        self.timeline_max = float(self.song_length)
        self.status.set("-Playing")
        #Chama o modulo mixer.music do pygame para dar play()
        pygame.mixer.music.play()
        self.songprogress()

    def stopsong(self):
        self.status.set("-Stopped")
        pygame.mixer.music.stop()

    def pausesong(self):
        self.status.set("-Paused")
        pygame.mixer.music.pause()

    def unpausesong(self):
        self.status.set("-Playing")
        pygame.mixer.music.unpause()

    def addmusic(self):
        # Função que solicita ao usuario que escolha o diretorio contendo as musicas
        path = filedialog.askdirectory()
        if path:
            os.chdir(path)
            songs = os.listdir(path)

            for song in songs:
                if song.endswith(".mp3"):
                    self.playlist.insert(END, song)

    def songprogress(self):

        if pygame.mixer.music.get_busy():
            # Obtém o tempo de reprodução atual em segundos
            current_time = pygame.mixer.music.get_pos() // 1000
       
            # Atualiza a posição do slider da linha do tempo
            self.timeline_slider.set(current_time)
            current_time_str = strftime("%M:%S", gmtime(current_time))
            # Atualize o rótulo de tempo atual
            self.time_label.config(text=current_time_str)
            # Atualiza a linha do tempo a cada segundo
        self.root.after(1000, self.songprogress)

    def setvolume(self, value):
        # Converte o valor do controle deslizante para uma faixa de 0.0 a 1.0
        volume = float(value) / 100
        volume_str = "{:.0f}".format(volume*100)
        # Atualiza o volume atual da música
        self.volume_label.config(text=f"{volume_str}%")
        pygame.mixer.music.set_volume(volume)

