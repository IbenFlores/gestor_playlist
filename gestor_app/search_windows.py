from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QStackedWidget, QComboBox
)
from playlist_manager import PlaylistManager  # Se asume que el PlaylistManager ya está definido.

class SearchWindowBase(QWidget):
    def __init__(self, hash_table, playlist_manager, switch_to_menu_callback):
        super().__init__()
        self.hash_table = hash_table
        self.playlist_manager = playlist_manager
        self.switch_to_menu_callback = switch_to_menu_callback

        # Layout general
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Resultados de la búsqueda
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

        # Selección de canciones y gestión de playlists
        self.selection_label = QLabel("Select a song to add to a playlist:")
        self.layout.addWidget(self.selection_label)

        self.song_selection = QLineEdit()
        self.song_selection.setPlaceholderText("Enter track ID")
        self.layout.addWidget(self.song_selection)

        self.playlist_label = QLabel("Select or create a playlist:")
        self.layout.addWidget(self.playlist_label)

        self.playlist_selection = QComboBox()
        self.update_playlists()  # Inicializar con las playlists actuales
        self.layout.addWidget(self.playlist_selection)

        self.new_playlist_entry = QLineEdit()
        self.new_playlist_entry.setPlaceholderText("Or create a new playlist")
        self.layout.addWidget(self.new_playlist_entry)

        self.add_to_playlist_button = QPushButton("Add to Playlist")
        self.add_to_playlist_button.clicked.connect(self.add_to_playlist)
        self.layout.addWidget(self.add_to_playlist_button)

        # Botón de regresar
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.switch_to_menu_callback)
        self.layout.addWidget(self.back_button)

    def update_playlists(self):
        """Actualizar las opciones de playlists en el ComboBox."""
        self.playlist_selection.clear()
        self.playlist_selection.addItems(self.playlist_manager.playlists.keys())

    def add_to_playlist(self):
        """Agregar la canción seleccionada a una playlist."""
        track_id = int(self.song_selection.text())
        selected_playlist = self.playlist_selection.currentText()
        new_playlist_name = self.new_playlist_entry.text()

        # Buscar la canción en el hash table por track ID
        song = self.hash_table.search_by_song_id(track_id)
        if not song:
            self.result_text.append("Track ID not found. Please select a valid song.")
            return

        # Si se proporciona un nuevo nombre de playlist, usarlo.
        if new_playlist_name:
            self.playlist_manager.create_playlist(new_playlist_name)
            self.playlist_manager.add_song_to_playlist(new_playlist_name, song)
            self.result_text.append(f"Song added to new playlist '{new_playlist_name}'.")
        else:
            self.playlist_manager.add_song_to_playlist(selected_playlist, song)
            self.result_text.append(f"Song added to playlist '{selected_playlist}'.")

        # Actualizar las playlists en el ComboBox
        self.update_playlists()


class SearchByArtistWindow(SearchWindowBase):
    def __init__(self, hash_table, playlist_manager, switch_to_menu_callback):
        super().__init__(hash_table, playlist_manager, switch_to_menu_callback)

        # Búsqueda por artista
        self.artist_label = QLabel("Enter artist name:")
        self.layout.insertWidget(0, self.artist_label)

        self.artist_entry = QLineEdit()
        self.layout.insertWidget(1, self.artist_entry)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_by_artist)
        self.layout.insertWidget(2, self.search_button)

    def search_by_artist(self):
        artist_name = self.artist_entry.text()
        results = self.hash_table.search_by_artist(artist_name)

        self.result_text.clear()
        if results:
            for song in results:
                self.result_text.append(f"{song.song_id}: {song.artist_name} - {song.track_name} (Popularity: {song.popularity})")
        else:
            self.result_text.append("No songs found for this artist.")


class SearchByTrackNameWindow(SearchWindowBase):
    def __init__(self, hash_table, playlist_manager, switch_to_menu_callback):
        super().__init__(hash_table, playlist_manager, switch_to_menu_callback)

        # Búsqueda por nombre de canción
        self.track_label = QLabel("Enter track name:")
        self.layout.insertWidget(0, self.track_label)

        self.track_entry = QLineEdit()
        self.layout.insertWidget(1, self.track_entry)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_by_track_name)
        self.layout.insertWidget(2, self.search_button)

    def search_by_track_name(self):
        track_name = self.track_entry.text()
        results = self.hash_table.search_by_track_name(track_name)

        self.result_text.clear()
        if results:
            for song in results:
                self.result_text.append(f"{song.song_id}: {song.artist_name} - {song.track_name} (Popularity: {song.popularity})")
        else:
            self.result_text.append("No songs found for this track name.")


class SearchByPopularityWindow(SearchWindowBase):
    def __init__(self, hash_table, playlist_manager, switch_to_menu_callback):
        super().__init__(hash_table, playlist_manager, switch_to_menu_callback)

        # Búsqueda por popularidad
        self.popularity_label = QLabel("Enter minimum and maximum popularity:")
        self.layout.insertWidget(0, self.popularity_label)

        self.min_popularity_entry = QLineEdit()
        self.min_popularity_entry.setPlaceholderText("Minimum popularity")
        self.layout.insertWidget(1, self.min_popularity_entry)

        self.max_popularity_entry = QLineEdit()
        self.max_popularity_entry.setPlaceholderText("Maximum popularity")
        self.layout.insertWidget(2, self.max_popularity_entry)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_by_popularity)
        self.layout.insertWidget(3, self.search_button)

    def search_by_popularity(self):
        min_popularity = self.min_popularity_entry.text()
        max_popularity = self.max_popularity_entry.text()

        try:
            min_popularity = int(min_popularity) if min_popularity else None
            max_popularity = int(max_popularity) if max_popularity else None

            results = self.hash_table.search_by_popularity(min_popularity, max_popularity)

            self.result_text.clear()
            if results:
                for song in results:
                    self.result_text.append(f"{song.song_id}: {song.artist_name} - {song.track_name} (Popularity: {song.popularity})")
            else:
                self.result_text.append("No songs found in this popularity range.")
        except ValueError:
            self.result_text.append("Please enter valid numeric values for popularity.")