from PIL import Image, ImageDraw, ImageFont

import json

class MemeManager:

    IMAGE_WIDTH = 512
    FONT_SIZE = 24
    FONT_PATH = './fonts/Roboto.ttf'

    def __init__(self, text):
        self.rawText = text

    def getMeme(self):
        text = self.getParams()
        memeName = text[0].lower()
        text = text[1:]
        try:
            imagePath = './img' + memeName + '.jpg'
            image = Image.open(imagePath)
        except FileNotFoundError:
            raise ValueError("File not found")

        with open("metadata.json", "r") as data:
            dataJSON = json.load(data)
        memeInfo = dataJSON[memeName]
        if "color" in memeInfo:
            color = tuple(memeInfo.color)
        else:
            color = (0, 0, 0)
        textpos = memeInfo.textpos
        image = self.resizeImage(image)
        font = ImageFont.truetype(self.FONT_PATH, self.FONT_SIZE)
        draw = ImageDraw.Draw(image)
        for i in range(len(textpos)):
            pos = (textpos[i].x, textpos[i].y)
            linea = text[textpos[i].id]
            draw.text(xy=pos, text=linea, fill=color, font=font)
        image.save('temp.jpg')
        return

    def getParams(self):
        return self.rawText.split('_')

    def resizeImage(self, image):
        aspectRatio = image.size[1] / image.size[0]
        width = self.IMAGE_WIDTH
        height = round(aspectRatio * width)
        return image.resize(width, height)
