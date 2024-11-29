from queue import Queue
import random
from song import Song

class PlaylistManager:
    def __init__(self):
        self.playlists = {}
        self.playback_queue = Queue()  # Cola para la reproducción
    
    def create_playlist(self, playlist_name):
        """Crear una nueva playlist."""
        if playlist_name not in self.playlists:
            self.playlists[playlist_name] = []
        else:
            print(f"La playlist '{playlist_name}' ya existe.")
    
    def add_song_to_playlist(self, playlist_name, song):
        """Agregar una canción a la playlist."""
        if playlist_name in self.playlists:
            self.playlists[playlist_name].append(song)
        else:
            print(f"La playlist '{playlist_name}' no existe.")
    
    def list_songs_in_playlist(self, playlist_name):
        """Listar todas las canciones de una playlist."""
        if playlist_name in self.playlists:
            return self.playlists[playlist_name]
        else:
            print(f"La playlist '{playlist_name}' no existe.")
            return []

    def select_random_song(self, playlist_name):
        """Seleccionar una canción al azar de una playlist."""
        if playlist_name in self.playlists and self.playlists[playlist_name]:
            random_song = random.choice(self.playlists[playlist_name])
            print(f"Canción seleccionada al azar: {random_song}")
            return random_song
        else:
            print(f"La playlist '{playlist_name}' está vacía o no existe.")
            return None

    def generate_playback_queue(self, playlist_name, starting_song=None, queue_length=10):
        """
        Generar una cola de reproducción a partir de una canción inicial al azar.
        :param playlist_name: Nombre de la playlist.
        :param starting_song: Canción inicial, si es None selecciona al azar.
        :param queue_length: Número de canciones en la cola, incluida la inicial.
        """
        if playlist_name not in self.playlists or not self.playlists[playlist_name]:
            print(f"La playlist '{playlist_name}' está vacía o no existe.")
            return

        songs = self.playlists[playlist_name]
        if starting_song is None:
            starting_song = self.select_random_song(playlist_name)

        self.playback_queue = Queue()  # Reiniciar la cola de reproducción
        if starting_song:
            self.playback_queue.enqueue(starting_song)

        available_songs = [song for song in songs if song != starting_song]

        while len(self.playback_queue) < queue_length and available_songs:
            next_song = random.choice(available_songs)
            self.playback_queue.enqueue(next_song)
            available_songs.remove(next_song)

        print("Cola de reproducción generada:")
        for idx, song in enumerate(self.playback_queue, start=1):
            print(f"{idx}: {song}")

    def play_next(self):
        """Reproducir la siguiente canción de la cola."""
        if not self.playback_queue.is_empty():
            next_song = self.playback_queue.dequeue()
            print(f"Reproduciendo: {next_song}")
            return next_song
        else:
            print("La cola de reproducción está vacía.")
            return None