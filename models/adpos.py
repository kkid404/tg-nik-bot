from PIL import Image, ImageDraw, ImageFont
from random import randint

class Adpos():
    
    def __init__(self) -> None:
        self.NUMBER_POSITION = (30, 140)
        self.NAME_POSITION = (30, 215)
        self.DATE_POSITION = (257, 215)
        self.CVV_POSITION = (370, 215)

        self.OUTPUT_FILE = f"ready_card{randint(100, 999)}.jpg"

        self.FONT_CARD = "fonts/Quiroh-Heavy/Quiroh-Heavy.ttf"
        self.FONT_OTHER_TEXT = "fonts/Khmer-Oureang-Ultra-expanded-UltraBlack/khbaphnom.ttf"

        self.COLOR_TEXT = "#83919C"

        self.NUMBER_SIZE = 29
        self.OTHER_SIZE = 18

        self.IMG_PATH = "img/cart-example.jpg"

    def create(self, number, name, date, cvv):
        with Image.open(self.IMG_PATH) as img:
            font_main = ImageFont.truetype(self.FONT_CARD, size=self.NUMBER_SIZE)
            font_other_text = ImageFont.truetype(self.FONT_OTHER_TEXT, size=self.OTHER_SIZE)

            draw = ImageDraw.Draw(img)
            draw.text(self.NUMBER_POSITION, number, fill="white", font=font_main)
            draw.text(self.NAME_POSITION, name, fill=self.COLOR_TEXT, font=font_other_text)
            draw.text(self.DATE_POSITION, date, fill=self.COLOR_TEXT, font=font_other_text)
            draw.text(self.CVV_POSITION, cvv, fill=self.COLOR_TEXT, font=font_other_text)
            img.save(self.OUTPUT_FILE)
    
        return self.OUTPUT_FILE