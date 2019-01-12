#import dependencies 
import pandas as pd 
from bs4 import BeautifulSoup as bs 
from splinter import Browser
import time 

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_info ={}

    #NASA news scrape 
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    #scrape most recent article headline
    mars_info['news_title'] = soup.find('div', class_='content_title').get_text() 
    mars_info['news_p'] = soup.find('div', class_='rollover_description_inner').get_text() 

    
    #JPL image scrape 
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(1)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')
    feat_img = jpl_soup.find('a', class_='button fancybox')['data-fancybox-href']

    mars_info['featured_image_url'] = f'https://www.jpl.nasa.gov{feat_img}'


    #Mars Weather (Twitter)
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(1)
    weather_html = browser.html
    weather_soup = bs(weather_html, 'html.parser')

    mars_info['mars_weather'] = weather_soup.find('div', class_='js-tweet-text-container').get_text() 


    #Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    tables = pd.read_html(facts_url) 
    df = pd.DataFrame(tables[0])
    df.columns = ['Description', 'Value']
    mars_df = df.set_index('Description')

    mars_info['mars_facts'] = mars_df.to_html()


    return mars_info
