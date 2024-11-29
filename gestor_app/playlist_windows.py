from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QStackedWidget, QHBoxLayout
from PyQt6.QtCore import QRandomGenerator
from queue import Queue
from song import Song

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
        Selecciona una canción al azar de la playlist actual y la agrega a la cola de reproducción.
        """
        if not self.current_playlist_name:
            print("No playlist selected.")
            return

        random_song = self.playlist_manager.select_random_song(self.current_playlist_name)
        if random_song:
            self.playlist_manager.playback_queue.enqueue(random_song)
            print(f"Added to queue: {random_song}")