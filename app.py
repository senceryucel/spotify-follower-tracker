import requests, time, json
from fetcher import fetch_followers
from sender import mail_sender
from datetime import datetime
import pytz

with open("config.json", "r") as config_file:
    config = json.load(config_file)

TIMEZONE = pytz.timezone(config["timezone"])
SPOTIFY_USER_ID = config["spotify_configs"]["user_id_to_track"]
SPOTIFY_CLIENT_ID = config["spotify_configs"]["spotify_client_id"]
SPOTIFY_CLIENT_SECRET = config["spotify_configs"]["spotify_client_secret"]

fetcher = fetch_followers.FetchFollowers(SPOTIFY_USER_ID)

is_send_gmail = config["send_gmail"]
if is_send_gmail:
    gmail_sender_config = config["gmail_sender"]
    gmail_sender = mail_sender.GmailSender(gmail_sender_config)

def get_token():
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=payload, headers=headers)
    return response.json()["access_token"]

def monitor_error(error):
    with open("./logs/error.log", "a") as error_log:
        error_log.write(f"{datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')} An error occurred: {str(error)}\n")
        if is_send_gmail:
            gmail_sender.send_message("Spotify - Error", f"An error occurred: {str(error)}")

SPOTIFY_ACCESS_TOKEN = get_token()

url = "https://api.spotify.com/v1/users/{user_id}"

headers = {
    "Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"
}

init_response = requests.get(url.format(user_id=SPOTIFY_USER_ID), headers=headers)

total_followers = init_response.json()["followers"]["total"]

time.sleep(.5)

with open("./logs/error.log", "a") as error_log:
    error_log.write(f"{datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')} App started\n")

while True:
    try:
        response = requests.get(url.format(user_id=SPOTIFY_USER_ID), headers=headers)
        temp = response.json()["followers"]["total"]
    except KeyError as expired_token:
        with open("./logs/error.log", "a") as error_log:
            error_log.write(f"{datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')} Token expired - getting new token\n")
        SPOTIFY_ACCESS_TOKEN = get_token()
        headers["Authorization"] = f"Bearer {SPOTIFY_ACCESS_TOKEN}"
        continue
    except json.decoder.JSONDecodeError as e:
        with open("./logs/error.log", "a") as error_log:
            error_log.write(f"{datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')} API limit reached - retrying in 60s\n")
        time.sleep(60)
        continue
    except Exception as e:
        monitor_error(e)
        continue

    try:
        if temp != total_followers:
            print(f"Change in followers: {temp - total_followers}")
            updated_lists = fetcher.compare_followers()
            if updated_lists[0] or updated_lists[1]:
                if updated_lists[0]:  # new followers
                    if is_send_gmail:
                        followers = ", ".join(updated_lists[0])
                        gmail_sender.send_message("Spotify - New followers", f"New followers: {followers}")
                if updated_lists[1]:  # unfollowers
                    if is_send_gmail:
                        unfollowers = ", ".join(updated_lists[1])
                        gmail_sender.send_message("Spotify - Unfollowers", f"Unfollowers: {unfollowers}")
                total_followers = temp
            else:
                # we are in the temp != total_followers block but the lists are empty
                # this means the new person has followed and then unfollowed immediately
                gmail_sender.send_message("Spotify - Followed and unfollowed", "Followed and unfollowed immediately")
    except Exception as e:
        monitor_error(e)

    time.sleep(.75)  # wait to avoid spamming the API
