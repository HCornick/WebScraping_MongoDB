# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import pprint
import pymongo



# NASA Mars News
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later.

def scrape_all_mars():
    mars_dict = {}
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create a BeautifulSoup object
    soup = bs(response.text, 'html.parser')

    # Scrape site to find latest news title and paragraphs
    news_title = soup.find('div', class_ = "content_title").text
    news_paragraph = soup.find('div', class_='rollover_description_inner').text

    # Save title and paragraph in mars info dictionary
    mars_dict["news_title"] = news_title 
    mars_dict["news_paragraph"] = news_paragraph

    # JPL Mars Space Images - Featured Image
    # Visit the url for JPL Featured Space Image.
    # Use beautiful soup to navigate the site and find the image url for the current Featured Mars Image 
    # and assign the url string to a variable called featured_image_url.`

    # Visit the url for JPL's Featured Space Image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    response2 = requests.get(jpl_url)
    soup2 = bs(response2.text, 'html.parser')

    # Use beautiful soup to find the image url
    image = soup2.find('a', class_="button fancybox")
    url_piece = image["data-fancybox-href"]
    image_url = 'https://www.jpl.nasa.gov' + url_piece
    image_url = image_url.replace('medium', 'large')
    image_url = image_url.replace('ip', 'hires')

    # Save the featured image_url within mars info dictionary
    mars_dict["featured_image"] = image_url

    # Mars Weather
    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called mars_weather.

    # Collects most recent tweet from Mars weather twitter account
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    tweet_response = requests.get(twitter_url)
    weather_soup = bs(tweet_response.text, 'html.parser')
    mars_weather = weather_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather = mars_weather.split("Welcome",1)[0] 
    
    # Save the weather information within mars info dictionary
    mars_dict["mars_weather"] = mars_weather

    # Mars Facts
    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including 
    # Diameter, Mass, etc. Use Pandas to convert the data to a HTML table string.

    # Scrape the desired information from the url
    facts_url = "https://space-facts.com/mars/"
    mars_info = pd.read_html(facts_url)

    # Convert mars info list to a pandas dataframe
    mars_df = mars_info[0]
    mars_df.columns = ["description", "value"]
    mars_df.set_index("description", inplace=True)

    # Convert mars_df information to an html table
    mars_facts = mars_df.to_html()
    
    # Save the weather information within mars info dictionary
    mars_dict["mars_table"] = mars_facts

    # Mars Hemispheres
    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    # Click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. 
    # Use a Python dictionary to store the data using the keys img_url and title.
    # Append the dictionary with the image url string and the hemisphere title to a list. 
    # This list will contain one dictionary for each hemisphere.

    # Mars Hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/'
    hresponse = requests.get(hemisphere_url)
    hem_soup = bs(hresponse.text, 'html.parser')

    hem_image = hem_soup.find_all('a', class_="itemLink product-item")

    hem_images = []
    hem_piece = 'https://astrogeology.usgs.gov'
    for each in hem_image:
        hem_dict = {}
        string = each.text
        remove = string.find("Enhance")
        title = string[:remove]
        hem_dict["title"] = title
        
        hem_images.append(hem_dict)
        hem_url = hem_piece + each["href"]
        picresponse = requests.get(hem_url)
        img_soup = bs(picresponse.text, 'html.parser')
        pictures = img_soup.find_all('img', class_="wide-image")
        for picture in pictures:
            imgtext = picture["src"]
        hem_dict["img_url"] = hem_piece + imgtext
    
    # Save the hemisphere image information within mars info dictionary
    mars_dict["hemisphere_imgs"] = hem_images

    # Return the dictionary
    return mars_dict