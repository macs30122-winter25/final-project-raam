import requests                     
from bs4 import BeautifulSoup as bs 
import time

# River Wang

def find_posts(n, subreddit):
    '''
    Find posts within a subreddit posted between January 2019 and 
    January 2022 under the "top" section.

    Args:
        n (int): total number of posts to be searched (increments by 25)
        subreddit (str): name of the subreddit

    Returns: a list of all URLs to the posts within a subreddit
    '''
    counter = 0
    num_error = 0
    post_urls = []
    page_url = f"https://old.reddit.com/r/{subreddit}/top/?sort=top&t=all"
    time_frame = ['6 years ago', '5 years ago', '4 years ago', '3 years ago']

    headers = {"User-Agent": "Mozilla/5.0"}  # Avoid request blocking

    while counter <= n:
        response = requests.get(page_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch {page_url}, Status Code: {response.status_code}")
            break  # Stop if blocked
        if response.status_code != 429:
            num_error += 1
            error = True
        
        soup = bs(response.text, 'html.parser')
        found_posts = False  # Track if any posts are found

        for post in soup.find_all('div', class_="top-matter"):
            if post.find('time') and post.find('time').text in time_frame:
                url = post.find('a')['href']
                if url.startswith("/r/"):
                    url = "https://old.reddit.com" + url
                if 'redd' not in url:
                    continue
                post_urls.append(url)
                found_posts = True

        if not found_posts:
            print("No matching posts found on this page.")
            break  # Stop if no posts found
        
        # Find next button safely
        next_button = soup.find("span", class_="next-button")
        if next_button and next_button.find("a"):
            page_url = next_button.find("a")["href"]
        else:
            print("No next button found. Reached last page or blocked.")
            break  # Stop if there are no more pages

        counter += 25
        if num_error >= 2 and error:
            time.sleep(1.2)
        else:
            time.sleep(0.61)  # Respect rate limits
            num_error = 0
        
        error = False

    return post_urls
