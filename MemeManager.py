from PIL import Image, ImageDraw, ImageFont, ImageSequence

import json

class MemeManager:

    IMAGE_WIDTH = 512
    FONT_SIZE = 24
    FONT_PATH = './fonts/Roboto.ttf'

    def setText(self, text):
        self.args = text

    def getMeme(self):
        memeName = self.args[0].lower()
        text = self.args[1:]
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
                self.printText(linea, textpos[i], image, memeInfo)
            except IndexError:
                raise TypeError("Not enough arguments")
        image.save('temp.jpg')
        image.close()
        return

    def getAnimatedMeme(self):
        memeName = self.args[0].lower()
        text = self.args[1:]
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
                self.printText(
                    text[textpos[i]["id"]],
                    textpos[i],
                    frame,
                    memeInfo
                )

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

    def resizeImage(self, image):
        aspectRatio = image.size[1] / image.size[0]
        width = self.IMAGE_WIDTH
        height = round(aspectRatio * width)
        return image.resize((width, height))

    def printText(self, texto, data, image, memeInfo):
        if "deg" in data:
            rotacion = self.getRotation(data["deg"])
        else:
            rotacion = 0
        textoSeparado = texto.split('\n')
        contador = 0
        if "fontsize" in memeInfo:
            fontsize = memeInfo["fontsize"]
        else:
            fontsize = self.FONT_SIZE
        for i in textoSeparado:
            textImg = self.textToImage(i, rotacion, fontsize)
            corner = (
                data['x'] - textImg.size[0] // 2,
                data['y'] + (fontsize + 4) * contador
            )
            contador = contador + 1
            image.paste(textImg, box=corner, mask=textImg)

    def getRotation(self, deg):
        return ((deg % 360) + 360) % 360

    def textToImage(self, text, deg, fontsize):
        font = ImageFont.truetype(self.FONT_PATH, fontsize)
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

    @staticmethod
    def getMemeList(page):
        memeList = "```asciidoc"
        memeList += "\nMemer, bot de discord\n"
        memeList += "====================\n"
        memeList += "[Lista de memes: Página {}]\n".format(page)
        with open("metadata.json", "r") as metadata:
            data = json.load(metadata)
        i = 0
        for meme in data:
            if i // 10 != (page - 1):
                i = i + 1
                continue
            elif i // 10 >= page:
                break
            i = i + 1
            maxID = 0
            for line in data[meme]['textpos']:
                maxID = max(maxID, line['id'])
            if "anim" in data[meme]:
                memeList += ". {}: {} parámetros\n".format(
                    meme,
                    maxID + 1
                )
            else:
                memeList += "* {}: {} parámetros\n".format(
                    meme,
                    maxID + 1
                )
        memeList += "Los memes con . requieren anim\n"
        memeList += "```"
        return memeList

#Para poder debugear sin necesidad de correr el bot
if __name__ == '__main__':
    instance = MemeManager("buttons_DFS_BFS_yo")
    instance.getMeme()

