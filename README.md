# GamePigeonTools
Computer Assisted tools for iMessage GamePigeon games, using Tesseract OCR

# How it works
The whole process can be broken down into a few steps

1) We take a screenshot of the screen
2) We use a couple of techniques including thresholding and blurring to make the image easier for Tesseract to read
3) We extract the text from the image
4) We generate the answer with an external API, or with some other algorithm

# How do you use it
Before we begin:
You'll need to install all the required dependencies.
You'll need an iPhone that can play GamePigeon, and a Mac so you can use the QuickTime screen record.

1) Connect your iPhone to the Mac and open up QuickTime, and create a new moview recording. Select your iPhone as the video source.
2) Position the video recording close to the left side of the screen. You'll need to adjust the screenshot coordinates in the code
if you're not running this on 2015 Macbook Pro. Sorry!
3) Open up the game, and make sure the letters are visible.
4) Run the program with "python3 Anagrams.py" or "python3 WordHunt.py". You can check the screenshot output via the temp jpg files
created in the directory.


