'''
Name: Mitchell Marino
Date: 2018-01-10
Program: Data_Fetcher.py
Description: Used to Query TMDb's database for data using their online API.
'''

#Imports
import requests

#Decorator Function for making requests with TMDb class.
def request_JSON(url_creator):
    def wrapper(self, obj):
            url = url_creator(self,obj)
            req = requests.get(url)
            json_obj = req.json() #Parse the request from JSON into dictionary.
            return json_obj
    return wrapper

#Class used to generate URLs and obtain information from TMDb's online API.
class TMDb(object):

    #Constructor
    def __init__(self, debug=False, language='en'):
        self._base_url = 'http://api.themoviedb.org/3'
        self._api_key  = '3b408e256b7877671776f951ab2dcd52'
        self._language = language

    #--Get details on a movie--
    @request_JSON
    def get_movie_details(self, movie_id):
        '''Get movie's details from TMDb API.'''
        #Append query for images.
        append_to_response = ("&append_to_response=similar,credits,images&include_image_language=en,null")
        url = ("%s/movie/%s?api_key=%s&language=%s%s" 
               %(self._base_url, movie_id, self._api_key, self._language, append_to_response))  
        return url

    #--Get details on a tv show--
    @request_JSON
    def get_tv_details(self, tv_id):
        '''Get tv show's details from TMDb API.'''
        #Append query for images.
        append_to_response = ("&append_to_response=similar,credits,images&include_image_language=en,null")
        url = ("%s/tv/%s?api_key=%s&language=%s%s" 
               %(self._base_url, tv_id, self._api_key, self._language, append_to_response))
        return url

    #--Get details on a person--
    @request_JSON
    def get_person_details(self, person_id):
        '''Get person's details from TMDb API.'''
        #Append query for images.
        append_to_response = ("&append_to_response=movie_credits,tv_credits,external_ids,images&include_image_language=en,null")
        url = ("%s/person/%s?api_key=%s&language=%s%s" 
               %(self._base_url, person_id, self._api_key, self._language, append_to_response))
        return url

    #--Get most popular movies--
    @request_JSON
    def get_popular_movies(self, page):
        '''Get popular movies from TMDb API.'''
        #20 results per page.
        url = ("%s/movie/popular?api_key=%s&language=%s&page=%s" 
               %(self._base_url, self._api_key, self._language, page))
        return url

    #--Top rated movies--
    @request_JSON
    def get_top_movies(self, page):
        '''Get top movies from TMDb API.'''
        #20 results per page.
        url = ("%s/movie/top_rated?api_key=%s&language=%s&page=%s" 
               %(self._base_url, self._api_key, self._language, page))
        return url
    
    @request_JSON
    def get_upcoming_movies(self, page):
        '''Get upcoming movies from TMDb API.'''
        #20 results per page.
        url = ("%s/movie/upcoming?api_key=%s&language=%s&page=%s" 
               %(self._base_url, self._api_key, self._language, page))
        return url
    
    #Finding IDs of movie name, tv show name, or person name.
    def get_id_list(self, mode, query_str):
        '''
        Fetch the IDs relating to a query string from IMDb API.
        Will return a list with length >= 0 depending how many items match the description.
        '''
        query_str = query_str.replace(" ","%20") #Replace spaces with %20 for URL.
        if mode == "Movie":   
            #Searching for Movie.
            url = ("%s/search/movie?api_key=%s&language=%s&query=%s&page=1&include_adult=false" 
               %(self._base_url, self._api_key, self._language, query_str))
        elif mode == "TV Show": 
            #Searching for TV show.
            url = ("%s/search/tv?api_key=%s&language=%s&query=%s&page=1&include_adult=false" 
               %(self._base_url, self._api_key, self._language, query_str))
        else: 
            #Searching for Person.
            url = ("%s/search/person?api_key=%s&language=%s&query=%s&page=1&include_adult=false" 
               %(self._base_url, self._api_key, self._language, query_str))
        #Obtain data from TMDb.
        req = requests.get(url)
        #Parse the request from JSON into a dictionary.
        json_obj = req.json() 
        #Return dictionary.
        return json_obj