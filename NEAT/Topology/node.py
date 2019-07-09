import random

class Node:
    def __init__(self, number, layer='AmbiguousHidden', activation='sigmoid'):
        self.number = number
        self.activation = activation
        self.layer = layer
        self.active = False

    def __str__(self):
        return "Node(number:%s, activation:%s, layer:%s, active:%s)" % (self.number, self.activation, self.layer, self.active)

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
        
    def toggle(self):
        self.active = not self.active

    @property
    def is_active(self):
        return self.active

