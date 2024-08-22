import praw
import os
import requests
from html import escape

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
        # Extract the unique 7-character code from the URL
        unique_id = submission.id
        filename = f'reddit_posts/{unique_id}.txt'
        
        if not os.path.exists(filename):
            # Sanitize content to remove HTML tags and escape special characters
            sanitized_title = escape(submission.title)
            sanitized_url = escape(submission.url)
            sanitized_content = escape(submission.selftext)
            sanitized_score = escape(str(submission.score))
            sanitized_timestamp = escape(str(submission.created_utc))
            
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"Title: {sanitized_title}\n\n")
                file.write(f"URL: {sanitized_url}\n\n")
                file.write(f"Score: {sanitized_score}\n\n")
                file.write(f"Content:\n{sanitized_content}\n\n")
                file.write(f"Timestamp: {sanitized_timestamp}\n")

except Exception as e:
    with open('error_log.txt', 'a', encoding='utf-8') as file:
        file.write(f"An error occurred: {e}\n")
