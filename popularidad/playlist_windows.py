from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QStackedWidget, QHBoxLayout
from PyQt6.QtCore import QRandomGenerator
from queue import Queue
from song import Song
import random

class PlaylistListWindow(QWidget):
    def __init__(self, playlist_manager, open_playlist_callback, switch_to_menu_callback):
        """
        Ventana para mostrar la lista de playlists.
        :param playlist_manager: Instancia de PlaylistManager para manejar las playlists.
        :param open_playlist_callback: Función para abrir una playlist específica.
        :param switch_to_menu_callback: Función para volver al menú principal.
        """
        super().__init__()
        self.playlist_manager = playlist_manager
        self.open_playlist_callback = open_playlist_callback
        self.switch_to_menu_callback = switch_to_menu_callback
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz gráfica de la ventana."""
        self.setWindowTitle("Playlists")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout(self)

        # Lista de playlists
        self.playlist_list_widget = QListWidget()
        self.update_playlist_list()
        layout.addWidget(self.playlist_list_widget)

        # Botones
        button_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.switch_to_menu_callback)

        open_button = QPushButton("Open Playlist")
        open_button.clicked.connect(self.open_selected_playlist)

        button_layout.addWidget(back_button)
        button_layout.addWidget(open_button)
        layout.addLayout(button_layout)

    def update_playlist_list(self):
        """Actualizar la lista de playlists mostrada."""
        self.playlist_list_widget.clear()
        for playlist_name in self.playlist_manager.playlists.keys():
            self.playlist_list_widget.addItem(playlist_name)

    def open_selected_playlist(self):
        """Abrir la playlist seleccionada."""
        selected_item = self.playlist_list_widget.currentItem()
        if selected_item:
            playlist_name = selected_item.text()
            self.open_playlist_callback(playlist_name)


class PlaylistDetailWindow(QWidget):
    def __init__(self, playlist_name, playlist_manager, switch_to_menu_callback):
        """
        Ventana para mostrar los detalles de una playlist específica.
        :param playlist_name: Nombre de la playlist.
        :param playlist_manager: Instancia de PlaylistManager para manejar las playlists.
        :param switch_to_menu_callback: Función para volver al menú principal.
        """
        super().__init__()
        self.playlist_manager = playlist_manager
        self.switch_to_menu_callback = switch_to_menu_callback
        self.current_playlist_name = playlist_name  # Almacena el nombre de la playlist actual
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz gráfica de la ventana."""
        self.setWindowTitle(f"Playlist: {self.current_playlist_name}")
        self.setGeometry(100, 100, 600, 400)

        # Layout principal
        layout = QVBoxLayout(self)

        # Título de la playlist
        playlist_label = QLabel(f"Playlist: {self.current_playlist_name}")
        playlist_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(playlist_label)

        # Lista de canciones
        self.song_list_widget = QListWidget()
        self.update_song_list()
        layout.addWidget(self.song_list_widget)

        # Botones
        button_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.switch_to_menu_callback)

        random_button = QPushButton("Play Random Song")
        random_button.clicked.connect(self.play_random_song)

        button_layout.addWidget(back_button)
        button_layout.addWidget(random_button)
        layout.addLayout(button_layout)

    def update_song_list(self):
        """Actualiza la lista de canciones mostrada en la interfaz."""
        self.song_list_widget.clear()
        songs = self.playlist_manager.list_songs_in_playlist(self.current_playlist_name)
        for song in songs:
            self.song_list_widget.addItem(str(song))

    def play_random_song(self):
        """
        Selecciona una canción al azar de la playlist actual, genera una cola de reproducción,
        y muestra la lista en una ventana temporal.
        """
        if not self.current_playlist_name:
            print("No playlist selected.")
            return

        # Obtener una canción al azar
        random_song = self.playlist_manager.select_random_song(self.current_playlist_name)
        if random_song:
            # Crear una cola aleatoria con el resto de las canciones
            songs_in_playlist = self.playlist_manager.list_songs_in_playlist(self.current_playlist_name)
            remaining_songs = [song for song in songs_in_playlist if song != random_song]
            random.shuffle(remaining_songs)

            # Crear la ventana con la lista de reproducción
            self.show_song_details_with_queue(random_song, remaining_songs)


    def show_song_details_with_queue(self, current_song, queue_songs):
        """
        Muestra una ventana con los detalles de la canción seleccionada y una cola de reproducción.
        :param current_song: La canción seleccionada para reproducir.
        :param queue_songs: Lista de canciones restantes en la cola.
        """
        # Crear una nueva ventana para mostrar la canción y la cola
        self.playback_window = QWidget()  # Crear la ventana como atributo de la clase
        self.playback_window.setWindowTitle("Now Playing")
        self.playback_window.setGeometry(100, 100, 400, 500)

        # Layout principal
        layout = QVBoxLayout(self.playback_window)

        # Detalles de la canción actual
        song_name_label = QLabel(f"Now Playing: {current_song.track_name}")
        song_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        song_name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(song_name_label)

        duration_minutes = current_song.duration_ms // 60000
        duration_seconds = (current_song.duration_ms % 60000) // 1000
        duration_label = QLabel(f"Duration: {duration_minutes} min {duration_seconds} sec")
        duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(duration_label)

        artist_label = QLabel(f"Artist: {current_song.artist_name}")
        artist_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(artist_label)

        # Lista de reproducción (queue)
        queue_label = QLabel("Queue:")
        queue_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        queue_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(queue_label)

        queue_list_widget = QListWidget()
        for idx, song in enumerate(queue_songs, start=1):
            duration_minutes = song.duration_ms // 60000
            duration_seconds = (song.duration_ms % 60000) // 1000
            queue_list_widget.addItem(
                f"{idx}. {song.track_name} by {song.artist_name} ({duration_minutes}:{duration_seconds:02d})"
            )
        layout.addWidget(queue_list_widget)

        # Botón para cerrar la ventana
        back_button = QPushButton("Close")
        back_button.clicked.connect(self.playback_window.close)  # Cierra la ventana
        layout.addWidget(back_button)

        # Mostrar la ventana
        self.playback_window.show()