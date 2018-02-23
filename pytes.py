from PIL import Image
from googletrans import Translator
import pytesseract
import argparse
import cv2
import os

#using a windows system, replace this with the path to you tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

#testing with one image
#likely switching to directory next
argp = argparse.ArgumentParser()
argp.add_argument("-i", "--image", required=True, help="path to image")
argp.add_argument("-p", "--preprocess", type=str, default="thresh",
    help="preprocessing type")
argp.add_argument("-t", "--translate", type=str, default ="",
    help="translate option using google trans")
#ensure the proper tesseract trained data file is downloaded
#(does not currently error check this for you)
argp.add_argument("-l", "--language", type=str, default="eng",
    help="tesseract image to string language")
args = vars(argp.parse_args())

img = cv2.imread(args["image"])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)

filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

newimg = Image.open(filename)
imgtext = pytesseract.image_to_string(newimg, lang=args["language"])
os.remove(filename)
print(imgtext)

if args["translate"] != "":
    translator = Translator()
    print(translator.translate(imgtext, src=args["translate"]))