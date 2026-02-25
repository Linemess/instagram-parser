from instagrapi import Client
import requests
import os
import time

IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE = os.getenv("AIRTABLE_TABLE")

ACCOUNTS = [
    "username1",
    "username2"
]

def send_to_airtable(data):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "fields": data
    }
    requests.post(url, json=payload, headers=headers)

def main():
    cl = Client()
    cl.login(IG_USERNAME, IG_PASSWORD)

    for username in ACCOUNTS:
        try:
            user_id = cl.user_id_from_username(username)
            medias = cl.user_medias(user_id, amount=5)

            for media in medias:
                if media.product_type == "clips":
                    data = {
                        "username": username,
                        "caption": media.caption_text,
                        "likes": media.like_count,
                        "comments": media.comment_count,
                        "views": media.view_count,
                        "date": str(media.taken_at)
                    }
                    send_to_airtable(data)

            time.sleep(7)

        except Exception as e:
            print(f"Error with {username}: {e}")

if __name__ == "__main__":
    main()
