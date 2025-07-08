import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

WORDPRESS_URL = os.getenv("WORDPRESS_URL")  # e.g., https://example.com
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")  # No spaces!

def publish_to_wordpress(title, content):
    """
    Publishes a post to WordPress using REST API credentials from .env
    """
    if not all([WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD]):
        print("❌ Missing environment variables. Check .env file.")
        return False

    post_url = f"{WORDPRESS_URL.rstrip('/')}/wp-json/wp/v2/posts"
    headers = {"Content-Type": "application/json"}
    data = {
        "title": title,
        "content": content,
        "status": "publish"  # or "draft"
    }

    try:
        response = requests.post(
            post_url,
            headers=headers,
            json=data,
            auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
        )

        if response.status_code == 201:
            print(f"✅ Post published: {response.json().get('link')}")
            return True
        else:
            print(f"❌ Failed to publish post. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Error during request: {e}")
        return False
