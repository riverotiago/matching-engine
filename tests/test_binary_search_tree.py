import unittest
from binary_search_tree import BinarySearchTree, Node

class TestBinarySearchTree(unittest.TestCase):
    def test_insert(self):
        pass

    def test_search(self):
        pass

    def test_delete(self):
        pass

    def test_traverse(self):
        bst = BinarySearchTree()
        for i in range(4):
            n = Node(key=(i, i+1), content=[])
            bst.insert(n)

        for bst_node in bst.traverse():
            print(bst_node.key)
