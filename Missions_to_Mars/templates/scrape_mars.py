from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd 
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    mars_data = {}

    # Visit mars news
    news_url = 'https://mars.nasa.gov/news'
    browser.visit(news_url)

    time.sleep(1)

    # Scrape page into Soup
    news_html = browser.html
    soup = bs(news_html, 'html.parser')

    # Get the latest news title and paragraph
    news_info = soup.select_one('ul.item_list li.slide')
    news_title = news_info.find('div', class_ = 'content_title').text
    news_p = news_info.find(class_ = 'rollover_description_inner').text


    print(news_title)
    print(news_p)
    # Close the browser after scraping
    browser.quit()
    
    
    #  Visit mars space image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    time.sleep(1)

    # Scrape page into Soup
    image_html = browser.html
    soup = bs(image_html, 'html.parser')


    # Find the src for the image
    image_path = soup.find('section', class_ = 'primary_media_feature').find('article').get('style')
    relative_image_path = image_path.split(sep = "'")[1]
    featured_image_url = image_url.replace('/spaceimages/?search=&category=Mars', relative_image_path)

    print(featured_image_url)
    # Close the browser after scraping
    browser.quit()



    # Visit mars weather 
    weather_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(weather_url)
    soup = bs(response.text, 'html.parser')
    
    mars_weather_text = soup.find('div', class_ = 'js-tweet-text-container').text
    mars_weather_split = mars_weather_text.replace('InSight', '').split('\n')
    mars_weather_split_1 = mars_weather_split[0].split(')')
    mars_weather_split_3 = mars_weather_split[2].split('pic')
    mars_weather = '),'.join(mars_weather_split_1) + ' ' + mars_weather_split_3[0]

    print(mars_weather)
    # Visit mars facts
    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)
    df = table[0]
    df.rows = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons', 'Orbit Distance', 'Orbit Period', 'Surface Temperature', 'First Record', 'Recorded By']
    df.columns = ['Description', 'Values']
    df.set_index('Description', inplace = True)
    html_table = df.to_html()

    print(html_table)
    # Visit mars hemisphere
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(hemisphere_url)
    soup = bs(response.text, 'html.parser')
    items = soup.find_all('div', class_ = 'item')
    hemisphere_image_url = []
    for item in items:
        image_url = hemisphere_url.replace('/search/results?q=hemisphere+enhanced&k1=target&v1=Mars',item.find('img').get('src'))
        title = item.find('h3').text
        hemisphere_image_url.append({'title': title, 'image_url': image_url})


    print(hemisphere_image_url)

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title
    }

    # Return results
    return mars_data
