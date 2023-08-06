from manim import *
from manim_ml.neural_network.layers.parent_layers import VGroupNeuralNetworkLayer

class Convolutional2DLayer(VGroupNeuralNetworkLayer):
    
    def __init__(self, feature_map_height, feature_map_width, filter_width, filter_height, 
            pixel_width=0.5, map_color=BLUE, filter_color=ORANGE, stride=1,
            **kwargs):
        super(VGroupNeuralNetworkLayer, self).__init__(**kwargs)
        self.feature_map_height = feature_map_height
        self.feature_map_width = feature_map_width
        self.filter_width = filter_width
        self.filter_height = filter_height
        self.pixel_width = pixel_width
        self.map_color = map_color
        self.filter_color = filter_color
        self.stride = stride

        self.construct_layer()

    def construct_layer(self):
        """Makes the assets for the layer"""
        pass

    def make_forward_pass_animation(self, **kwargs):
        """Make feed forward animation"""
        pass