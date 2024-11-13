// BST.cpp
#include <iostream>
#include "BST.h"

// Constructor for BSTNode
BSTNode::BSTNode(Song song) : song(song), left(nullptr), right(nullptr) {}

// Constructor for BST
BST::BST() : root(nullptr) {}

// Insert a song into the BST
void BST::insert(Song song) {
    root = insertHelper(root, song);
}

// Helper function to insert a node into the BST recursively
BSTNode* BST::insertHelper(BSTNode* node, Song song) {
    if (node == nullptr) {
        return new BSTNode(song);
    }

    if (song.track_id < node->song.track_id) {
        node->left = insertHelper(node->left, song);
    } else if (song.track_id > node->song.track_id) {
        node->right = insertHelper(node->right, song);
    }
    return node;
}

// Search for a song by track_id
BSTNode* BST::search(int track_id) const {
    return searchHelper(root, track_id);
}

// Helper function to search for a song by track_id recursively
BSTNode* BST::searchHelper(BSTNode* node, int track_id) const {
    if (node == nullptr || node->song.track_id == track_id) {
        return node;
    }

    if (track_id < node->song.track_id) {
        return searchHelper(node->left, track_id);
    } else {
        return searchHelper(node->right, track_id);
    }
}