# autoblog.py
import requests
import json
import time

from tenacity import (
    retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
)
from configmanager import *

shop_name = config['shopify_shop_name']
company_name = config['company_name']

keyword = "shirt" # seo keyword

def get_shop_blogs(shopify_store_url, access_token):
    url = f"https://{shopify_store_url}/admin/api/2024-04/blogs.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

def get_articles(store_url, access_token, blog_id):
    """
    Retrieves all articles from a specified blog in the Shopify store using the Shopify Admin API.

    This function makes an HTTP GET request to the Shopify API's articles endpoint for a specific blog. It is decorated with a retry mechanism which retries the request on encountering specific exceptions (like network-related errors) with exponential backoff.

    Parameters:
    - store_url (str): The base URL of the Shopify store, e.g., 'https://example.myshopify.com'.
    - access_token (str): The access token used for authenticating with the Shopify API.
    - blog_id (str): The ID of the blog from which to retrieve articles.

    Returns:
    - dict: A dictionary object containing the response data with details of all articles if successful.

    Raises:
    - Exception: If the request fails or the response status is not 200, it raises an exception with the error code and text.

    Usage:
    - articles = get_articles('https://example.myshopify.com', 'your_access_token', '123456789')
      print(articles)  # Prints the list of articles retrieved from the specified blog.
    """

    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    response = requests.get(f"https://{store_url}/admin/api/2024-04/blogs/{blog_id}/articles.json", headers=headers)

    if response.status_code == 200:
        return response.json()  # Returns the list of articles
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")  


def delete_article(store_url, access_token, article_id, blog_id):
    # Shopify API URL
    url = f"https://{store_url}/admin/api/2024-04/blogs/{blog_id}/articles/{article_id}.json"

    # Set headers
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token,
    }

    # Make the POST request to Shopify API
    response = requests.delete(url, headers=headers)
    # Check the response
    if response.status_code == 200:
        print("Blog post deleted successfully!")
        print("Response:", response.json())
        return response.json()
    else:
        print("Failed to delete blog post.")
        print("Status Code:", response.status_code)
        print("Response:", response.json())
        return response.json()

@retry(wait=wait_random_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(10), retry=retry_if_exception_type(requests.exceptions.RequestException))
def post_blog(store_url, access_token, api_key, blog_id):

    title, content = gen_blog(api_key)

    # Article details
    article_title = title
    article_body = content
    author = "Author Name"

    # Shopify API URL for creating a blog post
    url = f"https://{store_url}/admin/api/2024-04/blogs/{blog_id}/articles.json"

    # Article data
    article_data = {
        "article": {
            "title": article_title,
            "body_html": article_body,
            "author": author
        }
    }

    # Convert the data to JSON format
    data = json.dumps(article_data)

    # Set headers
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": access_token,
    }

    # Make the POST request to Shopify API
    response = requests.post(url, headers=headers, data=data)

    # Check the response
    if response.status_code == 201:
        print("Blog post created successfully!")
        print("Response:", response.json())
        return response.json()
    else:
        print("Failed to create blog post.")
        print("Response:", response.json())
        raise Exception(f"Error: {response.status_code}, {response.text}") 

def gen_blog(api_key):
    url = "https://api.neets.ai/v1/chat/completions"

    payload = {
        "messages": [
            {
                "role": "user",
                "content": 
                "You are a content writer expert in writing SEO-optimized blog posts. \
                Respond only with the blog post. Your output should never contain your own output. \
                The blog is for a store called {shop_name}. \
                Write an SEO-optimized 200 word blog post with the SEO keyword {keyword}." \
                "Write the title at the start with the format  Title: (Title here) "
            }
        ],
        "model": "mistralai/Mixtral-8X7B-Instruct-v0.1",
        "temperature": 0.7
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-Key": api_key
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        lines = content.split("\n")
        title = "Blog Post"

        for line in lines:
            if line.startswith("Title:"):
                title = line.replace("Title:", "").strip()
            else:
                content = "\n".join(lines[lines.index(line) + 1:])
                break

        print(title)
        print(content)

        return title, content
    else:
        time.sleep(10)

