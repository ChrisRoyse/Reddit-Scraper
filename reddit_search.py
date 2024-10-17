import praw
import time
import logging
import re
import csv

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace with your actual credentials
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
user_agent = 'windows:BOTNAMEt:v0.1 (by /u/REDDITUSERNAME)'

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Set to keep track of seen post IDs
seen_posts = set()

# Open the CSV file in write mode
with open('reddit_posts.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Title', 'Body', 'URL'])

    # Function to check rate limits
    def check_rate_limits():
        limits = reddit.auth.limits
        used = limits.get('used', 0)
        remaining = limits.get('remaining', 0)
        reset = limits.get('reset', 60)  # Default to 60 seconds if the key is missing

        logging.info(f"Rate Limit - Used: {used}, Remaining: {remaining}, Reset: {reset} seconds")

        if remaining < 10:  # If remaining requests are less than 10
            logging.warning(f"Approaching rate limit. Sleeping for {reset + 10} seconds to reset.")
            time.sleep(reset + 10)  # Sleep for reset time plus a buffer

    # Function to check for numbers between 350 and 675 in the text
    def check_credit_score_range(text):
        pattern = re.compile(r'\b(3[5-9]\d|[4-6]\d{2}|675)\b', re.IGNORECASE)
        matches = pattern.findall(text)
        return bool(matches)

    # Function to check for specific keywords related to financial distress
    def contains_financial_distress_keywords(text):
        keywords = ["repo", "repossession", "foreclosure", "late payment", "late payments"]
        return any(keyword in text.lower() for keyword in keywords)

    # Other filter functions as before...
    def contains_pound_symbol(text):
        return '£' in text

    def contains_universal_credit(text):
        return 'universal credit' in text.lower()

    def contains_transfer_credit(text):
        return 'transfer credit' in text.lower() or 'transfer credits' in text.lower()

    def contains_ficotime(text):
        return 'ficotime' in text.lower() or 'fico time' in text.lower()

    def contains_disallowed_urls(url):
        return 'canada' in url.lower() or 'ukpersonal' in url.lower()

    # Exponential backoff function
    def exponential_backoff(attempt):
        base_delay = 10  # Base delay in seconds
        return base_delay * (2 ** attempt)  # Exponentially increase delay

    # Function to search for keywords in both titles and bodies and by flair
    def search_reddit_keywords_and_flair(keywords, reddit_instance, subreddits, limit=10, delay=2):
        attempt = 0
        while True:
            try:
                # Search for keywords
                for keyword in keywords:
                    logging.info(f"Searching for posts containing '{keyword}'...")
                    results = reddit_instance.subreddit('all').search(keyword, limit=limit, time_filter='week')
                    for submission in results:
                        if submission.id not in seen_posts:
                            title_lower = submission.title.lower()
                            selftext_lower = submission.selftext.lower()

                            # Skip posts containing "ficotime" or "fico time"
                            if contains_ficotime(title_lower) or contains_ficotime(selftext_lower):
                                logging.info(f"Skipping post due to presence of 'ficotime' or 'fico time': {submission.title}")
                                continue

                            # Check if the post contains the pound symbol (£), "universal credit", "transfer credit", or disallowed URLs
                            if contains_pound_symbol(title_lower) or contains_pound_symbol(selftext_lower):
                                logging.info(f"Skipping post due to presence of pound symbol (£): {submission.title}")
                                continue
                            if contains_universal_credit(title_lower) or contains_universal_credit(selftext_lower):
                                logging.info(f"Skipping post due to presence of 'universal credit': {submission.title}")
                                continue
                            if contains_transfer_credit(title_lower) or contains_transfer_credit(selftext_lower):
                                logging.info(f"Skipping post due to presence of 'transfer credit' or 'transfer credits': {submission.title}")
                                continue
                            if contains_disallowed_urls(submission.url):
                                logging.info(f"Skipping post due to disallowed URL: {submission.url}")
                                continue

                            # Check if the post has a number in the range and/or contains the financial distress keywords
                            if ('credit' in title_lower or 'credit' in selftext_lower):
                                if check_credit_score_range(title_lower) or check_credit_score_range(selftext_lower) or contains_financial_distress_keywords(title_lower) or contains_financial_distress_keywords(selftext_lower):
                                    print(f"Title: {submission.title}")
                                    print(f"Body: {submission.selftext[:100]}...")  # Print a snippet of the body
                                    print(f"Score: {submission.score}")
                                    print(f"URL: {submission.url}")
                                    print('---')

                                    # Write the data to the CSV file
                                    writer.writerow([submission.title, submission.selftext, submission.url])

                                seen_posts.add(submission.id)
                    # Check rate limits after each keyword search
                    check_rate_limits()
                    time.sleep(delay)  # Respect rate limits by adding a delay

                    # Add a 10-second delay between each keyword search
                    time.sleep(10)

                # Search for posts with specific flair
                for subreddit_name in subreddits:
                    logging.info(f"Searching for posts with 'Collections & Charge Offs' flair in '{subreddit_name}'...")
                    subreddit = reddit_instance.subreddit(subreddit_name)
                    for submission in subreddit.new(limit=limit):
                        if submission.id not in seen_posts:
                            if submission.link_flair_text and 'Collections & Charge Offs' in submission.link_flair_text:

                                # Skip posts containing "ficotime" or "fico time"
                                if contains_ficotime(submission.title.lower()) or contains_ficotime(submission.selftext.lower()):
                                    logging.info(f"Skipping post due to presence of 'ficotime' or 'fico time': {submission.title}")
                                    continue

                                # Skip posts with disallowed URLs
                                if contains_disallowed_urls(submission.url):
                                    logging.info(f"Skipping post due to disallowed URL: {submission.url}")
                                    continue

                                print(f"Title: {submission.title}")
                                print(f"Body: {submission.selftext[:100]}...")  # Print a snippet of the body
                                print(f"Score: {submission.score}")
                                print(f"URL: {submission.url}")
                                print(f"Flair: {submission.link_flair_text}")
                                print('---')

                                # Write the data to the CSV file
                                writer.writerow([submission.title, submission.selftext, submission.url])

                                seen_posts.add(submission.id)
                    # Check rate limits after flair search
                    check_rate_limits()
                    time.sleep(delay)  # Respect rate limits by adding a delay

                    # Add a 10-second delay between each subreddit flair search
                    time.sleep(10)

                # Search for posts containing "credit" and check for number range and financial distress keywords
                logging.info("Searching for posts containing 'credit' and checking for number range and keywords...")
                results = reddit_instance.subreddit('all').search('credit', limit=limit, time_filter='week')
                for submission in results:
                    if submission.id not in seen_posts:
                        title_lower = submission.title.lower()
                        selftext_lower = submission.selftext.lower()

                        # Skip posts containing "ficotime" or "fico time"
                        if contains_ficotime(title_lower) or contains_ficotime(selftext_lower):
                            logging.info(f"Skipping post due to presence of 'ficotime' or 'fico time': {submission.title}")
                            continue

                        # Skip posts with disallowed URLs
                        if contains_disallowed_urls(submission.url):
                            logging.info(f"Skipping post due to disallowed URL: {submission.url}")
                            continue

                        # Check if the post contains the pound symbol (£), "universal credit", or "transfer credit"
                        if contains_pound_symbol(title_lower) or contains_pound_symbol(selftext_lower):
                            logging.info(f"Skipping post due to presence of pound symbol (£): {submission.title}")
                            continue
                        if contains_universal_credit(title_lower) or contains_universal_credit(selftext_lower):
                            logging.info(f"Skipping post due to presence of 'universal credit': {submission.title}")
                            continue
                        if contains_transfer_credit(title_lower) or contains_transfer_credit(selftext_lower):
                            logging.info(f"Skipping post due to presence of 'transfer credit' or 'transfer credits': {submission.title}")
                            continue

                        # Check if the post has a number in the range or contains financial distress keywords
                        if check_credit_score_range(title_lower) or check_credit_score_range(selftext_lower) or contains_financial_distress_keywords(title_lower) or contains_financial_distress_keywords(selftext_lower):
                            print(f"Title: {submission.title}")
                            print(f"Body: {submission.selftext[:100]}...")  # Print a snippet of the body
                            print(f"Score: {submission.score}")
                            print(f"URL: {submission.url}")
                            print('---')

                            # Write the data to the CSV file
                            writer.writerow([submission.title, submission.selftext, submission.url])

                        seen_posts.add(submission.id)
                # Check rate limits after this search
                check_rate_limits()
                time.sleep(delay)  # Respect rate limits by adding a delay

                # Add a 10-second delay between each keyword search
                time.sleep(10)

                attempt = 0  # Reset the attempt counter on a successful run

            except Exception as e:
                logging.error(f"Error occurred: {e}")
                logging.warning(f"Connection failed. Attempt {attempt + 1}. Retrying after exponential backoff...")
                time.sleep(exponential_backoff(attempt))
                attempt += 1

    # Keywords to search for
    keywords = ["Credit Saint", "debt consolidation", "Credit Help", "Credit Repair", "fico", "vantage score", "raise credit", "credit card debt", "co-signed", "cosigned", "charge off", "chargeoff", "goodwill letter", "goodwill letters", "goodwill payment", "goodwill payments", "late payment", "late payments", "charge-off", "charge-offs", "credit increase", "credit increases", "credit utilization", "credit score", "debt collector", "debt collectors"]

    # Subreddits to search for the specific flair
    subreddits = ["CRedit"]

    # Infinite loop to keep searching
    while True:
        search_reddit_keywords_and_flair(keywords, reddit, subreddits)
        time.sleep(5)  # Short delay to avoid tight looping, adjust as needed
