import dawg
from itertools import combinations
import collections
from collections import Counter
from PIL import Image
import numpy as np
import cv2, time, pytesseract
from PIL import ImageGrab


capture = None
img = ImageGrab.grab(bbox=(80,1400,900,1700))
img_np = np.array(img)
gray = cv2.cvtColor(img_np,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)[1]
#dn = cv2.fastNlMeansDenoisingColored(thresh, None, 10, 10, 7, 21)
#dilate = cv2.dilate(thresh, kernel, iterations = 2)

blur = cv2.bilateralFilter(thresh, 9, 75, 75)
#lap = cv2.Laplacian(blur, cv2.CV_64F)
#small = cv2.resize(blur, None, fx = 1, fy = 1, interpolation=cv2.INTER_CUBIC)
config = ('-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZl1|[]$ --oem 3 --psm 7')
cv2.imwrite("temp2.jpg", blur)
text = pytesseract.image_to_string(Image.open("temp2.jpg"), config=config)
x = ''.join(text.split('\n'))

fix = []
for char in x:
    if char == "l" or char == "|" or char == "[" or char == "]":
        fix.append("I")
    elif char == "$":
        fix.append("S")
    else:
        fix.append(char)

x = ''.join(fix)

words = open('/Users/edmondliu/WordHunt/collins.txt', 'r').read().splitlines()
trie = dawg.DAWG(words)
results = set()
ctr = collections.Counter(x)

def generateWords(current, count):
    if current.upper() in trie:
        results.add(current)
    for x in count.keys():
        if count[x] != 0:
            k = count.copy()
            k[x] -= 1
            if k[x] == 0:
                del k[x]
            next_str = current + x
            generateWords(next_str, k)

generateWords("", ctr)
print(sorted(list(results), key=len, reverse=True))


        
