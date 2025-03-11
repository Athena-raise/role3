# Weibo Elderly Care Data Scraper

This script scrapes Weibo posts related to elderly care topics using the Weibo API.

## Features

- Scrapes posts using multiple elderly care related keywords
- Collects user information, post content, and engagement metrics
- Saves data in CSV format with UTF-8 encoding
- Includes rate limiting to avoid API restrictions
- Error handling for API requests and data processing

## Requirements

- Python 3.7+
- Required packages listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root directory
2. Add your Weibo cookie to the `.env` file:
```
WEIBO_COOKIE=your_cookie_here
```

To get your Weibo cookie:
1. Log in to Weibo in your browser
2. Open Developer Tools (F12)
3. Go to the Network tab
4. Find any request to weibo.com
5. Copy the Cookie header value

## Usage

Run the script:
```bash
python weibo_scraper.py
```

The script will:
1. Search for posts using predefined elderly care related keywords
2. Scrape up to 5 pages of results for each keyword
3. Save the collected data to `weibo_elderly_care_data.csv`

## Output Format

The CSV file will contain the following columns:
- user_id: The Weibo user ID
- username: The Weibo username
- platform: Always "微博"
- keyword: The search keyword that matched the post
- publish_time: Post publication time
- content: Post content
- likes: Number of likes
- comments: Number of comments
- reposts: Number of reposts

## Notes

- The script includes a 2-second delay between requests to avoid rate limiting
- Make sure you have a valid Weibo cookie to access the API
- The script will automatically handle errors and continue with the next post if one fails 