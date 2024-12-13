# Spotify Playlist Controls

This repository contains a Python script and two AppleScript files that allow you to easily add or remove the currently playing song on Spotify to/from a default playlist.

## Files

- `controls.py`: A Python script that handles adding and removing songs from a playlist.
- `template.addsong.applescript`: A template for an AppleScript that adds the currently playing song to the default playlist.
- `template.removesong.applescript`: A template for an AppleScript that removes the currently playing song from the default playlist. 
- `template.secrets.json`: A template for a JSON file that contains your Spotify API credentials.

## Setup

1. Clone this repository. 
    ``` 
    git clone https://github.com/TomShlomi/SpotifyControls.git
    cd SpotifyControls
    ```
2. Install `uv`
3. Rename `template.secrets.json` to `secrets.json` and update the contents with your Spotify API credentials, username, and default playlist URI. You can obtain your API credentials by registering a new app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications). 

At this point, you can add or remove a song from your default playlist by running the following respective command in the repository's directory:
```
uv run controls.py add SONG_URI
```
```
uv run controls.py remove SONG_URI
```
where `SONG_URI` is the URI of the song you want to add or remove. You can obtain the URI of a song by right-clicking on it in Spotify, holding down the option key, and selecting "Copy Spotify URI". Songs can only be added or removed when you have an internet connection. If you run these commands while you don't have a connection, it will store the commands in command.json and excecute them all the next time you run a command while having internet.

4. Replace `"path/to/folder"` in both AppleScript files with the path to this repository's location on your computer and `"path/to/uv"` with the absolute path to your `uv` executable, and rename the files to `addsong.applescript` and `removesong.applescript` respectively.

At this point you can add or remove a song from your default playlist by running the following respective command in any directory:
```
osascript /path/to/folder/addsong.applescript
```
```
osascript /path/to/folder/removesong.applescript
```

5. Create two Quick Actions in Automator (installed by default on macOS), select "Run AppleScript" as the action, copy the contents of `addsong.applescript` and `removesong.applescript` into the respective Quick Actions, and save them.
6. Open System Preferences > Keyboard > Shortcuts > Services
7. Scroll down to the "General" section, and you should see your newly created Quick Actions. Click on the action you want to create a keyboard shortcut for, and then click "Add Shortcut" to set the desired key combination.

Now you can add or remove a song from your default playlist by pressing the respective key combination.
