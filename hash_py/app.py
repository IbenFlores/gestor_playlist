import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QStackedWidget
)
from loader import load_songs_from_csv


class SearchByArtistWindow(QWidget):
    def __init__(self, hash_table, switch_to_menu_callback):
        super().__init__()
        self.hash_table = hash_table
        self.switch_to_menu_callback = switch_to_menu_callback


        # Layout for artist search
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.artist_label = QLabel("Enter artist name:")
        layout.addWidget(self.artist_label)

        self.artist_entry = QLineEdit()
        layout.addWidget(self.artist_entry)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_by_artist)
        layout.addWidget(self.search_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.switch_to_menu_callback)
        layout.addWidget(self.back_button)

    def search_by_artist(self):
        artist_name = self.artist_entry.text()
        results = self.hash_table.search_by_artist(artist_name)

        self.result_text.clear()
        if results:
            for song in results:
                self.result_text.append(f"{song.artist_name} - {song.track_name} (Popularity: {song.popularity})")
        else:
            self.result_text.append("No songs found for this artist.")


class SearchByTrackNameWindow(QWidget):
    def __init__(self, hash_table, switch_to_menu_callback):
        super().__init__()
        self.hash_table = hash_table
        self.switch_to_menu_callback = switch_to_menu_callback


        # Layout for track name search
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.track_label = QLabel("Enter track name:")
        layout.addWidget(self.track_label)

        self.track_entry = QLineEdit()
        layout.addWidget(self.track_entry)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_by_track_name)
        layout.addWidget(self.search_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.switch_to_menu_callback)
        layout.addWidget(self.back_button)

    def search_by_track_name(self):
        track_name = self.track_entry.text()
        results = self.hash_table.search_by_track_name(track_name)

        self.result_text.clear()
        if results:
            for song in results:
                self.result_text.append(f"{song.artist_name} - {song.track_name} (Popularity: {song.popularity})")
        else:
            self.result_text.append("No songs found for this track name.")


class SearchByPopularityWindow(QWidget):
    def __init__(self, hash_table, switch_to_menu_callback):
        super().__init__()
        self.hash_table = hash_table
        self.switch_to_menu_callback = switch_to_menu_callback

        # Layout for popularity search
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.popularity_label = QLabel("Enter minimum and maximum popularity:")
        layout.addWidget(self.popularity_label)

        self.min_popularity_entry = QLineEdit()
        self.min_popularity_entry.setPlaceholderText("Minimum popularity")
        layout.addWidget(self.min_popularity_entry)

        self.max_popularity_entry = QLineEdit()
        self.max_popularity_entry.setPlaceholderText("Maximum popularity")
        layout.addWidget(self.max_popularity_entry)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_by_popularity)
        layout.addWidget(self.search_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.switch_to_menu_callback)
        layout.addWidget(self.back_button)

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
                    self.result_text.append(f"{song.artist_name} - {song.track_name} (Popularity: {song.popularity})")
            else:
                self.result_text.append("No songs found in this popularity range.")
        except ValueError:
            self.result_text.append("Please enter valid numeric values for popularity.")


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
    file_path = 'hash_py/spotify_data.csv'
    hash_table = load_songs_from_csv(file_path)

    # Start main window
    main_window = MainWindow(hash_table)
    main_window.show()

    sys.exit(app.exec())