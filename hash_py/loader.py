import csv
from song import Song
from song_hash_table import SongHashTable

def load_songs_from_csv(file_path):
    hash_table = SongHashTable()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            song = Song(
                int(row['']), row['artist_name'], row['track_name'], row['track_id'],
                int(row['popularity']), int(row['year']), row['genre'],
                float(row['danceability']), float(row['energy']), int(row['key']),
                float(row['loudness']), int(row['mode']), float(row['speechiness']),
                float(row['acousticness']), float(row['instrumentalness']), 
                float(row['liveness']), float(row['valence']), float(row['tempo']),
                int(row['duration_ms']), int(row['time_signature'])
            )
            hash_table.insert(song)
    return hash_table