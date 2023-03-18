import spotipy
import spotipy.util as util
import sys
import json

# Load secrets from secrets.json
with open('secrets.json') as f:
    secrets = json.load(f)

# Set your Spotify API credentials
SPOTIPY_CLIENT_ID = secrets['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = secrets['SPOTIPY_CLIENT_SECRET']
SPOTIPY_REDIRECT_URI = secrets['SPOTIPY_REDIRECT_URI']

# Scopes necessary for adding and removing songs from a playlist
username = secrets['username']
token = util.prompt_for_user_token(username, scope="user-library-read playlist-modify-public playlist-modify-private", client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

# Authenticate with the Spotify API
sp = spotipy.Spotify(auth=token)

def add_song_to_playlist(song_uri, playlist_uri=secrets['default_playlist_uri']):
    """
    Add a song to the specified playlist.

    :param song_uri: Spotify URI of the song to add.
    :param playlist_uri: Spotify URI of the playlist to add the song to
    """
    # Extract playlist ID from the playlist URI
    playlist_id = playlist_uri.split(':')[-1]

    # Extract track ID from the song URI
    track_id = song_uri.split(':')[-1]

    # Add the song to the playlist
    sp.playlist_add_items(playlist_id, [track_id])

def remove_song_from_playlist(song_uri, playlist_uri=secrets['default_playlist_uri']):
    """
    Remove a song from the specified playlist.

    :param song_uri: Spotify URI of the song to remove.
    :param playlist_uri: Spotify URI of the playlist to remove the song from
    """
    playlist_id = playlist_uri.split(':')[-1]
    track_id = song_uri.split(':')[-1]

    # Initialize variables for pagination
    offset = 0
    limit = 100
    position_to_remove = None

    # Loop through the playlist tracks using pagination
    while True:
        playlist_tracks = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        for i, item in enumerate(playlist_tracks['items']):
            if item['track']['id'] == track_id:
                position_to_remove = offset + i
                break
        if position_to_remove is not None or playlist_tracks['next'] is None:
            break
        offset += limit

    if position_to_remove is not None:
        # Remove the song from the specified position
        tracks_to_remove = [{
            'uri': track_id,
            'positions': [position_to_remove]
        }]
        sp.playlist_remove_specific_occurrences_of_items(playlist_id, tracks_to_remove)
    else:
        print(f"Could not find song {song_uri} in playlist {playlist_uri}.")

if __name__ == '__main__':
    if len(sys.argv) > 2:
        command = sys.argv[1]
        song_uri = sys.argv[2]
    else:
        # Throw an error if no song URI is provided
        print("Must provide a command (add or remove) and a song URI")
        sys.exit()

    if command == 'add':
        add_song_to_playlist(song_uri)
    elif command == 'remove':
        remove_song_from_playlist(song_uri)
    else:
        print("Command not recognized.")
        sys.exit()
        