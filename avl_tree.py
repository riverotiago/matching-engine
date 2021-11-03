from typing import Optional, Any
from dataclasses import dataclass

@dataclass
class AVLNode:
    key: Any
    data: Optional[Any] = None
    parent: Optional['AVLNode'] = None
    left: Optional['AVLNode'] = None
    right: Optional['AVLNode'] = None
    height: int = 0

    def is_leaf(self) -> bool:
        return self.height == 0

@dataclass
class AVLTree:
    root: Optional[AVLNode] = None

    def insert(self, insert_node: AVLNode) -> None:
        if self.root is None:
            self.root = insert_node 

        node = self.root
        while True:
            if insert_node.key < node.key:
                if node.left is None:
                    insert_node.parent = node
                    node.left = insert_node 
                    self._rebalance(node.left)
                    return
                node = node.left
            elif insert_node.key > node.key:
                if node.right is None:
                    insert_node.parent = node
                    node.right = insert_node 
                    self._rebalance(node.right)
                    return
                node = node.right
            else:
                return

    def traverse(self, node: Optional[AVLNode] = None) -> None:
        if node:
            yield from self.traverse(node.left)
            yield node
            yield from self.traverse(node.right)

    def _rebalance(self, node: Optional[AVLNode]) -> None:
        while node is not None:
            self._updateHeight(node)
            balance = self._getBalance(node)
            if balance > 1:
                if self._getBalance(node.left) < 0:
                    self._rotateLeft(node.left)
                self._rotateRight(node)
            elif balance < -1:
                if self._getBalance(node.right) > 0:
                    self._rotateRight(node.right)
                self._rotateLeft(node)
            node = node.parent

    def _rotateLeft(self, node: AVLNode) -> None:
        right = node.right
        right.parent = node.parent
        if node.parent is None:
            self.root = right
        elif node.parent.left is node:
            node.parent.left = right
        else:
            node.parent.right = right
        node.right = right.left
        if node.right is not None:
            node.right.parent = node
        right.left = node
        node.parent = right
        self._updateHeight(node)
        self._updateHeight(right)

    def _rotateRight(self, node: AVLNode) -> None:
        left = node.left
        left.parent = node.parent
        if node.parent is None:
            self.root = left
        elif node.parent.left is node:
            node.parent.left = left
        else:
            node.parent.right = left
        node.left = left.right
        if node.left is not None:
            node.left.parent = node
        left.right = node
        node.parent = left
        self._updateHeight(node)
        self._updateHeight(left)

    def _updateHeight(self, node: AVLNode) -> None:
        node.height = max(self._getHeight(node.left), self._getHeight(node.right)) + 1

    def getMin(self, node: Optional[AVLNode]) -> Optional[AVLNode]:
        if node is None:
            return None
        while node.left is not None:
            node = node.left
        return node

    def getMax(self, node: Optional[AVLNode]) -> Optional[AVLNode]:
        if node is None:
            return None
        while node.right is not None:
            node = node.right
        return node

    def getPredecessor(self, node: AVLNode) -> Optional[AVLNode]:
        if node.left is not None:
            return self.getMax(node.left)
        while node.parent is not None and node.parent.left is node:
            node = node.parent
        return node.parent

    def getSuccessor(self, node: AVLNode) -> Optional[AVLNode]:
        if node.right is not None:
            return self.getMin(node.right)
        while node.parent is not None and node.parent.right is node:
            node = node.parent
        return node.parent

    def _getHeight(self, node: Optional[AVLNode]) -> int:
        if node is None:
            return 0
        return node.height

    def _getBalance(self, node: Optional[AVLNode]) -> int:
        if node is None:
            return 0
        return self._getHeight(node.left) - self._getHeight(node.right)

    def delete(self, node: AVLNode) -> None:
        if node.left is None:
            self._transplant(node, node.right)
        elif node.right is None:
            self._transplant(node, node.left)
        else:
            successor = self.getSuccessor(node)
            if successor.parent is not node:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor

    def _transplant(self, node1: AVLNode, node2: Optional[AVLNode]) -> None:
        if node1.parent is None:
            self.root = node2
        elif node1.parent.left is node1:
            node1.parent.left = node2
        else:
            node1.parent.right = node2
        if node2 is not None:
            node2.parent = node1.parent

    def get(self, key: Any) -> Optional[AVLNode]:
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node
        return None
