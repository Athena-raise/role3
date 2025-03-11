import os
import time
import json
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

class WeiboScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Cookie': os.getenv('WEIBO_COOKIE', ''),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.keywords = [
            '养老', '老年人', '养老院', '居家养老', '养老政策',
            '养老保障', '养老服务', '养老产业', '养老社区'
        ]
        # 设置输出目录为桌面的"微博"文件夹
        self.output_dir = os.path.expanduser('~/Desktop/微博')
        
    def search_weibo(self, keyword, page=1):
        """Search Weibo posts with given keyword"""
        url = 'https://m.weibo.cn/api/container/getIndex'
        params = {
            'containerid': '100103type=1&q=' + keyword,
            'page_type': 'searchall',
            'page': page,
            'luicode': '10000011',
            'lfid': '100103type=1&q=' + keyword
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error searching for keyword '{keyword}': {str(e)}")
            return None

    def clean_content(self, content):
        """Clean the content by removing HTML tags and formatting"""
        if not content:
            return ''
            
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        
        # Remove URLs
        content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)
        
        # Remove special characters and extra spaces
        content = re.sub(r'&nbsp;', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        # Remove hashtags
        content = re.sub(r'#\w+#', '', content)
        
        # Remove @ mentions
        content = re.sub(r'@[\w\-]+', '', content)
        
        # Clean up any remaining whitespace
        content = content.strip()
        
        return content

    def extract_post_data(self, post):
        """Extract relevant data from a post"""
        try:
            # Handle timestamp conversion
            created_at = post.get('created_at', '')
            try:
                # Try to parse the timestamp
                if isinstance(created_at, str):
                    # If it's a string like "2024-03-20 10:30:00"
                    publish_time = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                else:
                    # If it's a timestamp
                    publish_time = datetime.fromtimestamp(int(created_at))
            except (ValueError, TypeError):
                publish_time = datetime.now()  # Fallback to current time if parsing fails

            # Clean the content
            content = self.clean_content(post.get('text', ''))

            return {
                'user_id': str(post.get('user', {}).get('id', '')),
                'username': post.get('user', {}).get('screen_name', ''),
                'platform': '微博',
                'keyword': post.get('keyword', ''),
                'publish_time': publish_time.strftime('%Y-%m-%d %H:%M:%S'),
                'content': content,
                'likes': int(post.get('attitudes_count', 0)),
                'comments': int(post.get('comments_count', 0)),
                'reposts': int(post.get('reposts_count', 0))
            }
        except Exception as e:
            print(f"Error extracting post data: {str(e)}")
            return None

    def scrape_data(self, max_pages=5):
        """Scrape data for all keywords"""
        all_posts = []
        
        for keyword in self.keywords:
            print(f"Scraping data for keyword: {keyword}")
            
            for page in range(1, max_pages + 1):
                print(f"Processing page {page}")
                data = self.search_weibo(keyword, page)
                
                if not data or 'data' not in data or 'cards' not in data['data']:
                    print(f"No more data for keyword '{keyword}' on page {page}")
                    break
                
                for card in data['data']['cards']:
                    if 'mblog' in card:
                        post_data = self.extract_post_data(card['mblog'])
                        if post_data:
                            post_data['keyword'] = keyword
                            all_posts.append(post_data)
                
                # Add delay to avoid rate limiting
                time.sleep(3)  # Increased delay to 3 seconds
        
        return all_posts

    def save_to_csv(self, data, filename='weibo_elderly_care_data.csv'):
        """Save scraped data to CSV file"""
        if not data:
            print("No data to save")
            return
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 构建完整的文件路径
        filepath = os.path.join(self.output_dir, filename)
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"Data saved to {filepath}")

def main():
    scraper = WeiboScraper()
    data = scraper.scrape_data()
    scraper.save_to_csv(data)

if __name__ == "__main__":
    main() 