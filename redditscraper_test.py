import requests
import time
import csv
from bs4 import BeautifulSoup as bs
import random
import re
from find_posts import find_posts  # Import function to get post URLs

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
            # Skip non-text content (images, videos)
            if any(post_url.endswith(ext) for ext in ['.jpg', '.png', '.gif', '.mp4', '.webm', '.jpeg']):
                print(f"Skipping media link: {post_url}")
                continue

            time.sleep(random.uniform(sleep_time, sleep_time + 0.1))  # Randomized delay for safety
            
            try:
                response = requests.get(post_url, headers=headers, timeout=10)  # Added timeout
                if response.status_code != 200:
                    print(f"Failed to fetch {post_url}: {response.status_code}")
                    continue

                soup = bs(response.text, "html.parser")

                # Extract post details with better error handling
                title_tag = soup.find("h1")
                title = title_tag.text.strip() if title_tag else "No Title"

                body_tag = soup.find("div", class_="md")
                body = body_tag.text.strip() if body_tag else "No Body"

                combined_text = title + " " + body

                user_tag = soup.find("a", class_=re.compile("author"))
                user = user_tag.text if user_tag else "Unknown"

                timestamp_tag = soup.find("time")
                timestamp = timestamp_tag.get("datetime", "Unknown") if timestamp_tag else "Unknown"

                score_tag = soup.find("div", class_="score unvoted")
                post_score = score_tag.text if score_tag else "Unknown"

                comments_count_tag = soup.find("span", class_=re.compile("comments"))
                comments_count = comments_count_tag.text if comments_count_tag else "0"

            except Exception as e:
                print(f"Error parsing {post_url}: {e}")
                continue

            # Extract comments safely
            comments_section = soup.find("div", class_="sitetable nestedlisting")
            comments = comments_section.find_all("div", class_="entry unvoted") if comments_section else []

            for comment in comments[:max_comments]:
                try:
                    comment_user_tag = comment.find("a", class_=re.compile("author"))
                    comment_user = comment_user_tag.text if comment_user_tag else "Anonymous"

                    comment_body_tag = comment.find("div", class_="md")
                    comment_body = comment_body_tag.text.strip() if comment_body_tag else "No Comment"

                    comment_combined_text = title + " " + comment_body

                    comment_score_tag = comment.find("span", class_="score unvoted")
                    comment_score = comment_score_tag.text if comment_score_tag else "Unknown"

                    comment_timestamp_tag = comment.find("time")
                    comment_timestamp = comment_timestamp_tag.get("datetime", "Unknown") if comment_timestamp_tag else "Unknown"

                except:
                    continue
                
                writer.writerow([timestamp, user, title, body, combined_text, post_score, comments_count, post_url, comment_user, comment_body, comment_combined_text, comment_score, comment_timestamp])

            print(f"Scraped: {post_url}")

    print("Scraping complete! Data saved in", csv_filename)

# Example usage
if __name__ == "__main__":
    subreddit = "nursing"  # Replace with the desired subreddit
    num_posts = 100  # Number of posts to fetch
    post_urls = find_posts(num_posts, subreddit)

    if post_urls:
        scrape_reddit_posts(post_urls, "reddit_data.csv")
    else:
        print("No posts found.")
