from __future__ import print_function
import os
import base64
from email import message_from_bytes
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

import vertexai
from vertexai.preview.generative_models import GenerativeModel

# --- Load environment variables ---
load_dotenv()

# --- SETUP VARIABLES ---
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
PROJECT_ID = os.getenv("PROJECT_ID", "ai-news-agency")
REGION = os.getenv("REGION", "us-central1")
LAST_ID_FILE = "last_email_id.txt"
AGENT_PROMPT_FILE = "agents/lisa_luckas.txt"

# --- GMAIL: Get the latest email message ---
def get_latest_email():
    creds = None
    if os.path.exists('token.json'):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', maxResults=1).execute()
    if 'messages' not in results:
        print("📭 No messages found.")
        return None, None

    message_id = results['messages'][0]['id']

    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, 'r') as f:
            last_id = f.read().strip()
        if message_id == last_id:
            print("🔁 No new email to process.")
            return None, None

    # Save new ID
    with open(LAST_ID_FILE, 'w') as f:
        f.write(message_id)

    msg = service.users().messages().get(userId='me', id=message_id, format='raw').execute()
    msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    mime_msg = message_from_bytes(msg_str)

    def extract_email_body(mime_msg):
        if mime_msg.is_multipart():
            for part in mime_msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    return part.get_payload(decode=True).decode()
                elif content_type == "text/html" and "attachment" not in content_disposition:
                    return part.get_payload(decode=True).decode()
        else:
            return mime_msg.get_payload(decode=True).decode()
        return None

    email_text = extract_email_body(mime_msg)
    return email_text, message_id

# --- VERTEX AI: Summarize the email using Gemini ---
def summarize_email(email_text):
    vertexai.init(project=PROJECT_ID, location=REGION)
    model = GenerativeModel("gemini-2.5-pro")

    with open(AGENT_PROMPT_FILE, "r") as f:
        role_prompt = f.read()

    full_prompt = f"{role_prompt}\n\n{email_text}"
    response = model.generate_content(full_prompt)
    return response.text

# --- MAIN ---
if __name__ == '__main__':
    print("🚀 Starting AI News Agent...")
    email_body, email_id = get_latest_email()
    if email_body:
        print("✉️ New email received. Summarizing...")
        summary = summarize_email(email_body)
        print("\n📰 --- AI-Generated News Summary ---\n")
        print(summary)
        with open("summaries.log", "a") as f:
            f.write(f"{email_id}\n{summary}\n\n")

        # --- WORDPRESS PUBLISHING ---
        from wordpress_publisher import publish_to_wordpress
        import json

        # Load image and crosslink data
        with open("images/dax30.json") as img_file:
            images = json.load(img_file)

        with open("links/business.json") as link_file:
            crosslinks = json.load(link_file)

        # Publish the summary
        title_line = summary.split("\n")[0].strip("* ").strip()
        publish_to_wordpress(
            title=title_line,
            content=summary,
            category="5",  # Fixed category ID for Business
            tags=[8],      # Use the correct numeric tag ID
            images=images,
        crosslinks=crosslinks
    )
