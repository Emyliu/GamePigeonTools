import dawg
from itertools import combinations
import collections
from collections import Counter
from PIL import Image
import numpy as np
import cv2, time, pytesseract
from PIL import ImageGrab


# Take the screenshot, and turn it into a numpy array so we can use cv2 methods
img = ImageGrab.grab(bbox=(80,1400,900,1700))
img_np = np.array(img)


# In order:
# 1) Make the image grayscale
# 2) Use a binary threshold to remove all artifacts that are not letters
# 3) Blur the image to make it easier for Tesseract to read.
# 4) Write the image to disk.
gray = cv2.cvtColor(img_np,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)[1]
blur = cv2.bilateralFilter(thresh, 9, 75, 75)
cv2.imwrite("temp2.jpg", blur)

# We read the image from disk and use some Tesseract configs to help it read better.
config = ('-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZl1|[]$ --oem 3 --psm 7')
text = pytesseract.image_to_string(Image.open("temp2.jpg"), config=config)


# Tesseract sometimes messes up so we're going to correct some common mistakes.
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


# We're going to read a textfile and create a Trie from it.
words = open('/Users/edmondliu/WordHunt/collins.txt', 'r').read().splitlines()
trie = dawg.DAWG(words)
results = set()
ctr = collections.Counter(x)

# I know that this can be more efficient, I'll get around to it.
# Basically generates every possible word and checks the dictionary Trie to see if it exists.
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


# Return the values
generateWords("", ctr)
print(sorted(list(results), key=len, reverse=True))


        
