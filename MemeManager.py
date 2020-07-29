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
            imagePath = './img/' + memeName + '.jpg'
            image = Image.open(imagePath)
        except FileNotFoundError:
            raise ValueError("File not found")

        with open("metadata.json", "r") as data:
            dataJSON = json.load(data)
        memeInfo = dataJSON[memeName]
        if "color" in memeInfo:
            color = tuple(memeInfo['color'])
        else:
            color = (0, 0, 0)
        textpos = memeInfo['textpos']
        image = self.resizeImage(image)
        for i in range(len(textpos)):
            pos = (textpos[i]["x"], textpos[i]["y"])
            linea = text[textpos[i]["id"]]
            if "deg" in textpos[i]:
                rotacion = textpos[i]["deg"] % 360
            else:
                rotacion = 0
            if (rotacion < 0):
                rotacion += 360
            textImg = self.textToImage(linea, color, rotacion)
            image.paste(textImg, box=pos, mask=textImg)
        image.save('temp.jpg')
        image.close()
        return

    def getParams(self):
        return self.rawText.split('_')

    def resizeImage(self, image):
        aspectRatio = image.size[1] / image.size[0]
        width = self.IMAGE_WIDTH
        height = round(aspectRatio * width)
        return image.resize((width, height))

    def textToImage(self, text, color, deg): 
        font = ImageFont.truetype(self.FONT_PATH, self.FONT_SIZE)
        inv = (255, 255, 255, 0)
        textImg = Image.new("RGBA", font.getsize(text), color=inv)
        textDraw = ImageDraw.Draw(textImg)
        textDraw.text((0, 0), text=text, font=font, fill=color)
        textImg = textImg.rotate(deg, expand=1, fillcolor=inv)
        return textImg


#Para poder debugear sin necesidad de correr el bot
if __name__ == '__main__':
    instance = MemeManager("buttons_DFS_BFS_yo")
    instance.getMeme()

