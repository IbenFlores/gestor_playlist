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

        # Sanitizar el nombre del artista
        artist_name = str(song.artist_name).strip() if song.artist_name else ""
        if artist_name not in self.by_artist:
            self.by_artist[artist_name] = []
        self.by_artist[artist_name].append(song)

        # Sanitizar el nombre de la canción
        track_name = str(song.track_name).strip() if song.track_name else ""
        if track_name not in self.by_track_name:
            self.by_track_name[track_name] = []
        self.by_track_name[track_name].append(song)

        # Insertar por popularidad
        if song.popularity not in self.by_popularity:
            self.by_popularity[song.popularity] = []
        self.by_popularity[song.popularity].append(song)

    def search_by_artist(self, artist_name):
        """Buscar canciones cuyo nombre del artista comienza con el nombre proporcionado."""
        results = []
        if not artist_name:  # Si el parámetro es None o vacío
            return results

        artist_name = str(artist_name).strip().lower()
        for artist in self.by_artist.keys():
            artist_sanitized = str(artist).strip().lower()
            if artist_sanitized.startswith(artist_name):
                results.extend(self.by_artist[artist])
        return results


    def search_by_track_name(self, track_name):
        return self.by_track_name.get(track_name, [])
    
    def search_by_track_name(self, track_name):
        """Buscar canciones cuyo nombre de la pista comienza con el nombre proporcionado."""
        results = []
        if not track_name:  # Si el parámetro es None o vacío
            return results

        track_name = str(track_name).strip().lower()
        for name in self.by_track_name.keys():
            name_sanitized = str(name).strip().lower()
            if name_sanitized.startswith(track_name):
                results.extend(self.by_track_name[name])
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