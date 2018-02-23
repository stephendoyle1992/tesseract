from PIL import Image
import pytesseract
import argparse
import cv2
import os


#testing with one image
#likely switching to directory next
argp = argparse.ArgumentParser()
argp.add_argument("-i", "--image", required=True, help="path to image")
argp.add_argument("-p", "--preprocess", type=str, default="thresh",
    help="preprocessing type")
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
imgtext = pytesseract.image_to_string(newimg)
os.remove(filename)
print(imgtext)

