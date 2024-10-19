import praw
import os
import requests
import markdown2  # This library will convert markdown to HTML

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
    subreddit_name = 'SouthAsianMasculinity'
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
        # Extract the unique timestamp as filename
        unique_id = submission.created_utc
        filename = f'reddit_posts/{unique_id}.html'
        
        if not os.path.exists(filename):
            # Always use the Reddit permalink as the post URL
            post_url = f"https://www.reddit.com{submission.permalink}"

            # Determine the content to display based on the post type
            if submission.is_self:
                # Convert markdown to HTML using markdown2
                content = markdown2.markdown(submission.selftext)
            elif submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                content = f'<img src="{submission.url}" alt="{submission.title}"/>'
            elif submission.url.endswith(('.mp4', '.gifv', '.webm')):
                content = f'<video controls><source src="{submission.url}" type="video/mp4">Your browser does not support the video tag.</video>'
            else:
                content = f'<a href="{submission.url}" target="_blank">{submission.url}</a>'

            # Write the post content, including the poster's username
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"""
                <div class="post">
                    <h2 class="title">{submission.title}</h2>
                    <p class="author">Posted by: {submission.author}</p>
                    <p class="url"><a href="{post_url}" target="_blank">{post_url}</a></p>
                    <div class="content">{content}</div>
                    <p class="timestamp">Timestamp: {submission.created_utc}</p>
                </div>
                """)

except Exception as e:
    with open('error_log.txt', 'a', encoding='utf-8') as file:
        file.write(f"An error occurred: {e}\n")
