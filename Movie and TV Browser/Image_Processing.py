'''
Name: Mitchell Marino
Date: 2018-01-10
Program: Image_Processing.py
Description: Used to fetch images from the web and resize them to adequate dimensions.
'''

#Imports
from PIL import Image, ImageTk
import urllib.request
import io

def find_suitable_image(posters):
    '''
    Browse an array of posters, find one with suitable aspect ratio.
    If one with given aspect ratio cannot be found, return first poster in the array.
    '''
    for poster in posters:
        if poster["aspect_ratio"] == 0.6666666666666666:
            return poster["file_path"]
    return posters[0]["file_path"]

def generate_260x390_image(file_path):
    '''
    Resize an image to 260x390 to fit on the Canvas of the application.
    '''
    #Base url for tmdb photos.
    base_url = "http://image.tmdb.org/t/p/original"
    #Construct URL.
    url = "%s%s" %(base_url, file_path)
    #Open the image for use locally.
    with urllib.request.urlopen(url) as URL:
        img = io.BytesIO(URL.read())
        img = Image.open(img)
        #Resize image.
        img = img.resize((260,390), Image.ANTIALIAS)
        #Save as TKinter image for use by the canvas.
        photo = ImageTk.PhotoImage(img)
    return photo

def generate_profile_image():
    '''
    Pull my Linkedin photo from the web for use by the application's help page.
    My linkedin as of writing this can be found at: https://www.linkedin.com/in/mitchelltmarino/
    '''
    #Address of my Linkedin photo.
    url = ("https://media.licdn.com/mpr/mpr/shrinknp_400_400/AAEAAQAAAAAAAAaPAAAAJDQ5NmQwZGI3LWEyYjUtNDBjZi05NzVhLTdhZWYwOTU4MzkzZA.jpg")
    #Open the image for use locally.
    with urllib.request.urlopen(url) as URL:
        img = io.BytesIO(URL.read())
        img = Image.open(img)
        #Save as TKinter image for use by the canvas.
        photo = ImageTk.PhotoImage(img)
    return photo