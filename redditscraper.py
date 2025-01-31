import requests
import time
import csv
from bs4 import BeautifulSoup as bs
import random
import re

def scrape_reddit_posts(post_urls, csv_filename, max_comments=50):
    """
    Scrapes details from Reddit posts and their comments.
    
    Args:
        post_urls (list): List of Reddit post URLs to scrape.
        csv_filename (str): Name of the output CSV file.
        max_comments (int): Maximum number of comments to extract per post.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    sleep_time = 0.61  # Adjusted sleep time to match requirement
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Username", "Post Title", "Post Body", "Combined Text", "Score", "Comments Count", "Post URL", "Comment Username", "Comment Body", "Comment Combined Text", "Comment Score", "Comment Timestamp"])
        
        for post_url in post_urls:
            time.sleep(random.uniform(sleep_time, sleep_time + 0.1))  # Randomized delay for safety
            response = requests.get(post_url, headers=headers)
            
            if response.status_code != 200:
                print(f"Failed to fetch {post_url}: {response.status_code}")
                continue
            
            soup = bs(response.text, "html.parser")
            
            try:
                title = soup.find("h1").text.strip()
                body = soup.find("div", class_="md").text.strip() if soup.find("div", class_="md") else ""
                combined_text = title + " " + body
                user = soup.find("a", class_=re.compile("author"))
                user = user.text if user else "Unknown"
                timestamp = soup.find("time").get("datetime", "Unknown")
                score = soup.find("div", class_="score unvoted")
                post_score = score.text if score else "Unknown"
                comments_count = soup.find("span", class_=re.compile("comments"))
                comments_count = comments_count.text if comments_count else "0"
            except Exception as e:
                print(f"Error parsing {post_url}: {e}")
                continue
            
            comments_section = soup.find("div", class_="sitetable nestedlisting")
            comments = comments_section.find_all("div", class_="entry unvoted") if comments_section else []
            
            for comment in comments[:max_comments]:
                try:
                    comment_user = comment.find("a", class_=re.compile("author"))
                    comment_user = comment_user.text if comment_user else "Anonymous"
                    comment_body = comment.find("div", class_="md").text.strip()
                    comment_combined_text = title + " " + comment_body
                    comment_score = comment.find("span", class_="score unvoted")
                    comment_score = comment_score.text if comment_score else "Unknown"
                    comment_timestamp = comment.find("time").get("datetime", "Unknown")
                except:
                    continue
                
                writer.writerow([timestamp, user, title, body, combined_text, post_score, comments_count, post_url, comment_user, comment_body, comment_combined_text, comment_score, comment_timestamp])
                
            print(f"Scraped: {post_url}")
    
    print("Scraping complete! Data saved in", csv_filename)

# Example usage (replace with actual post URLs from find_posts.py)
# post_urls = find_posts(100, "some_subreddit")
# scrape_reddit_posts(post_urls, "reddit_data.csv")
