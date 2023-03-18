-- Set the path to the folder containing the Python script
set script_folder to "path/to/folder"

-- Get the currently playing song from Spotify
tell application "Spotify"
	set current_track to the current track
	next track
end tell

-- Get the Spotify URI of the currently playing song
set track_uri to the "" & id of current_track

-- Run the Python script to remove the currently playing song from the default playlist
set command to "python3 controls.py remove " & track_uri
set results to do shell script "cd " & script_folder & "; " & command

-- Uncomment the following line to display the results
-- display dialog results