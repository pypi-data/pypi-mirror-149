from manim import *
from manim_ml.neural_network.layers.convolutional_2d import Convolutional2DLayer
from manim_ml.neural_network.layers.parent_layers import ConnectiveLayer

class Convolutional2DToConvolutional2D(ConnectiveLayer):
    """2D Conv to 2d Conv"""
    input_class = Convolutional2DLayer
    output_class = Convolutional2DLayer

    def __init__(self, input_layer, output_layer, color=WHITE, pulse_color=RED,
                **kwargs):
        super().__init__(input_layer, output_layer, input_class=Convolutional2DLayer, 
                        output_class=Convolutional2DLayer, **kwargs)
        self.color = color
        self.pulse_color = pulse_color

        self.add(self.lines)

    def create_filter(self):
        """Creates the filter object"""
        pass

    def make_forward_pass_animation(self, layer_args={}, run_time=1.5, **kwargs):
        """Forward pass animation from conv to conv"""
        # Scans a filter across the input layer feature map

        animation_group = AnimationGroup()
        return animation_group

    @override_animation(Create)
    def _create_override(self, **kwargs):
        return AnimationGroup()