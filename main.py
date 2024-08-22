import praw
import os
import requests

# Function to log rate limit data
def log_rate_limits(headers):
    rate_limit_used = headers.get('X-Ratelimit-Used', 'N/A')
    rate_limit_remaining = headers.get('X-Ratelimit-Remaining', 'N/A')
    rate_limit_reset = headers.get('X-Ratelimit-Reset', 'N/A')

    # Overwrite the limits.txt file
    with open('limits.txt', 'w', encoding='utf-8') as file:
        file.write(f"Rate limit used: {rate_limit_used}\n")
        file.write(f"Rate limit remaining: {rate_limit_remaining}\n")
        file.write(f"Rate limit reset time: {rate_limit_reset}\n")

    return int(rate_limit_remaining) if rate_limit_remaining.isdigit() else 0

try:
    # Reddit API credentials
    reddit = praw.Reddit(
        client_id='AnT1VJEVnyqQ2rV6Px89jg',
        client_secret='HTCyxmAi5gUEIXde_I1W9DYBBaqZTA',
        user_agent='samasc'
    )

    # Define the subreddit you want to monitor
    subreddit_name = 'SouthAsianMasculinity'
    subreddit = reddit.subreddit(subreddit_name)

    # Manually make an API request to get the rate limit headers
    response = requests.get(f'https://www.reddit.com/r/{subreddit_name}/new/.json', headers={
        'User-Agent': 'samasc'
    })
    headers = response.headers
    
    # Log rate limit data and get the remaining rate limit
    rate_limit_remaining = log_rate_limits(headers)

    # Check if the rate limit remaining is really low
    if rate_limit_remaining < 10:  # You can adjust the threshold as needed
        print("Rate limit remaining is very low. Exiting...")
    else:
        # Create a directory to store posts if it doesn't exist
        os.makedirs('reddit_posts', exist_ok=True)

        # Fetch and save the 5 newest posts
        for submission in subreddit.new(limit=5):
            unique_id = submission.id
            filename = f'reddit_posts/{unique_id}.txt'
            
            if not os.path.exists(filename):
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"Title: {submission.title}\n\n")
                    file.write(f"URL: {submission.url}\n\n")
                    file.write(f"Score: {submission.score}\n\n")
                    file.write(f"Content:\n{submission.selftext}\n\n")
                    file.write(f"Timestamp: {submission.created_utc}\n")

except Exception as e:
    with open('error_log.txt', 'a', encoding='utf-8') as file:
        file.write(f"An error occurred: {e}\n")
