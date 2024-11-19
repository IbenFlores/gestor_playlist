from loader import load_songs_from_csv

def main():
    file_path = 'hash_py/spotify_data.csv'
    hash_table = load_songs_from_csv(file_path)

    print("Canciones de Meiko:", hash_table.search_by_artist("Meiko"))
    print("Cancion con nombre ('Out Loud'):", hash_table.search_by_track_name("Out Loud"))
    print("Cancion con ID 93:", hash_table.search_by_song_id(93))

if __name__ == "__main__":
    main()