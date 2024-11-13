#include "Song.h"
#include "BST.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

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

std::vector<Song> loadSongsFromCSV(const std::string& filename, BST& bst) {
    std::vector<Song> songs;
    std::ifstream file(filename);
    std::string line;

    std::getline(file, line);

    while (std::getline(file, line)) {
        Song song = readSongFromCSVLine(line);
        bst.insert(song);
        songs.push_back(song);
    }

    return songs;
}

int main() {
    BST bst;

    std::vector<Song> songs = loadSongsFromCSV("test.csv", bst);

    std::cout << "Songs in sorted order by ID:\n";
    bst.printInOrder();

    int searchId = 9;
    Song* foundSong = bst.search(searchId);
    
    if (foundSong) {
        std::cout << "\nSong with ID " << searchId << " found:\n";
        foundSong->printSong();
    } else {
        std::cout << "\nSong with ID " << searchId << " not found.\n";
    }

    return 0;
}