import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from loader import load_songs_into_hash_table
from search_windows import SearchByArtistWindow, SearchByPopularityWindow, SearchByTrackNameWindow
from playlist_manager import PlaylistManager
from playlist_loader import load_playlists_from_folder
from playlist_windows import PlaylistListWindow
from playlist_windows import PlaylistDetailWindow
from PyQt6.QtCore import QThread

class MainWindow(QMainWindow):
    def __init__(self, playlist_manager, switch_to_menu_callback):
        super().__init__()
        self.setWindowTitle("Song Search App")
        self.setGeometry(100, 100, 800, 600)
        
        # Inicialización de variables
        self.hash_table = {}  # Se llenará tras cargar las canciones
        self.playlist_manager = playlist_manager
        
        # Central widget con un stacked layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.stacked_widget = QStackedWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.stacked_widget)

        # Callback para volver al menú
        self.switch_to_menu_callback = switch_to_menu_callback

        # Crear el menú principal
        self.menu_widget = self.create_menu()
        self.stacked_widget.addWidget(self.menu_widget)
        self.stacked_widget.setCurrentWidget(self.menu_widget)

        # Ventanas de búsqueda (se inicializarán después de cargar los datos)
        self.search_by_artist_window = None
        self.search_by_track_name_window = None
        self.search_by_popularity_window = None

        # Ventanas de gestión de playlists
        self.playlist_window = None
        self.playlist_detail_window = None

        # Cargar canciones de manera asincrónica
        self.load_songs()

    def create_menu(self):
        menu_widget = QWidget()
        layout = QVBoxLayout(menu_widget)

        # Botones de navegación
        artist_button = QPushButton("Search by Artist")
        artist_button.clicked.connect(self.show_search_by_artist)
        layout.addWidget(artist_button)

        track_button = QPushButton("Search by Track Name")
        track_button.clicked.connect(self.show_search_by_track_name)
        layout.addWidget(track_button)

        popularity_button = QPushButton("Search by Popularity")
        popularity_button.clicked.connect(self.show_search_by_popularity)
        layout.addWidget(popularity_button)

        playlists_button = QPushButton("View Playlists")
        playlists_button.clicked.connect(self.view_playlists)
        layout.addWidget(playlists_button)

        return menu_widget

    def show_search_by_artist(self):
        if self.search_by_artist_window:
            self.stacked_widget.setCurrentWidget(self.search_by_artist_window)

    def show_search_by_track_name(self):
        if self.search_by_track_name_window:
            self.stacked_widget.setCurrentWidget(self.search_by_track_name_window)

    def show_search_by_popularity(self):
        if self.search_by_popularity_window:
            self.stacked_widget.setCurrentWidget(self.search_by_popularity_window)

    def view_playlists(self):
        if not self.playlist_window:
            self.playlist_window = PlaylistListWindow(
                self.playlist_manager,
                self.open_playlist,
                self.switch_to_menu_callback
            )
            self.stacked_widget.addWidget(self.playlist_window)
        self.stacked_widget.setCurrentWidget(self.playlist_window)

    def open_playlist(self, playlist_name):
        playlist_window = PlaylistDetailWindow(
            playlist_name,
            self.playlist_manager,
            lambda: self.stacked_widget.setCurrentWidget(self.menu_widget)
        )
        self.stacked_widget.addWidget(playlist_window)
        self.stacked_widget.setCurrentWidget(playlist_window)

    def load_songs(self):
        """Cargar canciones en la tabla hash de manera asincrónica."""
        file_path = 'spotify_data.csv'
        self.loader = load_songs_into_hash_table(file_path)
        self.loader.data_loaded.connect(self.on_songs_loaded)
        self.loader.start()

    def on_songs_loaded(self, hash_table):
        """Actualizar la tabla hash y crear las ventanas de búsqueda."""
        self.hash_table = hash_table
        print("Songs loaded successfully.")

        # Crear ventanas de búsqueda con los datos cargados
        self.search_by_artist_window = SearchByArtistWindow(self.hash_table, self.playlist_manager, self.switch_to_menu_callback)
        self.search_by_track_name_window = SearchByTrackNameWindow(self.hash_table, self.playlist_manager, self.switch_to_menu_callback)
        self.search_by_popularity_window = SearchByPopularityWindow(self.hash_table, self.playlist_manager, self.switch_to_menu_callback)

        # Agregar las ventanas al stacked widget
        self.stacked_widget.addWidget(self.search_by_artist_window)
        self.stacked_widget.addWidget(self.search_by_track_name_window)
        self.stacked_widget.addWidget(self.search_by_popularity_window)

        # Inicializar las playlists
        self.load_playlists()

    def load_playlists(self):
        """Cargar las playlists desde una carpeta."""
        folder_path = 'playlists'
        try:
            playlists = load_playlists_from_folder(folder_path)
            for name, songs in playlists.items():
                self.playlist_manager.playlists[name] = songs
            print("Playlists loaded successfully.")
        except FileNotFoundError:
            print(f"Folder '{folder_path}' not found. No playlists loaded.")
        except Exception as e:
            print(f"Error loading playlists: {e}")

    def closeEvent(self, event):
        """Guardar playlists antes de cerrar la aplicación."""
        print("Saving playlists...")
        try:
            for playlist_name in self.playlist_manager.playlists.keys():
                self.playlist_manager.save_playlist_to_csv(playlist_name)
            print("Playlists saved successfully.")
        except Exception as e:
            print(f"Error saving playlists: {e}")
        event.accept()  # Cerrar la ventana

if __name__ == '__main__':
    app = QApplication(sys.argv)
    playlist_manager = PlaylistManager()
    main_window = MainWindow(playlist_manager, lambda: main_window.stacked_widget.setCurrentWidget(main_window.menu_widget))
    main_window.show()
    sys.exit(app.exec())
