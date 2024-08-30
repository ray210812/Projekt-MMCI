from PIL import Image
import pytesseract
import cv2
import os
import numpy as np

#pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Marc\AppData\Local\Programs\Tesseract-OCR/tesseract.exe'



def prepareImage(image):
    # Bild in Graustufen umwandeln
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    gray_image = cv2.medianBlur(gray_image, 3)
    custom_config = r'--oem 3--psm 1'
    manual_thresh_value = 200  # Setzen Sie diesen Wert nach Bedarf
    _, preparedImage = cv2.threshold(gray_image, manual_thresh_value, 255, cv2.THRESH_BINARY)
    extrahierter_text = pytesseract.image_to_string(preparedImage, lang='deu', config=custom_config)
    count = len(extrahierter_text)
    cv2.imwrite(r'testergebnis1.jpg', preparedImage)

    manual_thresh_value = 100  # Setzen Sie diesen Wert nach Bedarf
    _, preparedImage1 = cv2.threshold(gray_image, manual_thresh_value, 255, cv2.THRESH_BINARY)
    cv2.imwrite(r'testergebnis2.jpg', preparedImage1)
    extrahierter_text2 = pytesseract.image_to_string(preparedImage1, lang='deu', config=custom_config)
    count2 = len(extrahierter_text2)

    manual_thresh_value = 150  # Setzen Sie diesen Wert nach Bedarf
    _, preparedImage2 = cv2.threshold(gray_image, manual_thresh_value, 255, cv2.THRESH_BINARY)
    cv2.imwrite(r'testergebnis3.jpg', preparedImage2)
    extrahierter_text3 = pytesseract.image_to_string(preparedImage2, lang='deu', config=custom_config)
    count3 = len(extrahierter_text3)

    if count >= count2 & count >= count3:
        return extrahierter_text, preparedImage
    if count2 >= count3:
        return extrahierter_text2, preparedImage1
    else:
        return extrahierter_text3, preparedImage2


def editImage(preparedImage, image):

    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(preparedImage, config=custom_config, lang='deu',
                                     output_type=pytesseract.Output.DICT)


    n_boxes = len(data['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])

        if w > 10 and h > 10:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    word_data = []
    for i in range(n_boxes):
        if data['text'][i].strip():  # Ignoriere leere Wörter
            word_info = {
                'word': data['text'][i],
                'left': data['left'][i],
                'top': data['top'][i],
                'width': data['width'][i],
                'height': data['height'][i]
            }
            word_data.append(word_info)

    return image



# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
# morphed_image = cv2.morphologyEx(preparedImage, cv2.MORPH_CLOSE, kernel)

#files = os.listdir(r'test')

#with open("datei.txt", "w", encoding="utf-8") as text:
    # Schreibe den String in die Datei

 #   for file in files :
  #      a, b = prepareImage(cv2.imread(r'test'+'\\'+file))
   #     text.write(file+'\n')
    #    text.write(a+'\n')
     #   cv2.imwrite(r'testergebnis\\'+file, b)

    #text.close()
#a,b = prepareImage(cv2.imread(r'static\\test'+'\\PXL_20240813_155317004.MP.jpg'))

#cv2.imwrite(r'static\\Auswertungen\\PXL_20240813_155335143.MP.jpg', b)
#print(a)
