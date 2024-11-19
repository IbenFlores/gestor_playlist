from song import Song

class SongHashTable:
    def __init__(self):
        # Diccionarios para cada atributo que deseamos buscar
        self.by_artist = {}
        self.by_track_name = {}
        self.by_popularity = {}
        self.by_song_id = {}

    def insert(self, song):
        # Insercion al diccionario por ID de cancion
        if song.song_id in self.by_song_id:
            print(f"Duplicate song_id detected: {song.song_id}. Ignoring.")
            return
        self.by_song_id[song.song_id] = song

        # Insercion al diccionario por nombre de artista
        if song.artist_name not in self.by_artist:
            self.by_artist[song.artist_name] = []
        self.by_artist[song.artist_name].append(song)

        # Insercion al diccionario por nombre de cancion
        if song.track_name not in self.by_track_name:
            self.by_track_name[song.track_name] = []
        self.by_track_name[song.track_name].append(song)

        # Insercion al diccionario por popularidad
        if song.popularity not in self.by_popularity:
            self.by_popularity[song.popularity] = []
        self.by_popularity[song.popularity].append(song)

    def search_by_artist(self, artist_name):
        return self.by_artist.get(artist_name, [])

    def search_by_track_name(self, track_name):
        return self.by_track_name.get(track_name, [])

    def search_by_popularity(self, min_popularity=None, max_popularity=None):
        results = []
        for popularity, songs in self.by_popularity.items():
            if (min_popularity is None or popularity >= min_popularity) and \
               (max_popularity is None or popularity <= max_popularity):
                results.extend(songs)
        return results

    def search_by_song_id(self, song_id):
        return self.by_song_id.get(song_id, None)

    def all_songs(self):
        return list(self.by_song_id.values())