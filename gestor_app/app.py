import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from loader import load_songs_into_hash_table
from search_windows import SearchByArtistWindow, SearchByPopularityWindow, SearchByTrackNameWindow
from playlist_manager import PlaylistManager
from playlist_loader import load_playlists_from_folder
from playlist_windows import PlaylistListWindow
from playlist_windows import PlaylistDetailWindow


class MainWindow(QMainWindow):
    def __init__(self, hash_table, playlist_manager, switch_to_menu_callback):
        super().__init__()
        self.setWindowTitle("Song Search App")
        self.setGeometry(100, 100, 800, 600)

        # Central widget with a stacked layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.stacked_widget = QStackedWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.stacked_widget)

        # Load all windows
        self.hash_table = hash_table
        self.playlist_manager = playlist_manager
        self.menu_widget = self.create_menu()

        # Callback to switch back to menu
        self.switch_to_menu_callback = switch_to_menu_callback

        self.search_by_artist_window = SearchByArtistWindow(hash_table, playlist_manager, switch_to_menu_callback)
        self.search_by_track_name_window = SearchByTrackNameWindow(hash_table, playlist_manager, switch_to_menu_callback)
        self.search_by_popularity_window = SearchByPopularityWindow(hash_table, playlist_manager, switch_to_menu_callback)
        
        # Playlist management windows
        self.playlist_window = PlaylistListWindow(playlist_manager, self.switch_to_menu_callback, self.switch_to_playlist_detail)
        self.playlist_detail_window = None  # Placeholder, will be set when a playlist is selected

        # Add widgets to stack
        self.stacked_widget.addWidget(self.menu_widget)
        self.stacked_widget.addWidget(self.search_by_artist_window)
        self.stacked_widget.addWidget(self.search_by_track_name_window)
        self.stacked_widget.addWidget(self.search_by_popularity_window)
        self.stacked_widget.addWidget(self.playlist_window)

    def create_menu(self):
        menu_widget = QWidget()
        layout = QVBoxLayout(menu_widget)

        # Buttons to navigate
        artist_button = QPushButton("Search by Artist")
        artist_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.search_by_artist_window))
        layout.addWidget(artist_button)

        track_button = QPushButton("Search by Track Name")
        track_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.search_by_track_name_window))
        layout.addWidget(track_button)

        popularity_button = QPushButton("Search by Popularity")
        popularity_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.search_by_popularity_window))
        layout.addWidget(popularity_button)
        
        # Botón para abrir la lista de playlists
        playlists_button = QPushButton("View Playlists")
        playlists_button.clicked.connect(self.view_playlists)
        layout.addWidget(playlists_button)

        return menu_widget
    
    def view_playlists(self):
        """Mostrar la ventana de lista de playlists."""
        self.playlist_list_window = PlaylistListWindow(
            self.playlist_manager,
            self.open_playlist,  # Callback para abrir una playlist específica
            self.switch_to_menu_callback
        )
        self.stacked_widget.addWidget(self.playlist_list_window)
        self.stacked_widget.setCurrentWidget(self.playlist_list_window)
        
    def open_playlist(self, playlist_name):
        """Abrir los detalles de una playlist específica."""
        playlist_window = PlaylistDetailWindow(
            playlist_name,
            self.playlist_manager,
            lambda: self.stacked_widget.setCurrentWidget(self.menu_widget)
        )
        self.stacked_widget.addWidget(playlist_window)
        self.stacked_widget.setCurrentWidget(playlist_window)
    
    def switch_to_playlist_detail(self, playlist_name):
        """Switch to playlist detail window when a playlist is selected."""
        self.playlist_detail_window = PlaylistDetailWindow(self.playlist_manager, playlist_name, self.switch_to_menu_callback)
        self.stacked_widget.addWidget(self.playlist_detail_window)
        self.stacked_widget.setCurrentWidget(self.playlist_detail_window)

    def closeEvent(self, event):
        """
        Save playlists to CSV before closing the application.
        """
        print("Saving playlists...")
        try:
            for playlist_name in self.playlist_manager.playlists.keys():
                self.playlist_manager.save_playlist_to_csv(playlist_name)
            print("Playlists saved successfully.")
        except Exception as e:
            print(f"Error saving playlists: {e}")
        event.accept()  # Close the window


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load songs into hash table
    file_path = 'gestor_app/spotify_data.csv'
    hash_table = load_songs_into_hash_table(file_path)

    # Load playlists from folder
    folder_path = 'playlists'
    playlist_manager = PlaylistManager()

    try:
        playlists = load_playlists_from_folder(folder_path)
        for name, songs in playlists.items():
            playlist_manager.playlists[name] = songs
        print("Playlists loaded successfully.")
    except FileNotFoundError:
        print(f"Folder '{folder_path}' not found. No playlists loaded.")
    except Exception as e:
        print(f"Error loading playlists: {e}")

    # Start main window
    main_window = MainWindow(hash_table, playlist_manager, lambda: main_window.stacked_widget.setCurrentWidget(main_window.menu_widget))
    main_window.show()

    sys.exit(app.exec())