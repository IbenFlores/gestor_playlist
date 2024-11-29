# hash_table.py
class SongHashTable:
    def __init__(self):
        self.by_artist = {}
        self.by_track_name = {}
        self.by_popularity = {}
        self.by_song_id = {}

    def insert(self, song):
        """Inserta una canción en los diccionarios de la hash table."""
        if song.song_id not in self.by_song_id:
            self.by_song_id[song.song_id] = song

        # Insertar por artista
        if song.artist_name not in self.by_artist:
            self.by_artist[song.artist_name] = []
        self.by_artist[song.artist_name].append(song)

        # Insertar por nombre de canción
        if song.track_name not in self.by_track_name:
            self.by_track_name[song.track_name] = []
        self.by_track_name[song.track_name].append(song)

        # Insertar por popularidad
        if song.popularity not in self.by_popularity:
            self.by_popularity[song.popularity] = []
        self.by_popularity[song.popularity].append(song)
    
    def search_by_artist(self, artist_name):
        """Buscar canciones cuyo nombre del artista comienza con el nombre proporcionado."""
        results = []
        for artist in self.by_artist.keys():
            if artist.lower().startswith(artist_name.lower()):
                for song in self.by_artist[artist]:
                    results.append(song)
        return results

    def search_by_track_name(self, track_name):
        return self.by_track_name.get(track_name, [])
    
    def search_by_track_name(self, track_name):
        """Buscar canciones cuyo nombre de la pista comienza con el nombre proporcionado."""
        results = []
        for name in self.by_track_name.keys():  # Usamos el método all_songs
            if name.lower().startswith(track_name.lower()):
                for song in self.by_track_name[name]:
                    results.append(song)
        return results

    def search_by_popularity(self, min_popularity=None, max_popularity=None):
        results = []
        for popularity, songs in self.by_popularity.items():
            if (min_popularity is None or popularity >= min_popularity) and \
               (max_popularity is None or popularity <= max_popularity):
                results.extend(songs)
        return results

    def search_by_song_id(self, song_id):
        return self.by_song_id.get(song_id, None)