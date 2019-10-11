from PIL import Image
import numpy as np
import cv2, time, pytesseract
from PIL import ImageGrab
import requests

# Take the screenshot, and turn it into a numpy array so we can use cv2 methods
img = ImageGrab.grab(bbox=(175,600,800,1500))
img_np = np.array(img)

# In order:
# 1) Make the image grayscale
# 2) Use a binary threshold to remove all artifacts that are not letters
# 3) Blur the image to make it easier for Tesseract to read.
# 4) Write the image to disk.
gray = cv2.cvtColor(img_np,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)[1]
blur = cv2.bilateralFilter(thresh, 9, 75, 75)
cv2.imwrite("temp.jpg", blur)

# We read the image from disk and use some Tesseract configs to help it read better.
config = ('-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZl1|[]$ --oem 3 --psm 6')
text = pytesseract.image_to_string(Image.open("temp.jpg"), config=config)


# Tesseract sometimes messes up so we're going to correct some common mistakes.
boggle = ''.join(text.split('\n'))
fix = []
for char in boggle:
    if char == "l" or char == "|" or char == "[" or char == "]":
        fix.append("I")
    elif char == "$":
        fix.append("S")
    else:
        fix.append(char)
b = ''.join(fix)
print(b)


# You need to get your own API key for the boggle solver
url = "https://codebox-boggle-v1.p.rapidapi.com/" + b

headers = {
    'x-rapidapi-host': "codebox-boggle-v1.p.rapidapi.com",
    'x-rapidapi-key': "INSERT KEY HERE"
    }

if len(boggle) != 16:
    print("OCR Failed")
else:
    response = requests.request("GET", url, headers=headers)
    print(sorted([t[2:-1] for t in response.text[1:-1].split(",")], key=len)[::-1])




