# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 09:57:45 2024

@author: EMKA
"""

import plotly.graph_objects as go
import numpy as np

class Vector:
    def __init__(self, components):
        self.components = np.array(components)

    def magnitude(self):
        return np.linalg.norm(self.components)

    def dot_product(self, other):
        return np.dot(self.components, other.components)

    def cross_product(self, other):
        return np.cross(self.components, other.components)

    def add(self, other):
        return Vector(self.components + other.components)

    def subtract(self, other):
        return Vector(self.components - other.components)

# Sample vectors
vector1 = Vector([1, 2, 3])
vector2 = Vector([4, 5, 6])

# Create a plot
fig = go.Figure()

# Add vectors to the plot
fig.add_trace(go.Scatter3d(x=[0, vector1.components[0]], y=[0, vector1.components[1]], z=[0, vector1.components[2]], 
                           mode='lines+markers', name='Vector 1'))
fig.add_trace(go.Scatter3d(x=[0, vector2.components[0]], y=[0, vector2.components[1]], z=[0, vector2.components[2]], 
                           mode='lines+markers', name='Vector 2'))

# Set layout
fig.update_layout(scene=dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z'),
                  margin=dict(r=20, b=10, l=10, t=10))

# Show plot
fig.show()
