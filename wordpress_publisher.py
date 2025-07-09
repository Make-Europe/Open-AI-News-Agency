import os
import random
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv("WORDPRESS_URL")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")

# Fixed category ID for Business
BUSINESS_CATEGORY_ID = 5

# Get media ID from image URL
def get_media_id(image_url):
    media_endpoint = f"{WORDPRESS_URL.rstrip('/')}/wp-json/wp/v2/media?per_page=100"
    try:
        response = requests.get(
            media_endpoint,
            auth=HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
        )
        if response.status_code == 200:
            for item in response.json():
                if item.get("source_url") == image_url:
                    return item.get("id")
        else:
            print(f"❌ Failed to fetch media library. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching media ID: {e}")
    return None

def publish_to_wordpress(title, content, category="Business", tags=None, images=None, crosslinks=None):
    if not all([WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD]):
        print("❌ Missing environment variables. Check .env file.")
        return False

    if tags is None:
        tags = []

    # Choose image if available
    image_url = None
    for company, image_list in images.items():
        if company.lower() in title.lower():
            image_url = random.choice(image_list)
            break

    featured_media_id = get_media_id(image_url) if image_url else None

    # Add crosslinks
    if crosslinks:
        selected_links = random.sample(crosslinks, min(3, len(crosslinks)))
        crosslink_html = "<br><br><strong>Related Articles:</strong><ul>"
        for link in selected_links:
            crosslink_html += f'<li><a href="{link}" target="_blank">{link}</a></li>'
        crosslink_html += "</ul>"
        content += crosslink_html

    # SEO (Yoast)
    meta_description = next((line for line in content.split("\n") if line.strip()), title)[:155]
    focus_keyword = " ".join(title.strip("* ").split()[:4])

    post_url = f"{WORDPRESS_URL.rstrip('/')}/wp-json/wp/v2/posts"
    headers = {"Content-Type": "application/json"}
    data = {
        "title": title,
        "content": content,
        "status": "publish",
        "categories": [BUSINESS_CATEGORY_ID],
        "tags": tags,
        "meta": {
            "yoast_wpseo_metadesc": meta_description,
            "yoast_wpseo_focuskw": focus_keyword
        }
    }

    if featured_media_id:
        data["featured_media"] = featured_media_id

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