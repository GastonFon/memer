from PIL import Image, ImageDraw, ImageFont, ImageSequence

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
        with open("metadata.json", "r") as data:
            dataJSON = json.load(data)
        memeInfo = dataJSON[memeName]
        if "anim" in memeInfo:
            raise ValueError("This is an animated meme")
        try:
            image = self.openImage(memeName, '.jpg')
        except ValueError:
            return
        textpos = memeInfo['textpos']
        image = self.resizeImage(image)
        for i in range(len(textpos)):
            try:
                linea = text[textpos[i]["id"]]
                self.printText(linea, textpos[i], image)
            except IndexError:
                raise TypeError("Not enough arguments")
        image.save('temp.jpg')
        image.close()
        return    

    def getAnimatedMeme(self):
        text = self.getParams()
        memeName = text[0].lower()
        text = text[1:]
        try:
            image = self.openImage(memeName, '.gif')
        except ValueError:
            return
        with open("metadata.json", "r") as data:
            dataJSON = json.load(data)
        memeInfo = dataJSON[memeName]
        textpos = memeInfo['textpos']
        frames = []
        for frame in ImageSequence.Iterator(image):
            frame = frame.convert("RGB")
 
            for i in range(len(textpos)):
                self.printText(text[textpos[i]["id"]], textpos[i], frame)

            frames.append(frame)
        frames[0].save(
            "temp.gif",
            format="GIF",
            save_all=True,
            append_images=frames[1:]
        )
        return

    def openImage(self, name, extension):
        imagePath = './img/' + name + extension
        try:
            image = Image.open(imagePath)
            return image
        except FileNotFoundError:
            raise ValueError("File not found")

    def getParams(self):
        return self.rawText.split('_')

    def resizeImage(self, image):
        aspectRatio = image.size[1] / image.size[0]
        width = self.IMAGE_WIDTH
        height = round(aspectRatio * width)
        return image.resize((width, height))

    def printText(self, texto, data, image):
        if "deg" in data:
            rotacion = self.getRotation(data["deg"])
        else:
            rotacion = 0
        textoSeparado = texto.split('\n')
        contador = 0
        for i in textoSeparado:
            textImg = self.textToImage(i, rotacion)
            corner = (
                data['x'] - textImg.size[0] // 2,
                data['y'] + (self.FONT_SIZE + 4) * contador
            )
            contador = contador + 1
            image.paste(textImg, box=corner, mask=textImg)

    def getRotation(self, deg):
        return ((deg % 360) + 360) % 360

    def textToImage(self, text, deg): 
        font = ImageFont.truetype(self.FONT_PATH, self.FONT_SIZE)
        textImg = Image.new("RGBA", font.getsize(text),
                color=(255, 255, 255, 255))
        textDraw = ImageDraw.Draw(textImg)
        textDraw.text(
            (0, 0),
            text=text,
            font=font,
            fill=(0, 0, 0)
        )
        textImg = textImg.rotate(
            deg, expand=1,
            fillcolor=(255, 255, 255, 0)
        )
        return textImg


#Para poder debugear sin necesidad de correr el bot
if __name__ == '__main__':
    instance = MemeManager("buttons_DFS_BFS_yo")
    instance.getMeme()

