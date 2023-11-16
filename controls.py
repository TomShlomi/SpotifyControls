import json
import os
import sys

import requests
import spotipy
import spotipy.util as util

# Load secrets from secrets.json
with open("secrets.json") as f:
    secrets = json.load(f)

# Set your Spotify API credentials
SPOTIPY_CLIENT_ID = secrets["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = secrets["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = secrets["SPOTIPY_REDIRECT_URI"]

# Scopes necessary for adding and removing songs from a playlist
username = secrets["username"]
try:
    token = util.prompt_for_user_token(
        username,
        scope="user-library-read playlist-modify-public playlist-modify-private",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )

    # Authenticate with the Spotify API
    sp = spotipy.Spotify(auth=token)
    CONNECTED = True
except requests.exceptions.ConnectionError:
    CONNECTED = False
    token = sp = None

print(f"Connected to Spotify: {CONNECTED}")


def print_playlist(playlist_uri):
    """
    Print the songs in a playlist.

    :param playlist_uri: Spotify URI of the playlist to print
    """
    assert sp is not None

    # Extract playlist ID from the playlist URI
    playlist_id = playlist_uri.split(":")[-1]

    # Initialize variables for pagination
    offset = 0
    limit = 100

    # Loop through the playlist tracks using pagination
    while True:
        playlist_tracks = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        assert playlist_tracks is not None
        for item in playlist_tracks["items"]:
            print(item["track"]["name"] + " by " + item["track"]["artists"][0]["name"])
        if playlist_tracks["next"] is None:
            break
        offset += limit


def add_song_to_playlist(song_uri, playlist_uri=secrets["default_playlist_uri"]):
    """
    Add a song to the specified playlist.

    :param song_uri: Spotify URI of the song to add.
    :param playlist_uri: Spotify URI of the playlist to add the song to
    """
    assert sp is not None
    # Extract playlist ID from the playlist URI
    playlist_id = playlist_uri.split(":")[-1]

    # Extract track ID from the song URI
    track_id = song_uri.split(":")[-1]

    # Add the song to the playlist
    sp.playlist_add_items(playlist_id, [track_id])


def remove_song_from_playlist(song_uri, playlist_uri=secrets["default_playlist_uri"]):
    """
    Remove a song from the specified playlist.

    :param song_uri: Spotify URI of the song to remove.
    :param playlist_uri: Spotify URI of the playlist to remove the song from
    """
    assert sp is not None
    playlist_id = playlist_uri.split(":")[-1]
    track_id = song_uri.split(":")[-1]

    # Initialize variables for pagination
    offset = 0
    limit = 100
    position_to_remove = None

    # Loop through the playlist tracks using pagination
    while True:
        playlist_tracks = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        assert playlist_tracks is not None
        for i, item in enumerate(playlist_tracks["items"]):
            if item["track"]["id"] == track_id:
                position_to_remove = offset + i
                break
        if position_to_remove is not None or playlist_tracks["next"] is None:
            break
        offset += limit

    if position_to_remove is not None:
        # Remove the song from the specified position
        tracks_to_remove = [{"uri": track_id, "positions": [position_to_remove]}]
        sp.playlist_remove_specific_occurrences_of_items(playlist_id, tracks_to_remove)
    else:
        print(f"Could not find song {song_uri} in playlist {playlist_uri}.")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        command = sys.argv[1]
        song_uri = sys.argv[2]
        print(f"{command} {song_uri}")
    else:
        # Throw an error if no song URI is provided
        print("Must provide a command (add or remove) and a song URI")
        sys.exit()

    # Ensure commands.json exists
    if not os.path.isfile("commands.json"):
        with open("commands.json", "w") as f:
            json.dump([], f)

    # Load all unexcecuted commands from commands.json. It must be a list of dictionaries, where each dictionary has a "command" and "song_uri" key.
    commands: list[dict[str, str]] = json.load(open("commands.json"))
    assert isinstance(commands, list) and all(
        isinstance(command, dict) and "command" in command and "song_uri" in command
        for command in commands
    )

    # Add the current command to the commands dictionary
    commands += [{"command": command, "song_uri": song_uri}]

    # Execute the commands if connected to the internet
    if CONNECTED:
        print(commands)
        while commands:
            d = commands.pop()
            try:
                if d["command"] == "add":
                    add_song_to_playlist(d["song_uri"])
                elif d["command"] == "remove":
                    remove_song_from_playlist(d["song_uri"])
                else:
                    print(f"Unrecognized command {d['command']}")
            except requests.exceptions.ConnectionError:
                print("Connection failed")
                commands.append(d)
                break

    # Save the commands dataframe to commands.json
    json.dump(commands, open("commands.json", "w"))
