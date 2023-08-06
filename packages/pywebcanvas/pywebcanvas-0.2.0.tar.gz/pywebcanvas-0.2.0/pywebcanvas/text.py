import js
from colour import Color
import pywebcanvas as pwc


class Text:
    def __init__(self, text, x, y, size=20, color="black", font="helvetica", stroke=False):
        self.text = text
        self.x, self.y = x, y
        self.size = size
        self.color = color
        self.font = font
        self.stroke = stroke
    
    def render(self, canvas):
        pwc.log(f"Render text {self} at x {self.x}, y {self.y}, size {self.size}, color {self.color}, font {self.font}, stroke {self.stroke}")

        ctx = canvas.ctx()

        hex_color = Color(self.color).hex 

        ctx.fillStyle = hex_color
        ctx.font = f"{self.size}px {self.font}"

        if self.stroke:
            ctx.strokeText(self.text, self.x, self.y)
        else:
            ctx.fillText(self.text, self.x, self.y)
