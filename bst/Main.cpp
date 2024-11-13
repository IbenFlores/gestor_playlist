// Main.cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include "Song.h"
#include "BST.h"

#define MAX_SONGS 1000

int main() {
    std::ifstream file("spotify_data.csv");
    if (!file.is_open()) {
        std::cerr << "File opening failed" << std::endl;
        return 1;
    }

    BST songTree;
    std::string line;

    // Skip the header line
    std::getline(file, line);

    // Read each song data line and insert it into the BST
    while (std::getline(file, line)) {
        std::istringstream ss(line);
        std::string artist_name, track_name, genre;
        int track_id, popularity, year, key, mode, duration_ms, time_signature;
        double danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo;

        // Read and parse CSV values
        std::getline(ss, artist_name, ',');
        std::getline(ss, track_name, ',');
        ss >> track_id;
        ss.ignore();
        ss >> popularity;
        ss.ignore();
        ss >> year;
        ss.ignore();
        std::getline(ss, genre, ',');
        ss >> danceability;
        ss.ignore();
        ss >> energy;
        ss.ignore();
        ss >> key;
        ss.ignore();
        ss >> loudness;
        ss.ignore();
        ss >> mode;
        ss.ignore();
        ss >> speechiness;
        ss.ignore();
        ss >> acousticness;
        ss.ignore();
        ss >> instrumentalness;
        ss.ignore();
        ss >> liveness;
        ss.ignore();
        ss >> valence;
        ss.ignore();
        ss >> tempo;
        ss.ignore();
        ss >> duration_ms;
        ss.ignore();
        ss >> time_signature;

        // Create a Song object and insert it into the BST
        Song song(artist_name, track_name, track_id, popularity, year, genre, danceability, energy, key, loudness, mode,
                  speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, time_signature);
        songTree.insert(song);
    }

    file.close();

    // Test search functionality
    int search_id = 123;  // Example track_id to search for
    BSTNode* result = songTree.search(search_id);

    if (result != nullptr) {
        std::cout << "Song found:" << std::endl;
        result->song.printSong();  // Print the song information
    } else {
        std::cout << "Song with track ID " << search_id << " not found." << std::endl;
    }

    return 0;
}