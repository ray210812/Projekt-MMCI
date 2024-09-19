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

    # Kontrast erhöhen
    gray_image = cv2.equalizeHist(gray_image)

    # Manuelle Schwellenwertsetzung und adaptive Schwellenwertsetzung
    manual_thresh_value = 200
    _, thresh_image_manual = cv2.threshold(gray_image, manual_thresh_value, 255, cv2.THRESH_BINARY)
    adaptive_thresh_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Texterkennung durchführen
    custom_config = r'--oem 3 --psm 6 '
    extrahierter_text_manual = pytesseract.image_to_string(thresh_image_manual, lang='deu', config=custom_config)
    print(extrahierter_text_manual)
    extrahierter_text_adaptive = pytesseract.image_to_string(adaptive_thresh_image, lang='deu', config=custom_config)
    print(extrahierter_text_adaptive)
    # Vergleich der Textlängen
    if len(extrahierter_text_manual) >= len(extrahierter_text_adaptive):
        return extrahierter_text_manual, editImage(thresh_image_manual, image)
    else:
        return extrahierter_text_adaptive, editImage(adaptive_thresh_image, image)

def editImage(thresh_image, image):
    # Texterkennung durchführen und Positionsdaten abrufen
    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(thresh_image, config=custom_config, lang='deu', output_type=pytesseract.Output.DICT)

    # Über alle erkannten Textfelder iterieren und Rechtecke zeichnen
    n_boxes = len(data['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        # Filtern
        if w > 10 and h > 10:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

# Beispielaufruf
a, b = prepareImage(cv2.imread(r'Bilder/PXL_20240813_155703086.jpg'))
print(a)