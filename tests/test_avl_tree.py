import unittest
from avl_tree import AVLTree, AVLNode

class TestAVLTree(unittest.TestCase):

    def test_insert(self):
        avl = AVLTree()
        node = AVLNode(key=(20, 0))
        avl.insert(node)

        # Primeiro nó inserido é root
        self.assertEqual(avl.root, node)

        # Nó inserido com key menor vai para esquerda 
        node_left = AVLNode(key=(15, 0)) 
        avl.insert(node_left)
        self.assertEqual(avl.root.left, node_left, "Nó inserido com key menor vai para esquerda")

        # Nó inserido com key maior vai para direita
        node_right = AVLNode(key=(30, 0)) 
        avl.insert(node_right)
        self.assertEqual(avl.root.right, node_right, "Nó inserido com key maior vai para direita")

    def test_traverse(self):
        avl = AVLTree()
        for i in range(3):
            n = AVLNode(key=(0, i))
            avl.insert(n)

        for i in range(2):
            n = AVLNode(key=(1, i))
            avl.insert(n)

        keys = [node.key for node in avl.traverse(avl.root)]
        keys_expected = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        
        self.assertEqual(keys, keys_expected)

    def test_rotate(self):
        avl = AVLTree()
        for i in range(3):
            n = AVLNode(key=(0, i))
            avl.insert(n)

        for i in range(2):
            n = AVLNode(key=(1, i))
            avl.insert(n)

        # Ao final da inserção
        #     0,1
        # 0,0    1,0
        #      0,2  1,1

        # Sanity test
        keys = [node.key for node in avl.traverse(avl.root)]
        avl._rotateLeft(avl.root)
        avl._rotateRight(avl.root)
        keys_expected = [node.key for node in avl.traverse(avl.root)]
        self.assertEqual(keys, keys_expected, "Sanity test.")
        self.assertEqual(avl.root.key, (0,1), "Raiz da árvore continua igual.")

        # Rotação para esquerda
        keys = [node.key for node in avl.traverse(avl.root)]
        avl._rotateLeft(avl.root)
        keys_expected = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        self.assertEqual(avl.root.key, (1,0), "Raiz da árvore mudou corretamente.")
        self.assertEqual(keys, keys_expected, "Rotação para esquerda mantém ordem de percurso in-order.")

        # Rotação para direita
        keys = [node.key for node in avl.traverse(avl.root)]
        avl._rotateRight(avl.root)
        keys_expected = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        self.assertEqual(avl.root.key, (0,1), "Raiz da árvore mudou corretamente.")
        self.assertEqual(keys, keys_expected, "Rotação para direita mantém ordem de percurso in-order.")

    def test_getMin(self):
        avl = AVLTree()
        for i in range(3):
            n = AVLNode(key=(0, i))
            avl.insert(n)

        for i in range(2):
            n = AVLNode(key=(1, i))
            avl.insert(n)

        self.assertEqual(avl.getMin(avl.root).key, (0,0), "Retorna nó com key menor.")

    def test_getMax(self):
        avl = AVLTree()
        for i in range(3):
            n = AVLNode(key=(0, i))
            avl.insert(n)

        for i in range(2):
            n = AVLNode(key=(1, i))
            avl.insert(n)
        
        self.assertEqual(avl.getMax(avl.root).key, (1,1), "Retorna nó com key maior.")

    def test_getSuccessor(self):
        avl = AVLTree()
        for i in range(3):
            n = AVLNode(key=(0, i))
            avl.insert(n)

        for i in range(2):
            n = AVLNode(key=(1, i))
            avl.insert(n)

        key = avl.getSuccessor(avl.getMin(avl.root)).key
        key_expected = (0,1)
        self.assertEqual(key, key_expected, "Retorna sucessor do nó com menor chave.")

    def test_getPredecessor(self):
        avl = AVLTree()
        for i in range(3):
            n = AVLNode(key=(0, i))
            avl.insert(n)

        for i in range(2):
            n = AVLNode(key=(1, i))
            avl.insert(n)

        key = avl.getPredecessor(avl.getMax(avl.root)).key
        key_expected = (1,0)
        self.assertEqual(key, key_expected, "Retorna predecessor do nó com maior chave.")

    def test_remove(self):
        avl = AVLTree()
        for i in range(3):
            n = AVLNode(key=(0, i))
            avl.insert(n)

        for i in range(2):
            n = AVLNode(key=(1, i))
            avl.insert(n)

        node_0_0 = avl.getMin(avl.root)
        avl.delete(node_0_0)
        keys = [node.key for node in avl.traverse(avl.root)]
        keys_expected = [(0, 1), (0, 2), (1, 0), (1, 1)]
        self.assertEqual(keys, keys_expected, "Remove nó com key (0,0).")

        node_1_0 = avl.getSuccessor(avl.getSuccessor(avl.getSuccessor(node_0_0)))
        avl.delete(node_1_0)
        keys = [node.key for node in avl.traverse(avl.root)]
        keys_expected = [(0, 1), (0, 2), (1, 1)]
        self.assertEqual(keys, keys_expected, "Remove nó com key (1,0).")

    def test_get(self):
        avl = AVLTree()
        for i in range(3):
            n = AVLNode(key=(0, i))
            avl.insert(n)

        for i in range(2):
            n = AVLNode(key=(1, i))
            avl.insert(n)

        node = AVLNode(key=(0,1.5))
        avl.insert(node)
        self.assertEqual(avl.get(node.key), node, "Retorna nó com key (0,1.5).")
        self.assertEqual(avl.get(avl.root.key), avl.root, "Retorna raiz da árvore.")
        self.assertEqual(avl.get((1,-1)), None, "Retorna None se não encontrar nó com key (1,-1).")

if __name__ == '__main__':
    unittest.main()
