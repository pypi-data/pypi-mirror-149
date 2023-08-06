import js
from colour import Color
import pywebcanvas as pwc


class Background:
    def __init__(self, canvas):
        self.canvas = canvas

    def fill(self, color):
        hex_color = Color(color).hex      
        pwc.log(f"Set {self.canvas} background to {hex_color}")
        self.canvas.canvas.setAttribute('style', f'background-color:{hex_color}')
