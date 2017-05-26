# -*- coding=utf-8 -*-

class BinaryTreeNode:
    """
    Simple Binary Tree Node
    """
    def __init__(self, data=None):
        self.data = data
        self.left_kid = None
        self.right_kid = None


class SimpleBinaryTree:
    """
    Simple Binary Tree 
    """
    def __init__(self, data=None):
        self.treeNode = BinaryTreeNode(data)

    def set_data(self, data):
        self.treeNode.data = data

    def set_right_kid(self, binary_tree_node):
        assert binary_tree_node.__class__ is SimpleBinaryTree.__class__
        self.treeNode.right_kid = binary_tree_node

    def set_left_kid(self, binary_tree_node):
        assert binary_tree_node.__class__ is SimpleBinaryTree.__class__
        self.treeNode.left_kid = binary_tree_node

    def front_read(self, node):
        if node is not None and node.data is not None:
            print(node.data)
            self.front_read(node.left_kid)
            self.front_read(node.right_kid)

    def mid_read(self, node):
        if node is not None and node.data is not None:
            self.front_read(node.left_kid)
            print(node.data)
            self.front_read(node.right_kid)

    def behind_read(self, node):
        if node is not None and node.data is not None:
            self.front_read(node.left_kid)
            self.front_read(node.right_kid)
            print(node.data)


