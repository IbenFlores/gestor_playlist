import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QStackedWidget
)
from loader import load_songs_into_hash_table
from search_windows import SearchByArtistWindow, SearchByPopularityWindow, SearchByTrackNameWindow

class MainWindow(QMainWindow):
    def __init__(self, hash_table):
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
        self.menu_widget = self.create_menu()

        # Callback to switch back to menu
        switch_to_menu_callback = lambda: self.stacked_widget.setCurrentWidget(self.menu_widget)

        self.search_by_artist_window = SearchByArtistWindow(hash_table, switch_to_menu_callback)
        self.search_by_track_name_window = SearchByTrackNameWindow(hash_table, switch_to_menu_callback)
        self.search_by_popularity_window = SearchByPopularityWindow(hash_table, switch_to_menu_callback)

        # Add widgets to stack
        self.stacked_widget.addWidget(self.menu_widget)
        self.stacked_widget.addWidget(self.search_by_artist_window)
        self.stacked_widget.addWidget(self.search_by_track_name_window)
        self.stacked_widget.addWidget(self.search_by_popularity_window)

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

        return menu_widget


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load songs from CSV
    file_path = 'gestor_app/spotify_data.csv'
    hash_table = load_songs_into_hash_table(file_path)

    # Start main window
    main_window = MainWindow(hash_table)
    main_window.show()

    sys.exit(app.exec())