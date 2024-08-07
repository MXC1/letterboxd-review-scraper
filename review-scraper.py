import time
from bs4 import BeautifulSoup
import requests
import os
import pathlib
import argparse

if os.path.exists("E:\\Documents\\WebScraping\\review-scraper\\output.txt"):
    os.remove("E:\\Documents\\WebScraping\\review-scraper\\output.txt")
    
argParser = argparse.ArgumentParser(prog="Review Scraper",
                                 description="A simple tool to return pages of Letterboxd reviews in plaintext. Useful if you want to analyse those reviews e.g. using AI.",
                                 usage="review-scraper.py")

# Parse film argument
print("Enter the film you want to return reviews for.")
print("Must be the same as it is in the URL on Letterboxd.")
print("E.g: v-for-vendetta")

film=""
while film in (None,""):
    print("Film: ", end="")
    film = input()

    # Check film exists
    url = "https://letterboxd.com/film/" + film
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    errorMessage = doc.find("body", class_="error")
    if errorMessage is not None:
        print("That film does not exist.")
        film=None
    
# Parse pages argument
number_of_pages = ""
while not number_of_pages.isdigit():
        print("How many pages of reviews to return: ", end="")
        number_of_pages = input()
number_of_pages=int(number_of_pages)    
    
output_file_location = str(pathlib.Path().resolve()) + "\\" + film + "-" + str(number_of_pages) + ".txt"

print("Output file location: " + output_file_location)

for page in range(1,number_of_pages+1):
    url = "https://letterboxd.com/film/" + film + "/reviews/by/activity/page/" + str(page)
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    pageOfReviews = doc.find_all("div", class_="film-detail-content")
    
    if (len(pageOfReviews)==0):
        break
    
    print("Parsing page: " + str(page))
    
    for review in pageOfReviews:
        
        rating = review.find("span", class_="rating")
        reviewContent = review.find("div", class_="body-text")

        spoilerElement = reviewContent.find("p", class_="contains-spoilers")
        if spoilerElement is not None:
            spoilerElement.decompose()

        for data in reviewContent(['style', 'script']):
            data.decompose()

        with open(output_file_location, "a", encoding="utf-8") as output_file:
            if rating is not None:
                output_file.write(rating.string + "- ")
            else:
                output_file.write(" No Rating " + "- ")
            output_file.write(' '.join(reviewContent.stripped_strings))
            output_file.write("\n")
            
print("Done!")
input()