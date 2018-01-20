'''
Name: Mitchell Marino
Date: 2018-01-10
Program: Frame_GUI.py
Description: Builds all the interfaces for the Movie and TV Browser application.
             Provides functionality allowing the user to search for movies, tv shows and people.
             It allows the searching of top movies.
             Parses and massages data for eloquent output.
'''

#Imports
import tkinter as tk
from tkinter.font import Font
from urllib.request import urlopen
import Image_Processing as Image

class Interface_Frame(tk.Frame):

    def __init__(self, container, frame_type, database):
        '''Build the frame, establish global variables.'''
        #Call constructor of inherited class.
        tk.Frame.__init__(self, master=container,padx=10,pady=10,relief="groove", bg="#194570")
        #Initialize database communication.
        self.database = database
        #IDs of Query results will be stored in search results.
        self.search_results = {}
        #Adjust type of frame so the Interface_Frame knows what type of Frame it is.
        self.frame_type = frame_type
        self.last_query = "" #To help limit requests per second to TMDb.
        #Fonts to be used for the Frame's widgets.
        self.main_bold_font = Font(family="Helvetica",size=25,weight="bold")
        self.main_norm_font = Font(family="Helvetica",size=25,weight="normal")
        self.alt_bold_font = Font(family="Helvetica",size=15,weight="bold")
        self.alt_norm_font = Font(family="Helvetica",size=15,weight="normal")
        #Split Main Frame into two Subframes; Left side and Right side.
        #Left Side
        if self.frame_type != "Help":
            #Note: Help frame does not require a left frame; will only use the right frame.
            left_side = tk.Frame(self,padx=5,pady=5,relief="groove", bg="#194570")  
            left_side.pack(anchor="nw", expand=False, fill="y",side="left")   
            left_side.grid_columnconfigure(0, weight=1)
        #Right Side
        right_side = tk.Frame(self,padx=5,pady=5,relief="groove", bg="#194570")
        right_side.pack(anchor="nw", expand=True, fill="both",side="right")
        right_side.grid_columnconfigure(0, weight=1)
        #If frame type is not of type "Top Movies, it will be built as a browser frame."
        if self.frame_type != "Top Movies":
            if self.frame_type != "Help":
                #Help frame does not have a left frame.
                self.build_browser_left(left_side) #Build left frame.
            self.build_generic_right(right_side) #Build right frame.
        else:
            #Build as "Top Movies" frame.
            self.build_top_left(left_side)
            self.build_top_right(right_side)

    def build_browser_left(self, left_side):
        '''Build left side frame for Browser frames'''
        left_side.grid_rowconfigure(3, weight=1)
        #search_label.
        search_label = tk.Label(left_side, text=self.frame_type+" Browser", font=self.main_bold_font, bg="#194570", fg="white")
        search_label.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="nwse")
        #search_field.
        self.search_field = tk.Entry(left_side, font=self.main_norm_font, relief="ridge")
        self.search_field.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="nwse", pady=2)
        #search_button.
        search_button = tk.Button(left_side, text="Search", font=self.alt_bold_font, command=self.search_pressed)
        search_button.grid(row=1, column=1, rowspan=1, columnspan=1, sticky="nwse", pady=2)
        #result_label.
        result_label = tk.Label(left_side, text="Search Results", font=self.main_bold_font, bg="#194570", fg="white")
        result_label.grid(row=2, column=0, rowspan=1, columnspan=2, sticky="nwse")
        #result_listbox.
        result_lb_frame = tk.Frame(left_side, padx=5, pady=5, relief="ridge", bg="#194570")
        self.result_listbox = tk.Listbox(result_lb_frame, font=self.alt_norm_font, height=1)
        self.result_listbox.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nswe")
        result_lb_frame.grid(row=3, column=0, rowspan=1, columnspan=2, sticky="nwse")
        result_lb_frame.grid_rowconfigure(0, weight=1)
        result_lb_frame.grid_columnconfigure(0, weight=1)
        #select_button.
        search_button = tk.Button(result_lb_frame, text="Select Result", font=self.alt_bold_font, command=self.select_pressed)
        search_button.grid(row=4, column=0, rowspan=1, columnspan=2, sticky="nwse", pady=2)
        #result_x_scrollbar.
        result_x_scrollbar = tk.Scrollbar(result_lb_frame, orient="horizontal")
        result_x_scrollbar.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="nswe")
        self.result_listbox.configure(xscrollcommand=result_x_scrollbar.set)
        result_x_scrollbar.configure(command=self.result_listbox.xview)
        #result_y_scrollbar.
        result_y_scrollbar = tk.Scrollbar(result_lb_frame)
        result_y_scrollbar.grid(row=0, column=1, rowspan=2, columnspan=1, sticky="nswe")
        self.result_listbox.configure(yscrollcommand=result_y_scrollbar.set)
        result_y_scrollbar.configure(command=self.result_listbox.yview)

    def build_generic_right(self, right_side):
        '''Build right side for Browser and Help frames.'''
        right_side.grid_rowconfigure(1, weight=1)
        #top_description_field frame.
        top_df_frame = tk.Frame(right_side, padx=0, pady=0, relief="groove", bg="#194570") 
        top_df_frame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nwse")
        top_df_frame.grid_columnconfigure(0, weight=1)
        top_df_frame.grid_rowconfigure(0, weight=1)
        #top_description_field.
        self.top_description_field = tk.Text(top_df_frame, font=self.alt_norm_font, width=10, height=1, relief="groove", wrap=tk.WORD)
        self.top_description_field.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nwse")
        #top_y_scrollbar.
        top_y_scrollbar = tk.Scrollbar(top_df_frame)
        top_y_scrollbar.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nswe")
        self.top_description_field.configure(yscrollcommand=top_y_scrollbar.set)
        top_y_scrollbar.configure(command=self.top_description_field.yview)
        #bottom_description_field frame.
        btm_df_frame = tk.Frame(right_side, padx=0, pady=0, relief="groove", bg="#194570") 
        btm_df_frame.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="nwse")
        btm_df_frame.grid_columnconfigure(0, weight=1)
        btm_df_frame.grid_rowconfigure(0, weight=1)
        #btm_description_field.
        self.btm_description_field = tk.Text(btm_df_frame, font=self.alt_norm_font, width=1, height=1, relief="groove", wrap=tk.WORD)
        self.btm_description_field.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nwse")
        self.btm_description_field.grid_columnconfigure(0, weight=1)
        self.btm_description_field.grid_rowconfigure(0, weight=1)
        #btm_y_scrollbar
        btm_y_scrollbar = tk.Scrollbar(btm_df_frame)
        btm_y_scrollbar.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nswe")
        self.btm_description_field.configure(yscrollcommand=btm_y_scrollbar.set)
        btm_y_scrollbar.configure(command=self.btm_description_field.yview)
        #btm and top fonts.
        self.top_description_field.tag_configure("maintitle", font=("Verdana", 20, "bold"))
        self.top_description_field.tag_configure("subtitle", font=("Verdana", 16, "bold"))
        self.btm_description_field.tag_configure("maintitle", font=("Verdana", 20, "bold"))
        self.btm_description_field.tag_configure("subtitle", font=("Verdana", 16, "bold"))
        #Set up image if it is help.
        if self.frame_type == "Help":
            self.help_update()
            #displayed_image.
            self.displayed_image = tk.Canvas(right_side, relief="groove", width=400, height=400, bg="white")
            self.displayed_image.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nwse")
            #display profile image.
            self.img = Image.generate_profile_image()
            self.displayed_image.create_image(0, 0, image=self.img, anchor="nw")
        else:
            #displayed_image.
            self.displayed_image = tk.Canvas(right_side, relief="groove", width=260, height=390, bg="white")
            self.displayed_image.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nwse")
        #Disable description texts.
        self.top_description_field.config(state="disabled")
        self.btm_description_field.config(state="disabled")

    def build_top_left(self, left_side):
        '''Build left side frame for Top Movies frame.'''
        left_side.grid_rowconfigure(5, weight=1)
        #top_label.
        search_label = tk.Label(left_side, text="Click one of the buttons below\nfor their respective lists", font=self.main_bold_font, bg="#194570", fg="white")
        search_label.grid(row=0, column=0, rowspan=1, columnspan=1, pady=10, sticky="nwse")
        #popular_button.
        popular_button = tk.Button(left_side, text="Top Popular Movies", font=self.alt_bold_font, command=self.get_top_popular)
        popular_button.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="ew", pady=2)
        #top_rated_button.
        top_rated_button = tk.Button(left_side, text="Top Rated Movies", font=self.alt_bold_font, command=self.get_top_rated)
        top_rated_button.grid(row=2, column=0, rowspan=1, columnspan=1, sticky="ew", pady=2)
        #upcoming_button.
        upcoming_button = tk.Button(left_side, text="Top Upcoming Movies", font=self.alt_bold_font, command=self.get_top_upcoming)
        upcoming_button.grid(row=3, column=0, rowspan=1, columnspan=1, sticky="ew", pady=2)
        #Desc_label
        Desc_label = tk.Label(left_side, text="The format is as follows:", font=self.main_bold_font, bg="#194570", fg="white")
        Desc_label.grid(row=4, column=0, rowspan=1, columnspan=1, pady=10, sticky="nwse")
        #movies_listbox.
        left_movies_frame = tk.Frame(left_side, padx=5, pady=5, relief="ridge", bg="#194570")
        self.left_txt = tk.Text(left_movies_frame, font=self.alt_norm_font, height=1,width=1)
        self.left_txt.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nswe")
        left_movies_frame.grid(row=5, column=0, rowspan=1, columnspan=1, sticky="nwse")
        left_movies_frame.grid_rowconfigure(0, weight=1)
        left_movies_frame.grid_columnconfigure(0, weight=1)
        self.left_txt.tag_configure("subtitle", font=("Verdana", 16, "bold"))
        self.left_txt.insert("end", "Movie Name", "subtitle")
        self.left_txt.insert("end", " (Year Released) -> ID")
        self.left_txt.insert("end", "\n\n\n\n Thank you for using the top movie browser, enjoy!")
        self.left_txt.config(state="disabled")

    def build_top_right(self, right_side):
        '''Build right side for top movies frame'''
        right_side.grid_rowconfigure(0, weight=1)
        #right_txt_frame
        right_txt_frame = tk.Frame(right_side, padx=0, pady=0, relief="groove", bg="#194570") 
        right_txt_frame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nwse")
        right_txt_frame.grid_columnconfigure(0, weight=1)
        right_txt_frame.grid_rowconfigure(0, weight=1)
        #right_top_txt.
        self.right_top_txt = tk.Text(right_txt_frame, font=self.alt_norm_font, width=10, height=1, relief="groove")
        self.right_top_txt.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nwse")
        #top_y_scrollbar.
        right_y_scrollbar = tk.Scrollbar(right_txt_frame)
        right_y_scrollbar.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nswe")
        self.right_top_txt.configure(yscrollcommand=right_y_scrollbar.set)
        right_y_scrollbar.configure(command=self.right_top_txt.yview)
        self.right_top_txt.tag_configure("subtitle", font=("Verdana", 16, "bold"))

    def search(self, search_query):
        '''Perform a Query for data. Return dictionary from JSON.'''
        data = {} #data is a dictionary, parsed from JSON from the database.
        #If current search is not equal to last search.. then search; otherwise do not.
        if(search_query!= self.last_query): 
            #Update last query as the current query.
            self.last_query = search_query
            try: #Exception will occur if user searches for an ID that does not exist.
                    #If the query is numeric, they are searching for an ID number.
                if search_query.isnumeric():
                    #Enable fields for input.
                    self.top_description_field.config(state="normal")
                    self.btm_description_field.config(state="normal")
                    #Perform a search for ID, based on type of frame.
                    #Then, update the frame given the results.
                    if self.frame_type == "Movie":
                        data = self.database.get_movie_details(search_query)
                        self.movie_update(data)
                    elif self.frame_type == "TV Show":
                        data = self.database.get_tv_details(search_query)
                        self.tv_update(data)
                    else:
                        data = self.database.get_person_details(search_query)
                        self.person_update(data)
                else:
                    #If query is not numeric, the user will have to identify the
                    #specific movie they are looking for.
                    data = self.database.get_id_list(self.frame_type, search_query)
                    self.update_left_frame(data) #Update the selection field.
                #Disable fields so they cannot be changed.
                self.top_description_field.config(state="disabled")
                self.btm_description_field.config(state="disabled")
            except:
                #If user searches for ID that does not exist, this exception will be thrown.
                self.top_description_field.delete(1.0, "end")
                self.displayed_image.delete("all") #Wipe image from canvas.
                #Construct error message, then display it to user.
                err = "The id enetered does not match any given %s." %(self.frame_type)
                self.top_description_field.insert("end", err, "subtitle")
                self.top_description_field.config(state="disabled")
                self.btm_description_field.config(state="disabled")

    def update_left_frame(self, data):
        '''Updates the left frame with results from a search query.'''
        self.search_results = {}
        self.result_listbox.delete(0,"end") #Clear previous results.
        #Fill listbox in a different way depending on the type of search.
        for i,result in enumerate(data["results"]):
            if self.frame_type == "Movie":
                year = self.parse_year(result["release_date"])
                item = ("%s (%s) " %(result["title"], year))
                self.search_results[i] = result["id"]
            elif self.frame_type == "TV Show":
                year = self.parse_year(result["first_air_date"])
                item = ("%s (%s) " %(result["name"], year))
                self.search_results[i] = result["id"]
            else:
                #if frame_type == "Person"
                try:
                    item = ("%s (Known For: %s) " %(result["name"], result["known_for"][0]["title"]))
                    self.search_results[i] = result["id"]
                except:
                    #If no "known for" movies exist, just display name.
                    item = (result["name"])
                    self.search_results[i] = result["id"]
            #Insert each item into the listbox.
            self.result_listbox.insert("end", item)

    def movie_update(self, data):
        '''
        Update the movie frame if a movie has been specifically selected.
        '''  
        #Wipe description fields.
        self.top_description_field.delete(1.0, "end") 
        self.btm_description_field.delete(1.0, "end") 
        #Generate variables for all possible relevant data.
        #title
        title = "%s" %(data["title"])
        #tagline
        tagline = "%s" %(data["tagline"])
        #genres
        genres = self.parse_genres(data["genres"])
        #release_date
        release_date = self.parse_date(data["release_date"])
        #runtime
        runtime = self.parse_runtime(data["runtime"])
        #rating
        rating = ""
        if data["vote_average"] != 0 and data["vote_count"] != 0:
            rating = "%s/10 rating from %s votes." %(data["vote_average"],data["vote_count"])
        #homepage
        homepage = "%s" %(data["homepage"])
        #imdbpage
        imdbpage = "http://www.imdb.com/title/%s" %(data["imdb_id"])
        #budget
        budget = ("${0:,}".format(data["budget"]))
        #revenue
        revenue = ("${0:,}".format(data["revenue"]))
        #credits
        noteable_actors = self.parse_actors(data["credits"]["cast"])
        #plot_summary
        plot_summary = data["overview"]
        #similar_films
        similar_films = self.parse_films(data["similar"]["results"])
        #Posting to decription fields. (Only posts data if it exists)
        #title
        self.top_description_field.insert("end", title, "maintitle")
        #tagline
        if tagline != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Tagline\n", "subtitle")
            self.top_description_field.insert("end", tagline)
        #genres
        if genres != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Genres\n", "subtitle")
            self.top_description_field.insert("end", genres)
        #release_date
        if release_date != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Release Date\n", "subtitle")
            self.top_description_field.insert("end", release_date)
        #runtime
        if runtime != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Runtime\n", "subtitle")
            self.top_description_field.insert("end", runtime)
        #rating
        if rating != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Rating\n", "subtitle")
            self.top_description_field.insert("end", rating)
        #budget
        if budget != "$0":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Budget\n", "subtitle")
            self.top_description_field.insert("end", budget)
        #revenue
        if revenue != "$0":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Revenue\n", "subtitle")
            self.top_description_field.insert("end", revenue)
        #credits
        if noteable_actors != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Noteable Actors\n", "subtitle")
            self.top_description_field.insert("end", noteable_actors)
        #homepage
        if homepage != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Home Page\n", "subtitle")
            self.top_description_field.insert("end", homepage)
        #imdbpage
        if imdbpage != "http://www.imdb.com/title/":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "IMDB Page\n", "subtitle")
            self.top_description_field.insert("end", imdbpage)
        #plot_summary
        if plot_summary != "":
            self.btm_description_field.insert("end", "Plot\n", "subtitle")
            self.btm_description_field.insert("end", plot_summary)
        if similar_films != "":
            self.btm_description_field.insert("end", "\n\n")
            self.btm_description_field.insert("end", "Similar Films\n", "subtitle")
            self.btm_description_field.insert("end", similar_films)
        #Generate Image
        try:
            #Try to show image, if no image exists to be shown then exception is thrown.
            img_path = Image.find_suitable_image(data["images"]["posters"])
            self.img = Image.generate_260x390_image(img_path)
            self.displayed_image.create_image(0, 0, image=self.img, anchor="nw")
        except: #No images.
            self.displayed_image.delete("all")

    def tv_update(self, data):
        '''
        Update the TV show frame if a movie has been specifically selected.
        '''  
        #Wipe description fields.
        self.top_description_field.delete(1.0, "end") 
        self.btm_description_field.delete(1.0, "end") 
        #Generate variables for all possible relevant data.
        #name
        name = "%s" %(data["name"])
        #release_date
        release_date = self.parse_date(data["first_air_date"])
        #genres
        genres = self.parse_genres(data["genres"])
        #seasons
        seasons = data["number_of_seasons"] 
        #episodes
        episodes = data["number_of_episodes"]
        #avg_runtime (Must be calculated)
        avg_runtime = 0
        for i,episode_length in enumerate(data["episode_run_time"]):
            avg_runtime = avg_runtime + episode_length
            if i+1 == len(data["episode_run_time"]):
                avg_runtime = avg_runtime / (i+1)
        runtime = self.parse_runtime(avg_runtime)
        #status (Informs user on year ended if it is finished)
        status = data["status"]
        if status == "Ended":
            try:
                year = data["last_air_date"].split("-")[0]
                if year != "":
                    status = "%s (Finished in %s)" %(status, year)
            except:
                #If last_air_date does not exist, don't return end year.
                status = "Ended"
        #show_type
        show_type = data["type"]
        #rating
        rating = ""
        if data["vote_average"] != 0 and data["vote_count"] != 0:
            rating = "%s/10 rating from %s votes." %(data["vote_average"],data["vote_count"])
        #homepage
        homepage = "%s" %(data["homepage"])
        #credits
        noteable_actors = self.parse_actors(data["credits"]["cast"])
        #overview
        overview = data["overview"]
        #similar_shows
        similar_shows = self.parse_shows(data["similar"]["results"])
        #Posting to decription fields. (Only posts data if it exists)
        #name
        self.top_description_field.insert("end", name, "maintitle")
        #release_date
        if release_date != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "First Aired Date\n", "subtitle")
            self.top_description_field.insert("end", release_date)
        #genres
        if genres != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Genres\n", "subtitle")
            self.top_description_field.insert("end", genres)
        #seasons
        if seasons != 0:
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Number of Seasons\n", "subtitle")
            self.top_description_field.insert("end", seasons)
        #episodes
        if episodes != 0:
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Number of Episodes\n", "subtitle")
            self.top_description_field.insert("end", episodes)
        #runtime
        if runtime != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Average Runtime\n", "subtitle")
            self.top_description_field.insert("end", runtime)
        #status
        if status != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Status\n", "subtitle")
            self.top_description_field.insert("end", status)
        #show_type
        if show_type != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Show Type\n", "subtitle")
            self.top_description_field.insert("end", show_type)
        #rating
        if rating != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Rating\n", "subtitle")
            self.top_description_field.insert("end", rating)
        #credits
        if noteable_actors != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Noteable Actors\n", "subtitle")
            self.top_description_field.insert("end", noteable_actors)
        #homepage
        if homepage != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Home Page\n", "subtitle")
            self.top_description_field.insert("end", homepage)
        #overview
        if overview != "":
            self.btm_description_field.insert("end", "Overview\n", "subtitle")
            self.btm_description_field.insert("end", overview)
        if similar_shows != "":
            self.btm_description_field.insert("end", "\n\n")
            self.btm_description_field.insert("end", "Similar Shows\n", "subtitle")
            self.btm_description_field.insert("end", similar_shows)
        #Generate image.
        try:
            #Try to show image, if no image exists to be shown then exception is thrown.
            img_path = Image.find_suitable_image(data["images"]["posters"])
            self.img = Image.generate_260x390_image(img_path)
            self.displayed_image.create_image(0, 0, image=self.img, anchor="nw")
        except: #No images.
            self.displayed_image.delete("all")

    def person_update(self, data):
        '''
        Update the Person frame if a movie has been specifically selected.
        '''  
        self.top_description_field.delete(1.0, "end") #Should delete everything.
        self.btm_description_field.delete(1.0, "end") #Should delete everything.
        #Generate text for all.
        #name
        name = "%s" %(data["name"])
        #gender --> 0 = undefined, 1 = female, 2 = male.
        gender = str(data["gender"])
        if gender == "1":
            gender = "Female"
        elif gender == "2":
            gender = "Male"
        #date_of_birth (May not exist in database)
        try:
            date_of_birth = self.parse_date(data["birthday"]) 
        except:
            #If does not exist, define as null.
            date_of_birth = ""
        #place_of_birth (May not exist in database)
        try:
            place_of_birth = data["place_of_birth"]
        except:
            #If does not exist, define as null.
            place_of_birth = ""
        #Date of death. (May not exist in database)
        try:
            date_of_death = self.parse_date(data["deathday"]) 
        except:
            #If does not exist, define as null.
            date_of_death = ""
        #social_media. May or may not exist.
        #Returns valid ID, Null or "" depending. 
        facebook_id = data["external_ids"]["facebook_id"]
        twitter_id = data["external_ids"]["twitter_id"]
        instagram_id = data["external_ids"]["instagram_id"]
        #imdbpage
        imdbpage = "http://www.imdb.com/title/%s" %(data["imdb_id"])
        #biography
        biography = data["biography"]
        #known_for_movies
        known_for_movies = self.parse_films(data["movie_credits"]["cast"])
        #known_for_tv
        known_for_tv = self.parse_shows(data["tv_credits"]["cast"])
        #Posting to text.
        #name
        self.top_description_field.insert("end", name, "maintitle")
        #gender
        if gender != "0":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Gender\n", "subtitle")
            self.top_description_field.insert("end", gender)
        #date_of_birth
        if date_of_birth != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Date of Birth\n", "subtitle")
            self.top_description_field.insert("end", date_of_birth)
        #place_of_birth
        if place_of_birth != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Place of Birth\n", "subtitle")
            self.top_description_field.insert("end", place_of_birth)
        #date_of_birth
        if date_of_death != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Date of Death\n", "subtitle")
            self.top_description_field.insert("end", date_of_death)
        #Social Media
        #facebook_id
        if facebook_id != None and facebook_id != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Facebook ID\n", "subtitle")
            self.top_description_field.insert("end", facebook_id)
        #twitter_id
        if twitter_id != None and twitter_id != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Twitter ID\n", "subtitle")
            self.top_description_field.insert("end", twitter_id)
        #instagram_id
        if instagram_id != None and instagram_id != "":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "Instagram ID\n", "subtitle")
            self.top_description_field.insert("end", instagram_id)
        #imdbpage
        if imdbpage != "http://www.imdb.com/title/":
            self.top_description_field.insert("end", "\n\n")
            self.top_description_field.insert("end", "IMDB Page\n", "subtitle")
            self.top_description_field.insert("end", imdbpage)
        #overview
        if biography != "":
            self.btm_description_field.insert("end", "Overview\n", "subtitle")
            self.btm_description_field.insert("end", biography)
        if known_for_movies != "":
            self.btm_description_field.insert("end", "\n\n")
            self.btm_description_field.insert("end", "Popular Movies Starred In\n", "subtitle")
            self.btm_description_field.insert("end", known_for_movies)
        if known_for_tv != "":
            self.btm_description_field.insert("end", "\n\n")
            self.btm_description_field.insert("end", "Popular TV Shows Starred In\n", "subtitle")
            self.btm_description_field.insert("end", known_for_tv)
        #Generate image.
        try:
            #Try to show image, if no image exists to be shown then exception is thrown.
            img_path = Image.find_suitable_image(data["images"]["profiles"])
            self.img = Image.generate_260x390_image(img_path)
            self.displayed_image.create_image(0, 0, image=self.img, anchor="nw")
        except: #No images.
            self.displayed_image.delete("all")

    def help_update(self):
        '''
        Update the help frame.
        '''  
        #Posting to text.
        #name
        self.top_description_field.insert("end", "About The Author:\n", "subtitle")
        self.top_description_field.insert("end", "Mitchell Timothy Marino", "maintitle")
        #date_of_birth
        self.top_description_field.insert("end", "\n\n")
        self.top_description_field.insert("end", "About Mitchell\n", "subtitle")
        about_mitchell = ("Mitchell has had a deep interest in technology ever since he was young."
                    " He aspires to some day lead a meaningful career in the field of technology and"
                    " develop himself as a person along the way.")
        self.top_description_field.insert("end", about_mitchell)
        #date of birth
        self.top_description_field.insert("end", "\n\n")
        self.top_description_field.insert("end", "Date of Birth\n", "subtitle")
        self.top_description_field.insert("end", "February 28th, 1997")
        #home town
        self.top_description_field.insert("end", "\n\n")
        self.top_description_field.insert("end", "Home Town\n", "subtitle")
        self.top_description_field.insert("end", "Markham, Ontario")
        #school
        self.top_description_field.insert("end", "\n\n")
        self.top_description_field.insert("end", "School\n", "subtitle")
        self.top_description_field.insert("end", "Wilfrid Laurier University")
        #program
        self.top_description_field.insert("end", "\n\n")
        self.top_description_field.insert("end", "Program\n", "subtitle")
        self.top_description_field.insert("end", "Honours Computer Science, BSc")
        #how_to_use
        self.btm_description_field.insert("end", "How To Use The Program\n", "subtitle")
        #String which describes how to use the program!
        how_to_use = ("On the menu bar, you should see a button that says %s. If you press it,"
                        " then there will be a drop down list which well allow you to choose an interface"
                        " from a list of interfaces the program supports. You can search for movies, tv shows, and"
                        " people. This can be done by searching for the name of what you are searching for in the"
                        " search bar, and then pressing the %s button. After that, all the results will pop up in the"
                        " search results pane below. Click on whichever result you would like to access and cick select."
                        " A collection of information about the item you serached for will appear on the right hand side, along"
                        " with a photo.\n\nNOTE: \nYou can also search for an item by its TMDb (The Movie Database) ID! For example,"
                        " searching '597' will display the movie 'Titanic' because 597 is the TMDb ID for Titanic!"
                        " \n\nThe Movie Database (TMDb) is the source of all data obtained by this program!"
                        % ('"Search"', "'Select'"))
        #Update field with instructions.
        self.btm_description_field.insert("end", how_to_use)

    def get_top_popular(self):
        '''
        Obtain a list of top popular movies,
        then output it to the frame.
        '''  
        if self.last_query != "popular":
            self.last_query = "popular"
            self.right_top_txt.config(state="normal")
            self.right_top_txt.delete(1.0,"end")
            data = {}
            self.search_results = {}
            #Query pages 1 - 20 in the database, and update the textfield.
            for i in range(1,21):
                data = self.database.get_popular_movies(i)
                for j, movie in enumerate(data["results"]):
                    self.search_results[i+j] = movie["id"]
                    self.right_top_txt.insert("end", "%s " %(movie["title"]), "subtitle")
                    self.right_top_txt.insert("end", "(%s) -> %s\n" %(movie["release_date"].split("-")[0], movie["id"]))
            self.right_top_txt.config(state="disabled")

    def get_top_rated(self):
        '''
        Obtain a list of top rated movies,
        then output it to the frame.
        ''' 
        if self.last_query != "rated":
            self.last_query = "rated"
            self.right_top_txt.config(state="normal")
            self.right_top_txt.delete(1.0,"end")
            self.search_results = {}
            #Query pages 1 - 20 in the database, and update the textfield.
            for i in range(1,21):
                data = self.database.get_top_movies(i)
                for j, movie in enumerate(data["results"]):
                    self.search_results[i+j] = movie["id"]
                    self.right_top_txt.insert("end", "%s " %(movie["title"]), "subtitle")
                    self.right_top_txt.insert("end", "(%s) -> %s\n" %(movie["release_date"].split("-")[0], movie["id"]))
            self.right_top_txt.config(state="disabled")

    def get_top_upcoming(self):
        '''
        Obtain a list of top upcoming movies,
        then output it to the frame.
        '''
        if self.last_query != "upcoming":
            self.last_query = "upcoming"
            self.right_top_txt.config(state="normal")
            self.right_top_txt.delete(1.0,"end")
            data = {}
            self.search_results = {}
            #Query pages 1 - 20 in the database, and update the textfield.
            for i in range(1,21):
                data = self.database.get_upcoming_movies(i)
                for j, movie in enumerate(data["results"]):
                    self.search_results[i+j] = movie["id"]
                    self.right_top_txt.insert("end", "%s " %(movie["title"]), "subtitle")
                    self.right_top_txt.insert("end", "(%s) -> %s\n" %(movie["release_date"].split("-")[0], movie["id"]))
            self.right_top_txt.config(state="disabled")

    def parse_year(self, date_string):
        '''
        Input: Date string in format (yyyy-mm-dd)
        Output: Year
        '''
        year = ""
        try:
            #Isolate the year in the text and return it.
            year = date_string.split("-")[0]
            if year == "":
                year = "Year unknown"
        except:
            #If date was "", return "Year Unknown".
            year = "Year unknown"
        return year

    def parse_date(self, date_string):
        '''
        Input: Date string in format yyyy-mm-dd
        Output: Date in format (month_name dd, yyyy)
        '''
        month = ["January", "February", "March", "April", "May", "June", "July",
                    "August", "September", "October", "November", "December"]
        date = ""
        try:
            #Create the date using the month array and isolating year / month / day.
            date_split = date_string.split("-")
            date = "%s %s, %s" %(month[int(date_split[1])-1], date_split[2], date_split[0])
        except:
            #If date was "", return "Year Unknown".
            date = ""
        return date

    def parse_runtime(self, runtime):
        '''
        Input: Number of minutes.
        Output: Duration in format of n hours, n minutes.
        '''
        runtime = ""
        try:
            #Attempt to create the duration in nicer format.
            hours_mins = lambda rt: (int(rt/60), int(rt%60))
            hours, mins = hours_mins(runtime)
            if hours > 1:
                runtime = "%d Hours " %(hours)
            elif hours == 1:
                runtime = "%d Hour " %(hours)
            if mins > 1:
                runtime = runtime + "%d Minutes" %(mins)
            elif mins == 1:
                runtime = runtime + "%d Minute" %(mins)
        except:
            #If error occurs, runtime is not known.
            runtime = ""
        return runtime
        
    def parse_actors(self, actors):
        '''
        Input: Dictionary of actors.
        Output: String of actors.
        '''
        noteable_actors = ""
        for i,person in enumerate(actors):
            noteable_actors = "%s%s" %(noteable_actors, person["name"])
            if i < len(actors)-1 and i < 5:
                noteable_actors = noteable_actors + "\n"
            else:
                break
        return noteable_actors

    def parse_films(self, films):
        '''
        Input: Dictionary of films.
        Output: String of films.
        '''
        film_string = ""
        for i,result in enumerate(films):
            year = self.parse_year(result["release_date"])
            film_string = "%s%s (%s)" %(film_string, result["title"], year)
            if i < len(films)-1 and i < 8:
                film_string = film_string + "\n"
            else:
                break
        return film_string

    def parse_shows(self, shows):
        '''
        Input: Dictionary of shows.
        Output: String of shows.
        '''
        show_string = ""
        for i,result in enumerate(shows):
            year = self.parse_year(result["first_air_date"])
            show_string = "%s%s (%s)" %(show_string, result["name"], year)
            if i < len(shows)-1 and i < 8:
                show_string = show_string + "\n"
            else:
                break
        return show_string

    def parse_genres(self, genre_list):
        '''
        Input: List of genres.
        Output: String of genres.
        '''
        genres = ""
        for i,genre in enumerate(genre_list):
                genres = genres + genre["name"]
                if i < len(genre_list)-1:
                    genres = genres + ", "
        return genres

    def select_pressed(self):
        '''When select button is pressed, run a search'''
        search_query = str(self.search_results[self.result_listbox.curselection()[0]])
        self.search(search_query)

    def search_pressed(self):
        '''When search button is pressed, run a search'''
        search_query = self.search_field.get()
        self.search(search_query)


