from PIL import Image
import pytesseract
import cv2
import os
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Marc\AppData\Local\Programs\Tesseract-OCR/tesseract.exe'



def prepareImage(image):
    # Bild in Graustufen umwandeln
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # Rauschen reduzieren
    gray_image = cv2.medianBlur(gray_image, 3)
    custom_config = r'--oem 3--psm 6'
    # Manuelle Schwellenwertsetzung
    manual_thresh_value = 200  # Setzen Sie diesen Wert nach Bedarf
    _, thresh_image = cv2.threshold(gray_image, manual_thresh_value, 255, cv2.THRESH_BINARY)
    extrahierter_text = pytesseract.image_to_string(thresh_image, lang='deu', config=custom_config)
    count = len(extrahierter_text)
    cv2.imwrite(r'testergebnis1.jpg', thresh_image)

    manual_thresh_value = 100  # Setzen Sie diesen Wert nach Bedarf
    _, thresh_image1 = cv2.threshold(gray_image, manual_thresh_value, 255, cv2.THRESH_BINARY)
    cv2.imwrite(r'testergebnis2.jpg', thresh_image1)
    extrahierter_text2 = pytesseract.image_to_string(thresh_image1, lang='deu', config=custom_config)
    count2 = len(extrahierter_text2)

    manual_thresh_value = 150  # Setzen Sie diesen Wert nach Bedarf
    _, thresh_image2 = cv2.threshold(gray_image, manual_thresh_value, 255, cv2.THRESH_BINARY)
    cv2.imwrite(r'testergebnis3.jpg', thresh_image2)
    extrahierter_text3 = pytesseract.image_to_string(thresh_image2, lang='deu', config=custom_config)
    count3 = len(extrahierter_text3)

    if count >= count2 & count >= count3:
        return extrahierter_text, editImage(thresh_image, image)
    if count2 >= count3:
        return extrahierter_text2, editImage(thresh_image1, image)


    else:
        return extrahierter_text3, editImage(thresh_image2, image)


def editImage(thresh_image, image):
    # Texterkennung durchführen und Positionsdaten abrufen
    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(thresh_image, config=custom_config, lang='deu',
                                     output_type=pytesseract.Output.DICT)

    # Über alle erkannten Textfelder iterieren und Rechtecke zeichnen
    n_boxes = len(data['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        # Filtern
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



image = cv2.imread(r'test'+'\\'+"PXL_20240813_155335143.MP.jpg")
print(pytesseract.image_to_string(image))
#files = os.listdir(r'test')

#with open("datei.txt", "w", encoding="utf-8") as text:
    # Schreibe den String in die Datei

 #   for file in files :
  #      a, b = prepareImage(cv2.imread(r'test'+'\\'+file))
   #     text.write(file+'\n')
    #    text.write(a+'\n')
     #   cv2.imwrite(r'testergebnis\\'+file, b)

    #text.close()
