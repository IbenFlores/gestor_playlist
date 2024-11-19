#ifndef SONG_H
#define SONG_H

#include <string>

class Song {
public:
    int id;
    std::string artist_name;
    std::string track_name;
    std::string track_id;
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

    Song();
    void printSong() const;
};

#endif