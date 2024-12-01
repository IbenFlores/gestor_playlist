# song.py
class Song:
    def __init__(self, song_id, artist_name, track_name, track_id, popularity, year, genre, danceability, energy,
                 key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo,
                 duration_ms, time_signature):
        self.song_id = int(song_id)
        self.artist_name = artist_name
        self.track_name = track_name
        self.track_id = track_id
        self.popularity = int(popularity)
        self.year = int(year)
        self.genre = genre
        self.danceability = float(danceability)
        self.energy = float(energy)
        self.key = int(key)
        self.loudness = float(loudness)
        self.mode = int(mode)
        self.speechiness = float(speechiness)
        self.acousticness = float(acousticness)
        self.instrumentalness = float(instrumentalness)
        self.liveness = float(liveness)
        self.valence = float(valence)
        self.tempo = float(tempo)
        self.duration_ms = int(duration_ms)
        self.time_signature = int(time_signature)

    def __repr__(self):
        return f"Song(ID={self.song_id}, Track={self.track_name}, Artist={self.artist_name})"