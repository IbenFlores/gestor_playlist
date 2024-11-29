from playlist_loader import load_playlists_from_folder

folder_path = 'playlists'
playlists = load_playlists_from_folder(folder_path)

for playlist_name, songs in playlists.items():
    print(f"Playlist: {playlist_name}")
    for song in songs:
        print(song)