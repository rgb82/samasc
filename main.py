import praw
import os
import requests
from datetime import datetime

# Define a class to represent a Reddit post
class RedditPost:
    def __init__(self, title, url, score, content, timestamp):
        self.title = title
        self.url = url
        self.score = score
        self.content = content
        self.timestamp = timestamp

    def to_html(self):
        return (f"<div class='post'>"
                f"<h1 class='title'>Title: {self.title}</h1>"
                f"<p class='url'><strong>URL:</strong> <a href='{self.url}'>{self.url}</a></p>"
                f"<p class='score'><strong>Score:</strong> {self.score}</p>"
                f"<p class='content'><strong>Content:</strong> {self.content}</p>"
                f"<p class='timestamp'><strong>Timestamp:</strong> {datetime.utcfromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')}</p>"
                f"</div>")

# Function to log rate limit data
def log_rate_limits(headers):
    rate_limit_used = headers.get('X-Ratelimit-Used', 'N/A')
    rate_limit_remaining = headers.get('X-Ratelimit-Remaining', 'N/A')
    rate_limit_reset = headers.get('X-Ratelimit-Reset', 'N/A')
    
    with open('limits.txt', 'w', encoding='utf-8') as file:
        file.write(f"Rate limit used: {rate_limit_used}\n")
        file.write(f"Rate limit remaining: {rate_limit_remaining}\n")
        file.write(f"Rate limit reset time: {rate_limit_reset}\n")
        file.write("\n")

try:
    # Reddit API credentials
    reddit = praw.Reddit(
        client_id='AnT1VJEVnyqQ2rV6Px89jg',
        client_secret='HTCyxmAi5gUEIXde_I1W9DYBBaqZTA',
        user_agent='samasc'
    )

    # Define the subreddit you want to monitor
    subreddit_name = 'SouthAsianMasculinity'  # Replace with the subreddit of your choice
    subreddit = reddit.subreddit(subreddit_name)

    # Create a directory to store posts if it doesn't exist
    os.makedirs('reddit_posts', exist_ok=True)

    # Manually make an API request to get the rate limit headers
    headers = requests.get(f'https://www.reddit.com/r/{subreddit_name}/new/.json', headers={
        'User-Agent': 'samasc'
    }).headers
    
    # Log rate limit data
    log_rate_limits(headers)

    # Fetch and save the 5 newest posts
    for submission in subreddit.new(limit=5):
        # Create a RedditPost instance
        post = RedditPost(
            title=submission.title,
            url=submission.url,
            score=submission.score,
            content=submission.selftext,
            timestamp=submission.created_utc
        )
        
        # Define file path
        filename = f'reddit_posts/{submission.id}.html'
        
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(post.to_html())

except Exception as e:
    with open('error_log.txt', 'a', encoding='utf-8') as file:
        file.write(f"An error occurred: {e}\n")
