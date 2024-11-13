#include "BST.h"
#include <iostream>

void BST::insert(BSTNode*& node, Song song) {
    if (node == nullptr) {
        node = new BSTNode(song);
    } else if (song.id < node->song.id) {
        insert(node->left, song);
    } else {
        insert(node->right, song);
    }
}

void BST::insert(Song song) {
    insert(root, song);
}

BSTNode* BST::search(BSTNode* node, int id) {
    if (node == nullptr || node->song.id == id) {
        return node;
    }

    if (id < node->song.id) {
        return search(node->left, id);
    } else {
        return search(node->right, id);
    }
}

Song* BST::search(int id) {
    BSTNode* result = search(root, id);
    return result ? &result->song : nullptr;
}

void BST::inorderTraversal(BSTNode* node) {
    if (node == nullptr) return;

    inorderTraversal(node->left);
    node->song.printSong();
    inorderTraversal(node->right);
}

void BST::printInOrder() {
    inorderTraversal(root);
}