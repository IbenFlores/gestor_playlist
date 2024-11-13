#include "Song.h"
#include <iostream>

// Constructor to initialize member variables
Song::Song() : id(0), popularity(0), year(0), key(0), mode(0), duration_ms(0), time_signature(0),
               danceability(0.0), energy(0.0), loudness(0.0), speechiness(0.0), acousticness(0.0),
               instrumentalness(0.0), liveness(0.0), valence(0.0), tempo(0.0) {}

// Method to print song details
void Song::printSong() const {
    std::cout << "ID: " << id << ", Artist: " << artist_name << ", Track: " << track_name
              << ", Popularity: " << popularity << ", Year: " << year << ", Genre: " << genre
              << ", Tempo: " << tempo << " BPM, Duration: " << duration_ms / 1000.0 << " seconds"
              << ", Time Signature: " << time_signature << std::endl;
}