import base64
import json
import sys

import requests

from app_key import SpotifyInfo

auth_header = None


def authorize():
    print("Please visit this URL to authorize this application:",
          SpotifyInfo.SPOTIFY_AUTHREQUEST_URL)

    auth_code = input("Enter the authorization code:")

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_code),
        "redirect_uri": SpotifyInfo.REDIRECT_URI
    }

    # python 3 or above
    if sys.version_info[0] >= 3:
        base64encoded = base64.b64encode(("{}:{}".format(SpotifyInfo.CLIENT_ID,
                                                         SpotifyInfo.CLIENT_SECRET)).encode())
        headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    else:
        base64encoded = base64.b64encode("{}:{}".format(SpotifyInfo.CLIENT_ID, SpotifyInfo.CLIENT_SECRET))
        headers = {"Authorization": "Basic {}".format(base64encoded)}

    post_request = requests.post(SpotifyInfo.SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # use the access token to access Spotify API

    return {"Authorization": "Bearer {}".format(access_token)}


def get_liked_songs():
    global auth_header
    if auth_header is None:
        auth_header = authorize()

    response = requests.get(SpotifyInfo.SPOTIFY_PLAYLIST_URL, headers=auth_header)

    response_json = response.json()
    liked_songs = []
    for song_info in response_json["items"]:
        liked_songs.append((song_info['track']['name'] + " ") + (song_info['track']['album']['name']))

    return liked_songs


if __name__ == "__main__":
    # auth_header = authorize()
    # url = SpotifyInfo.SPOTIFY_PLAYLIST_URL
    #
    # resp = requests.get(url, headers=auth_header)
    # # print(resp.text)
    get_liked_songs()
