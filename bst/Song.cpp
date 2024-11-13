// Song.cpp
#include <iostream>
#include "Song.h"

// Constructor implementation
Song::Song(std::string artist_name, std::string track_name, int track_id, int popularity, int year, std::string genre,
           double danceability, double energy, int key, double loudness, int mode, double speechiness,
           double acousticness, double instrumentalness, double liveness, double valence, double tempo,
           int duration_ms, int time_signature)
    : artist_name(artist_name), track_name(track_name), track_id(track_id), popularity(popularity), year(year),
      genre(genre), danceability(danceability), energy(energy), key(key), loudness(loudness), mode(mode),
      speechiness(speechiness), acousticness(acousticness), instrumentalness(instrumentalness), liveness(liveness),
      valence(valence), tempo(tempo), duration_ms(duration_ms), time_signature(time_signature) {}

// Method to print the song's information
void Song::printSong() const {
    std::cout << "Artist: " << artist_name << std::endl;
    std::cout << "Track: " << track_name << std::endl;
    std::cout << "ID: " << track_id << std::endl;
    std::cout << "Popularity: " << popularity << std::endl;
    std::cout << "Year: " << year << std::endl;
    std::cout << "Genre: " << genre << std::endl;
    std::cout << "Danceability: " << danceability << std::endl;
    std::cout << "Energy: " << energy << std::endl;
    std::cout << "Key: " << key << std::endl;
    std::cout << "Loudness: " << loudness << std::endl;
    std::cout << "Mode: " << mode << std::endl;
    std::cout << "Speechiness: " << speechiness << std::endl;
    std::cout << "Acousticness: " << acousticness << std::endl;
    std::cout << "Instrumentalness: " << instrumentalness << std::endl;
    std::cout << "Liveness: " << liveness << std::endl;
    std::cout << "Valence: " << valence << std::endl;
    std::cout << "Tempo: " << tempo << std::endl;
    std::cout << "Duration (ms): " << duration_ms << std::endl;
    std::cout << "Time Signature: " << time_signature << std::endl;
}