#ifndef BST_H
#define BST_H

#include "Song.h"

// A single node in the BST
class BSTNode {
public:
    Song song;      // The song associated with the node
    BSTNode* left;  // Pointer to the left child
    BSTNode* right; // Pointer to the right child

    BSTNode(Song s) : song(s), left(nullptr), right(nullptr) {}
};

// Binary Search Tree for storing songs
class BST {
private:
    BSTNode* root;  // Root of the tree

    // Helper functions
    void insert(BSTNode*& node, Song song);  // Insert a song
    BSTNode* search(BSTNode* node, int id);  // Search a song by ID
    void inorderTraversal(BSTNode* node);    // Print all songs in order

public:
    BST() : root(nullptr) {}  // Constructor to initialize the BST

    void insert(Song song);   // Public insert method
    Song* search(int id);     // Public search method
    void printInOrder();      // Public method to print all songs
};

#endif