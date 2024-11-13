// Song.h
#ifndef SONG_H
#define SONG_H

#include <string>

class Song {
public:
    std::string artist_name;
    std::string track_name;
    int track_id;
    int popularity;
    int year;
    std::string genre;
    double danceability;
    double energy;
    int key;
    double loudness;
    int mode;
    double speechiness;
    double acousticness;
    double instrumentalness;
    double liveness;
    double valence;
    double tempo;
    int duration_ms;
    int time_signature;

    // Constructor to initialize a song object
    Song(std::string artist_name, std::string track_name, int track_id, int popularity, int year, std::string genre,
         double danceability, double energy, int key, double loudness, int mode, double speechiness,
         double acousticness, double instrumentalness, double liveness, double valence, double tempo,
         int duration_ms, int time_signature);

    // Method to print the song's information
    void printSong() const;
};

#endif // SONG_H