__author__ = 'pawel'


class BinaryTreeNode():

    def __init__(self, root_id, left=None, right=None):
        self.root_id = root_id
        self.left = left
        self.right = right

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def set_value(self, value):
        self.root_id = value

    def get_value(self):
        return self.root_id

    def insert_right(self, newNode):
        if not self.right:
            self.right = BinaryTreeNode(newNode)
        else:
            tree = BinaryTreeNode(newNode)
            tree.right = self.right
            self.right = tree

    def insert_left(self, newNode):
        if not self.left:
            self.left = BinaryTreeNode(newNode)
        else:
            tree = BinaryTreeNode(newNode)
            self.left = tree
            tree.left = self.left

    def __str__(self):
        return '[{} < {} > {}]'.format(self.get_left() or '', self.get_value(), self.get_right() or '')


def print_tree(tree):
    if tree:
        print_tree(tree.get_left())
        print(tree.get_value())
        print_tree(tree.get_right())
