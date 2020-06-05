import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from spotify_api import get_liked_songs

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

PLAYLIST_NAME = "Spotify Collection"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "app_key/client_info.json"


def get_youtube_client():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes)
    credentials = flow.run_console()
    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)


def get_playlist_id():
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        maxResults=25,
        mine=True
    )
    response = request.execute()
    playlist_id = 0

    for playlist_items in response["items"]:
        if playlist_items["snippet"]["title"] == PLAYLIST_NAME:
            playlist_id = playlist_items["id"]
            break

    if playlist_id == 0:
        playlist_id = create_playlist()

    return playlist_id


def create_playlist():
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": PLAYLIST_NAME,
                "description": "Spotify liked songs",
                "tags": [
                    "Created by YoutubeSpotiifyConnect app",
                    "API call"
                ],
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    )
    response = request.execute()
    return response["id"]


def add_songs_to_playlist(tracks, my_playlist):
    """ Add the youtube videos to the playlist """

    print("Adding songs to playlist")
    current_videos = get_existing_songs_in_playlist(my_playlist)

    try:
        for track in tracks:
            print("Adding track " + track)
            if track in current_videos:
                print("Already exist", track)
                continue

            request = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": my_playlist,
                        "position": 0,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": track
                        }
                    }
                }
            )
            request.execute()
    except Exception as e:
        print("Could not complete the process due to error", e)

    pass


def get_existing_songs_in_playlist(playlist):
    existing_videos = []
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist
    )
    response = request.execute()

    if response['items'] is None:
        return existing_videos

    for track in response['items']:
        existing_videos.append(track['contentDetails']['videoId'])

    print(existing_videos)
    return existing_videos


def get_youtube_videos(tracks):
    items = []
    for track in tracks:
        request = youtube.search().list(
            part="snippet",
            maxResults=1,
            q=track
        )
        response = request.execute()
        print("Fetching .....")
        items.append(response['items'][0]['id']['videoId'])

    return items


if __name__ == "__main__":
    # get the liked songs from spotify
    liked_songs = get_liked_songs()

    # create youtube client
    youtube = get_youtube_client()

    # get the youtube videos of spotify liked songs
    youtube_videos = get_youtube_videos(liked_songs)

    # create or use existing playlist
    playlist = get_playlist_id()

    # add songs to playlist
    add_songs_to_playlist(youtube_videos, playlist)
