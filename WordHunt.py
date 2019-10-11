from PIL import Image
import numpy as np
import cv2, time, pytesseract
from PIL import ImageGrab
import requests

capture = None
img = ImageGrab.grab(bbox=(175,600,800,1500))
img_np = np.array(img)
gray = cv2.cvtColor(img_np,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)[1]
#dn = cv2.fastNlMeansDenoisingColored(thresh, None, 10, 10, 7, 21)
#dilate = cv2.dilate(thresh, kernel, iterations = 2)

blur = cv2.bilateralFilter(thresh, 9, 75, 75)
#lap = cv2.Laplacian(blur, cv2.CV_64F)
#small = cv2.resize(blur, None, fx = 1, fy = 1, interpolation=cv2.INTER_CUBIC)
config = ('-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZl1|[]$ --oem 3 --psm 6')
cv2.imwrite("temp.jpg", blur)
text = pytesseract.image_to_string(Image.open("temp.jpg"), config=config)
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
#print(response.text.sort(key = lambda s: len(s)))




