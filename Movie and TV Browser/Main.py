'''
Name: Mitchell Marino
Date: 2018-01-10
Program: Main.py
Description: The main program for the Movie and TV Browser.
'''

#Imports
import tkinter as tk
import Frame_GUI as Frame
import Data_Fetcher as Data

#Class for application GUI.
class Application_GUI(tk.Tk):
    '''
    Application GUI is the main window for the application.
    Frames will be layered and brought forward depending on which interface the
    user intends to use.
    '''

    def __init__(self):
        '''Constructor for Applicaiton GUI; The main window for the application.'''
        tk.Tk.__init__(self)
        #Establishing connection to TMDb using object created in Data_Grabber.
        self.database = Data.TMDb()
        #Setting up menu.
        self.menubar = tk.Menu(self)
        self.choice_menu = tk.Menu(self, tearoff="false")
        self.choice_menu.add_command(label="Movie Browser", command=self.launch_movie_frame)
        self.choice_menu.add_command(label="TV Show Browser", command=self.launch_tv_frame)
        self.choice_menu.add_command(label="Person Browser", command=self.launch_person_frame)
        self.choice_menu.add_command(label="Top Movies", command=self.top_movies_frame)
        self.menubar.add_cascade(label="Choose Interface", menu=self.choice_menu)
        self.menubar.add_command(label="Help", command=self.launch_help_frame)
        self.config(menu=self.menubar, bg="#194570")
        #Establishing minimum size for the application window.
        self.minsize(1200,650)
        #Create the main frame.
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        #Custom frames to be put into main frame depending on interface selected.
        self.frames = {}
        #Movie Browser Frame.
        self.frames["Movie"] = Frame.Interface_Frame(self.main_frame, "Movie", self.database)
        self.frames["Movie"].grid(row=0, column=0, sticky="nsew")
        #TV Show Browser Frame.
        self.frames["TV Show"] = Frame.Interface_Frame(self.main_frame, "TV Show", self.database)
        self.frames["TV Show"].grid(row=0, column=0, sticky="nsew")
        #Person Browser Frame.
        self.frames["Person"] = Frame.Interface_Frame(self.main_frame, "Person", self.database)
        self.frames["Person"].grid(row=0, column=0, sticky="nsew")
        #Top Movies Frame.
        self.frames["Top Movies"] = Frame.Interface_Frame(self.main_frame, "Top Movies", self.database)
        self.frames["Top Movies"].grid(row=0, column=0, sticky="nsew")
        #Help Frame.
        self.frames["Help"] = Frame.Interface_Frame(self.main_frame, "Help", self.database)
        self.frames["Help"].grid(row=0, column=0, sticky="nsew")
        #Launch movie frame as the initial top level frame.
        self.launch_movie_frame()

    def launch_movie_frame(self):
        '''Brings movie frame to the top.'''
        frame = self.frames["Movie"]
        frame.tkraise()
    
    def launch_tv_frame(self):
        '''Brings tv frame to the top.'''
        frame = self.frames["TV Show"]
        frame.tkraise()

    def launch_person_frame(self):
        '''Brings person frame to the top.'''
        frame = self.frames["Person"]
        frame.tkraise()
    
    def launch_help_frame(self):
        '''Brings help frame to the top.'''
        frame = self.frames["Help"]
        frame.tkraise()
    
    def top_movies_frame(self):
        '''Brings top movies frame to the top.'''
        frame = self.frames["Top Movies"]
        frame.tkraise()

#Launch and start application.
window = Application_GUI()
window.mainloop()


