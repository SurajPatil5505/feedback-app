import requests

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "YOUR_REDIRECT_URI"

# run this link in browser https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=scope=openid%20r_liteprofile%20r_emailaddress%20w_member_social
# This will return AUTH_CODE after code=, replace REPLACE_WITH_AUTH_CODE with your code
AUTH_CODE = "REPLACE_WITH_AUTH_CODE"

token_url = "https://www.linkedin.com/oauth/v2/accessToken"

data = {
    "grant_type": "authorization_code",
    "code": AUTH_CODE,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

response = requests.post(token_url, data=data)
print(response.json())