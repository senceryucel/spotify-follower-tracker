<h1 style="font-size: 48px" align="center">Spotify Follower Tracker</h1>

Get notified when someone follows (or unfollows) you on Spotify.

Spotify does not notify you when you gain or lose followers, so I created this application to monitor the changes in your followers list.

# Usage

### Before you start

##### Create a Spotify Developer Application
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
2. Click on `Create an App`
3. Add `http://localhost:8080` to the `Redirect URIs`
4. Fill in other fields and click on `Create`
5. Click on `Settings`, there you will find your `Client ID` and `Client Secret`.

##### Create a Gmail App Password
1. Go to [Google Account](https://myaccount.google.com/)
2. Click on `Security`
3. Scroll down to `Less secure app access` and turn it on
4. Click on `App passwords`
5. Select `Mail` and `Other` and click `Generate`
6. Generated password is your gmail app password.

##### Modify the `config.json` file
```json
{
    "timezone": "YOUR_TIMEZONE",
    
    "spotify_configs":{
        "user_id_to_track":"YOUR_SPOTIFY_USER_ID",
        "spotify_client_id":"YOUR_SPOTIFY_CLIENT_ID",
        "spotify_client_secret":"YOUR_SPOTIFY_CLIENT_SECRET"
    },
    
    "send_gmail": true,
    
    "gmail_sender":{
        "mail_from":"your_gmail_address@gmail.com",
        "mail_to":"your_gmail_address@gmail.com",
        "mail_password":"your gmail app password"
    }
}
```


## Running the application

### With Docker
1. Clone the repository

```bash
git clone https://www.github.com/senceryucel/spotify-follower-tracker
```

2. Run the app

```bash
docker-compose up --build
```

### Without Docker
1. Clone the repository

```bash
git clone https://www.github.com/senceryucel/spotify-follower-tracker
```

2. Install required packages

```bash
pip install -r requirements.txt
```

3. Run the app

```bash
python app.py
```

## TODO
- [ X ] Add support for multiple notification methods (e.g. Discord, Telegram, WhatsApp)
- [ X ] Add support for tracking playlist followers
- [ X ] Add support for tracking new releases

## Contributing
PRs are welcome. 

<br>

***
###### Sencer Yucel, 2024