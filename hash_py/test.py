from loader import load_songs_from_csv

def main():
    file_path = 'hash_py/spotify_data.csv'  # Replace with the actual path to your CSV file
    hash_table = load_songs_from_csv(file_path)

    # Example usage
    print("Songs by Adele:", hash_table.search_by_artist("Adele"))
    print("Songs with name '93 Million Miles':", hash_table.search_by_track_name("93 Million Miles"))
    print("Songs with popularity between 50 and 90:", hash_table.search_by_popularity(50, 90))
    print("Song with ID 1:", hash_table.search_by_song_id(1))
    print("All songs:", hash_table.all_songs())

if __name__ == "__main__":
    main()