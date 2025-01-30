import requests                     
from bs4 import BeautifulSoup as bs 
import time

def find_posts(n, subreddit):
    '''
    Find posts within a subreddit posted between January 2019 and 
    January 2022 under the "top" section.

    Args:
        n (int): total number of posts to be searched (increments by 25)
        subreddit (str): name of the subreddit

    Returns: a list of all urls to the posts within a subreddit
    '''
    counter = 0
    post_urls = []
    page_url = "https://old.reddit.com/r/{}/top/?sort=top&t=all".format(subreddit)
    time_frame = ['6 years ago', '5 years ago', '4 years ago', '3 years ago']
    while counter <= n:
        response = requests.get(page_url)
        soup = bs(response.text, 'html.parser')
        for post in soup.find_all('div', class_= "top-matter"):
            #if title.find('span').text == 'Code Blue Thread':
            if post.find('time').text in time_frame:
                url = post.find('a')['href']
                if url[:3] == "/r/":
                    url = "https://old.reddit.com" + url
                post_urls.append(url)
        page_url = soup.find("span", _class="next-button").find('a')['href']
        counter += 25
    
    return post_urls