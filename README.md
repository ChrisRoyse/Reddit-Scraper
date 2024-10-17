# CreditLeadScraper: Reddit Keyword Search and Lead Generation for Credit Repair

**CreditLeadScraper** is a Python-based tool designed to help credit repair companies identify potential leads by searching Reddit for specific keywords related to credit. The scraper scans Reddit posts and comments for users seeking advice or assistance with credit issues. When relevant posts are found, it saves the post title, content, and URL to a CSV file, enabling companies to engage directly with potential customers.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Future Enhancements](#future-enhancements)

## Features

- **Keyword-Based Search**: Searches Reddit posts and comments using customizable keywords related to credit and credit repair.
- **Lead Identification**: Detects posts where users are seeking credit advice or help, generating a list of potential leads.
- **Data Export**: Saves the title, content, and URL of matching posts to a CSV file for easy access and analysis.
- **Automated Scraping**: Continuously monitors Reddit, running on a schedule to identify new posts in real-time.
- **Rate Limit Handling**: Implements rate limit checks and exponential backoff to comply with Reddit API usage policies.
- **Customizable Filters**: Allows for filtering out irrelevant posts based on specific criteria, such as certain keywords or symbols.

## How It Works

1. **Initialization**: Sets up a Reddit instance using the PRAW (Python Reddit API Wrapper) library with provided credentials.
2. **Keyword Search**:
   - Searches Reddit posts and comments for a predefined list of keywords.
   - Scans both titles and bodies of posts.
3. **Filtering**:
   - Excludes posts containing disallowed keywords or symbols (e.g., "ficotime", "£", "universal credit").
   - Filters out posts from certain subreddits or with disallowed URLs.
4. **Lead Collection**:
   - Identifies posts that match credit-related criteria, such as specific credit score ranges or financial distress keywords.
   - Saves relevant post details (title, body, URL) to a CSV file.
5. **Rate Limit Compliance**:
   - Checks Reddit API rate limits to avoid exceeding allowed requests.
   - Implements exponential backoff in case of connection failures or rate limit hits.
6. **Continuous Monitoring**:
   - Runs in an infinite loop, periodically searching for new posts and updating the CSV file with new leads.

## Tech Stack

- **Language**: Python 3.x
- **Libraries**:
  - `praw`: Python Reddit API Wrapper for interacting with Reddit.
  - `logging`: For logging information and errors.
  - `re`: Regular expressions for pattern matching.
  - `csv`: For writing data to CSV files.
- **Reddit API**: Used for accessing posts and comments programmatically.

## Installation

### Prerequisites

- **Python 3.x** installed on your system.
- A **Reddit account** with a registered application to obtain API credentials.

### Steps

1. **Install Required Packages**

   ```bash
   pip install praw
   ```

2. **Set Up Reddit API Credentials**

   - Go to [Reddit Apps](https://www.reddit.com/prefs/apps) and create a new script application.
   - Obtain your `client_id`, `client_secret`, and set a `user_agent`.

3. **Configure the Script**

   - Open the script file `reddit_search.py`.
   - Replace the placeholder credentials with your actual Reddit API credentials:

     ```python
     client_id = 'YOUR_CLIENT_ID'
     client_secret = 'YOUR_CLIENT_SECRET'
     user_agent = 'windows:YOUR_APP_NAME:v0.1 (by /u/YOUR_REDDIT_USERNAME)'
     ```

4. **Customize Keywords and Filters (Optional)**

   - Modify the `keywords` list to include any additional keywords you want to search for.
   - Adjust filter functions as needed to refine your search criteria.

## Usage

1. **Run the Script**

   ```bash
   python reddit_search.py
   ```

2. **Monitor Output**

   - The script will log its progress, including any posts it skips or saves.
   - Relevant posts will be printed to the console and written to `reddit_posts.csv`.

3. **Review Leads**

   - Open `reddit_posts.csv` in a spreadsheet application to review and analyze the collected leads.

## Configuration

- **Keywords**: Customize the list of keywords in the script to target specific terms related to credit repair.

  ```python
  keywords = [
      "Credit Saint", "debt consolidation", "Credit Help", "Credit Repair",
      "fico", "vantage score", "raise credit", "credit card debt",
      "co-signed", "cosigned", "charge off", "goodwill letter",
      "late payment", "credit increase", "credit utilization",
      "credit score", "debt collector"
  ]
  ```

- **Subreddits**: Modify the `subreddits` list to include additional subreddits you want to monitor for specific flair.

  ```python
  subreddits = ["CRedit"]
  ```

- **Rate Limits and Delays**: Adjust the delay times and rate limit thresholds as needed to comply with Reddit's API policies.

  ```python
  def check_rate_limits():
      # Adjust rate limit thresholds
  ```

- **Filter Functions**: Update filter functions to exclude or include posts based on new criteria.

  ```python
  def contains_financial_distress_keywords(text):
      keywords = ["repo", "repossession", "foreclosure", "late payment"]
      return any(keyword in text.lower() for keyword in keywords)
  ```

## Future Enhancements

- **Comment Scraping**: Extend functionality to include comments, not just posts.
- **Database Integration**: Store leads in a database for more robust data management.
- **GUI Interface**: Develop a graphical user interface for easier configuration and monitoring.
- **Email Notifications**: Implement email alerts when new leads are found.
- **Advanced Analytics**: Add features to analyze trends in the collected data.
