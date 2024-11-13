#include "BST.h"
#include <iostream>

// Insert a song into the BST
void BST::insert(BSTNode*& node, Song song) {
    if (node == nullptr) {
        node = new BSTNode(song);  // Create a new node if the current node is null
    } else if (song.id < node->song.id) {
        insert(node->left, song);  // Go to the left subtree if the ID is smaller
    } else {
        insert(node->right, song); // Go to the right subtree if the ID is larger
    }
}

// Public insert method
void BST::insert(Song song) {
    insert(root, song);
}

// Search for a song by its ID in the BST
BSTNode* BST::search(BSTNode* node, int id) {
    if (node == nullptr || node->song.id == id) {
        return node;  // Return the node if found, or null if not found
    }

    if (id < node->song.id) {
        return search(node->left, id);  // Search in the left subtree
    } else {
        return search(node->right, id); // Search in the right subtree
    }
}

// Public search method
Song* BST::search(int id) {
    BSTNode* result = search(root, id);
    return result ? &result->song : nullptr;  // Return the song if found, or null if not found
}

// In-order traversal to print all songs in the tree
void BST::inorderTraversal(BSTNode* node) {
    if (node == nullptr) return;  // Base case: if the node is null, return

    inorderTraversal(node->left);  // Recursively visit the left subtree
    node->song.printSong();        // Print the song information
    inorderTraversal(node->right); // Recursively visit the right subtree
}

// Public method to print all songs in order
void BST::printInOrder() {
    inorderTraversal(root);
}