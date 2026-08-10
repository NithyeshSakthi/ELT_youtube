import requests
import json
import os
from dotenv import load_dotenv

#load the variable paths
load_dotenv(dotenv_path = ".env")
API_KEY = os.getenv("API_KEY")
CHANNEL = "MrBeast"
maxResults = 50 #add item want per page

#get the playlist_id
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
 

#get the video_ids
def get_video_ids(playlistId):
    video_ids = []
    pageToken = None
    #Find the videos inside the playlist
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
            #find the video id
            for item in data.get("items",[]):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            pageToken = data.get('nextPageToken')
            if not pageToken:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e
def batch_list(video_id_lst, batch_size):
    for video_id in range(0, len(video_id_lst), batch_size):
        yield video_id_lst[video_id: video_id + batch_size]

def extract_video_data(video_ids):

    extracted_data = []

    def batch_list(video_id_lst, batch_size):
        for video_id in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[video_id: video_id + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)

            url =f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}'

            response = requests.get(url)
            response.raise_for_status()   
            data = response.json()   

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
                
                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    "viewCount": statistics.get('viewCount', None),
                    "likeCount": statistics.get('likeCount', None),
                    "commentCount": statistics.get('CommentCount', None)
                }  
                extracted_data.append(video_data)
        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e
if __name__ == "__main__":  
    #print("API KEY:", API_KEY)
    #print("Playlist ID:", get_playlist_id())
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    print(extract_video_data(video_ids))
    

