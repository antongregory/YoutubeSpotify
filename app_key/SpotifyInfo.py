import urllib.parse


""" Add the client id and client secret information from your spotify dev"""
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = 'http://example.com/callback/'

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
SPOTIFY_API_ACCOUNT_URL = 'http://accounts.spotify.com/authorize'

SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, 'v1')
SPOTIFY_PLAYLIST_URL = "{}/v1/me/tracks".format(SPOTIFY_API_BASE_URL)

SCOPE = " ".join(['playlist-read-collaborative','playlist-read-private', 'user-library-read'])

client_info = {'client_id': CLIENT_ID,
               'response_type': 'code',
               'scope': SCOPE,
               'redirect_uri':REDIRECT_URI,
               'state':'34fFs29kd09'
               }

CLIENT_INFO_ENCODED = urllib.parse.urlencode(client_info)


SPOTIFY_AUTHREQUEST_URL = "{}?{}".format(SPOTIFY_API_ACCOUNT_URL,CLIENT_INFO_ENCODED)

