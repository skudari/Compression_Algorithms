import numpy as np

# Encoding will be left:0 right:1
class Tree:
    def __init__(self, prob, RGB, value="", left=None, right=None, code=None):
        self.prob = prob
        self.RGB = RGB
        self.value = value
        self.left = left
        self.right = right
        self.code = ""

