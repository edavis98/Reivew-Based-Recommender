#import packages
from selenium import webdriver
import time
import pandas as pd
import numpy as np
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.chrome.options import Options


#function for requesting number of reviews
def get_album_reviews(artist, album, num_reviews, verbose):
    '''
    Gathers reviews, users, ratings, and album for a specific album as scraped from rateyourmusic.com

    Args:
        artist (string)
        album (string)
        num_reviews (integer)
        verbose (boolean)

    Returns:
        reviews (list)
        albums (list)
        ratings (list)
        users (list)
    '''

    #set up adblock location
    path_to_extension = r'C:/Users/evanm/BrainStation/Capstone_Final/adblock' # NEED TO CHANGE PATH TO WHERE YOU HAVE THE 'adblock' FOLDER SAVED
    chrome_options = Options()
    chrome_options.add_argument('load-extension=' + path_to_extension)

    #initialize chrome driver w/ adblock
    driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)
    driver.create_options()
    driver.set_window_size(1120, 1000)

    #url to begin scraping from
    url = f'https://rateyourmusic.com/release/album/{artist}/{album}/reviews/1/'
    driver.get(url)
    
    #wait for browser to open
    time.sleep(2) # was originally 10 seconds
    
    #initialize lists
    reviews = []
    albums = []
    ratings = []
    users = []

    #while number of collected reviews does not equal number of requested reviews 
    while len(reviews) != num_reviews:

        #get review ids
        review_ids = driver.find_elements('xpath', './/div[@id="column_container_right"]//div[contains(@id,"reviews")]//div[contains(@id, "std")]')
        
        #for each review
        for ids in review_ids:

            #determine the location of the review
            location = ids.get_attribute('id')
            
            #xpath to specify review location
            xpath = './/div[@id="'
            xpath += str(location)
            xpath += '"]'
            
            #initialize variable to break while loop
            collected_successfully = False
        
            #runs until collected_successfully = True
            while not collected_successfully:

                #try to find items for scraping
                try:
                    
                    review = []
                    user = driver.find_element('xpath', '{}//div[contains(@class, "review_header")]//a[contains(@class, "user")]'.format(xpath)).text
                    review_loc = driver.find_elements('xpath', '{}//div[contains(@class, "body")]//span[contains(@class, "rendered")]'.format(xpath))
                    
                    #reviews are in list form so append
                    for value in review_loc:
                        review.append(value.text)
                    
                    #if rating exists record otherwise set to nan
                    try:
                        rating_loc = driver.find_element('xpath', '{}//div[contains(@class, "header")]//span[contains(@class, "rating")]/img[@width="90"]'.format(xpath))
                        rating = rating_loc.get_attribute("title")
                    except NoSuchElementException:
                        rating = np.nan
                        
                    #set true to break while loop
                    collected_successfully = True
                
                #if page hasn't loaded yet wait 2 seconds (was originally 5)
                except:
                    time.sleep(2)

            #append scraped information to reviews array
            reviews.append(review)
            albums.append(album)
            ratings.append(rating)
            users.append(user)
        
        #click next page
        try:
            driver.find_element('xpath', './/a[@class="navlinknext"]').click()
        
            time.sleep(1) # was originally 5 seconds
        
        #if on last page then break from if condition
        except NoSuchElementException:

            if len(reviews) == 0:
                reviews.append(np.nan)
                albums.append(album)
                ratings.append(np.nan)
                users.append(np.nan)
                print(f'URL/Reviews not found for {album} by {artist}')

            return reviews, albums, ratings, users
        
    #return requested reviews as a dataframe
    return reviews, albums, ratings, users