import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")

def post_to_linkedin(image_path):
    # Fetch LinkedIn user profile
    profile_res = requests.get(
        "https://api.linkedin.com/v2/me",
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "X-Restli-Protocol-Version": "2.0.0"
        }
    )

    if profile_res.status_code != 200:
        print(" Failed to fetch LinkedIn profile:", profile_res.text)
        return

    user_urn = f"urn:li:person:{profile_res.json()['id']}"

    # Register image upload
    register_body = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": user_urn,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    res = requests.post(
        "https://api.linkedin.com/v2/assets?action=registerUpload",
        headers=headers,
        json=register_body
    )

    if res.status_code != 200:
        print("Upload registration failed:", res.text)
        return

    res_json = res.json()

    upload_url = res_json["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    asset = res_json["value"]["asset"]

    # Upload image
    with open(image_path, 'rb') as f:
        upload_res = requests.put(upload_url, data=f)
        if upload_res.status_code not in [200, 201]:
            print("Image upload failed:", upload_res.text)
            return

    # Static post content and hashtags
    static_intro = " "
    hashtags = " "

    share_text = f"{static_intro}\n\n{hashtags}"

    # Prepare final share body
    share_body = {
        "author": user_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": share_text
                },
                "shareMediaCategory": "IMAGE",
                "media": [{
                    "status": "READY",
                    "description": {"text": "Valuable feedback from our community"},
                    "media": asset,
                    "title": {"text": "User Feedback Highlight"}
                }]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    # Publish the post
    share_res = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers=headers,
        json=share_body
    )

    if share_res.status_code == 201:
        print(" Posted to LinkedIn successfully.")
    else:
        print(f" Post failed: {share_res.status_code}")
        print(" Response:", share_res.text)
