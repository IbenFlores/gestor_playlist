#include "Song.h"
#include "BST.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

// Function to read a song from a CSV line
Song readSongFromCSVLine(const std::string& line) {
    Song song;
    std::stringstream ss(line);
    std::string field;

    std::getline(ss, field, ','); song.id = std::stoi(field);
    std::getline(ss, song.artist_name, ',');
    std::getline(ss, song.track_name, ',');
    std::getline(ss, song.track_id, ',');
    std::getline(ss, field, ','); song.popularity = std::stoi(field);
    std::getline(ss, field, ','); song.year = std::stoi(field);
    std::getline(ss, song.genre, ',');
    std::getline(ss, field, ','); song.danceability = std::stod(field);
    std::getline(ss, field, ','); song.energy = std::stod(field);
    std::getline(ss, field, ','); song.key = std::stoi(field);
    std::getline(ss, field, ','); song.loudness = std::stod(field);
    std::getline(ss, field, ','); song.mode = std::stoi(field);
    std::getline(ss, field, ','); song.speechiness = std::stod(field);
    std::getline(ss, field, ','); song.acousticness = std::stod(field);
    std::getline(ss, field, ','); song.instrumentalness = std::stod(field);
    std::getline(ss, field, ','); song.liveness = std::stod(field);
    std::getline(ss, field, ','); song.valence = std::stod(field);
    std::getline(ss, field, ','); song.tempo = std::stod(field);
    std::getline(ss, field, ','); song.duration_ms = std::stoi(field);
    std::getline(ss, field, ','); song.time_signature = std::stoi(field);

    return song;
}

// Function to load all songs from the CSV file and insert them into the BST
std::vector<Song> loadSongsFromCSV(const std::string& filename, BST& bst) {
    std::vector<Song> songs;
    std::ifstream file(filename);
    std::string line;

    // Skip the header
    std::getline(file, line);

    // Read and insert each song
    while (std::getline(file, line)) {
        Song song = readSongFromCSVLine(line);
        bst.insert(song);  // Insert song into BST
        songs.push_back(song);  // Optionally store songs in vector for further use
    }

    return songs;
}

int main() {
    // Initialize the BST
    BST bst;

    // Load songs from the CSV file and insert them into the BST
    std::vector<Song> songs = loadSongsFromCSV("test.csv", bst);

    // Print all songs in sorted order by ID
    std::cout << "Songs in sorted order by ID:\n";
    bst.printInOrder();

    // Search for a specific song by ID
    int searchId = 9;  // Example ID to search for
    Song* foundSong = bst.search(searchId);
    
    if (foundSong) {
        std::cout << "\nSong with ID " << searchId << " found:\n";
        foundSong->printSong();  // Print details of the found song
    } else {
        std::cout << "\nSong with ID " << searchId << " not found.\n";
    }

    return 0;
}