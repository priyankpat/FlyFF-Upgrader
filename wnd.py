from PIL import ImageGrab
import cv2
import pytesseract
import numpy as np
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Users\shank\Documents\Upgrader'

if __name__ == "__main__":
    # img = ImageGrab.grab(bbox=(self.tries_pos.x, self.tries_pos.y, self.tries_pos.x1, self.tries_pos.y1))
    # img.save("tries.png")
    img = ImageGrab.Image.open("tries.png")
    cv2.imshow('raw', cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    upscaled = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    cv2.imshow('us', cv2.cvtColor(np.array(upscaled), cv2.COLOR_RGB2BGR))
    # cv2.imwrite("tries_upscaled_image.png", upscaled)

    custom_config = r'--oem 3 --psm 10 outputbase digits -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(upscaled, config=custom_config)

    # print("[Tries] Recognized text:", text.strip())
    print(text.strip())
    cv2.waitKey(0)