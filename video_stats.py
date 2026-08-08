import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path = ".env")
API_KEY = os.getenv("API_KEY")
CHANNEL = "MrBeast"
maxResults = 50 #add the max page

def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL}&key={API_KEY}"

        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        #print(response)
        data = response.json()
        #print(json.dumps(data, indent=4))

        channel_items = data["items"][0]
        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        #print(channel_playlistsId)
        return channel_playlistId

    except requests.exceptions.RequestException as e:
        raise e
        #print(f"Error occurred while making the request: {e}")
 


def get_video_ids(playlistId):
    video_ids = []
    pageToken = None

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"
    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
                #print(response)
            data = response.json()
                #print(json.dumps(data, indent=4))
            for item in data.get("items",[]):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            pageToken = data.get('nextPageToken')
            if not pageToken:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e



if __name__ == "__main__":
    playlistId = get_playlist_id()
    print(get_video_ids(playlistId))
    print("API KEY:", API_KEY)
    print("Playlist ID:", get_playlist_id())
