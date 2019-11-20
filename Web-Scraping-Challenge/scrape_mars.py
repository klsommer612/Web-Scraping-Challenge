# Dependencies
from bs4 import BeautifulSoup as bs
from pprint import pprint
from splinter import Browser
from time import sleep
import pandas as pd

def scrape():

    # Windows executable path
    executable_path = {'executable_path': '/Users/klsom/Downloads/chromedriver'}
    b = Browser('chrome', **executable_path, headless=False)

    # Mac executable path
    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    # b = Browser('chrome', **executable_path, headless=False)

    news_title, news_p = mars_news(b)
    
    results = {
        'title': news_title,
        'paragraph': news_p,
        'image_URL': jpl_image(b),
        'weather': mars_weather_tweet(b),
        'facts': mars_facts(),
        'hemispheres': mars_hemis(b),
    }

    b.quit()
    return results

def mars_news(b):
    url = 'https://mars.nasa.gov/news/'
    b.visit(url)
    html = b.html
    mars_bs = bs(html, 'lxml')

    news_title = mars_bs.find('div', class_='content_title').text
    news_p = mars_bs.find('div', class_='article_teaser_body').text
    return news_title, news_p

def jpl_image(b):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    b.visit(url)

    b.click_link_by_partial_text('FULL IMAGE')
    sleep(1)
    b.click_link_by_partial_text('more info')

    html = b.html
    image_soup = bs(html, 'lxml')

    feat_img_url = image_soup.find('figure', class_='lede').a['href']
    feat_img_full_url = f'https://www.jpl.nasa.gov{feat_img_url}'
    return feat_img_full_url

def mars_weather_tweet(b):
    url = 'https://twitter.com/marswxreport?lang=en'
    b.visit(url)
    html = b.html
    tweet_soup = bs(html, 'lxml')
    
    first_tweet = tweet_soup.find('p', class_='TweetTextSize').text
    return first_tweet
    
def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Property', 'Value']
    df.set_index('Property', inplace=True)
    
    return df.to_html()
    
def mars_hemis(b):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    b.visit(url)
    
    html = b.html
    hemi_soup = bs(html, 'html.parser')

    hemi_strings = []
    links = hemi_soup.find_all('h3')
    
    for hemi in links:
        hemi_strings.append(hemi.text)

    hemisphere_image_urls = []

    # Loop through the hemisphere links to gather the images
    for hemi in hemi_strings:
        hemi_dict = {}
        
        b.click_link_by_partial_text(hemi)
        hemi_dict['img_url'] = b.find_by_text('Sample')['href']
        hemi_dict['title'] = hemi
        hemisphere_image_urls.append(hemi_dict)
        pprint(hemisphere_image_urls)
        
        b.click_link_by_partial_text('Back')
    
    return hemisphere_image_urls