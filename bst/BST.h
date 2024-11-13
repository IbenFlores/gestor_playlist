#ifndef BST_H
#define BST_H

#include "Song.h"

class BSTNode {
public:
    Song song;
    BSTNode* left;
    BSTNode* right;

    BSTNode(Song s) : song(s), left(nullptr), right(nullptr) {}
};

class BST {
private:
    BSTNode* root;

    void insert(BSTNode*& node, Song song);
    BSTNode* search(BSTNode* node, int id);
    void inorderTraversal(BSTNode* node);

public:
    BST() : root(nullptr) {}

    void insert(Song song);
    Song* search(int id);
    void printInOrder();
};

#endif