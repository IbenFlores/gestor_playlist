// BST.h
#ifndef BST_H
#define BST_H

#include "Song.h"

// Define a BST node
class BSTNode {
public:
    Song song;             // Song data
    BSTNode* left;         // Left child
    BSTNode* right;        // Right child

    // Constructor to initialize a node
    BSTNode(Song song);
};

// Define the BST class
class BST {
public:
    BSTNode* root;  // Root node

    // Constructor
    BST();

    // Method to insert a node into the BST
    void insert(Song song);

    // Method to search for a song by track_id
    BSTNode* search(int track_id) const;

private:
    // Helper method to insert a node into the BST recursively
    BSTNode* insertHelper(BSTNode* node, Song song);

    // Helper method to search for a song by track_id recursively
    BSTNode* searchHelper(BSTNode* node, int track_id) const;
};

#endif // BST_H