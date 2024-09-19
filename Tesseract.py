from PIL import Image
import pytesseract
import cv2
import os
import numpy as np
# Pfad zur Tesseract Instalation (für Windows benötigt)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Marc\AppData\Local\Programs\Tesseract-OCR/tesseract.exe'


# Texterkennung durchführen + vorbereitetes Bild bereitstellen
def prepareImage(image):
    # Bild in Graustufen umwandeln
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Rauschen reduzieren
    #gray_image = cv2.medianBlur(gray_image, 3)
    custom_config = r'--oem 3--psm 1'
    cv2.imwrite(r'testergebnis0.jpg', gray_image)
    manualValue = 200
    #preparedImage = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY |cv2.THRESH_OTSU)[1]
    #extrahierter_text = pytesseract.image_to_string(image , lang='deu', config=custom_config)
    #count = len(extrahierter_text)
    #print(extrahierter_text)
    #cv2.imwrite(r'testergebnis0.jpg', preparedImage)
    _, preparedImage = cv2.threshold(gray_image, manualValue, 255, cv2.THRESH_BINARY)
    extrahierter_text = pytesseract.image_to_string(preparedImage, lang='deu', config=custom_config)
    text=extrahierter_text.replace(" ","")
    text=text.replace("/n","")
    count = len(text)
    cv2.imwrite(r'testergebnis1.jpg', preparedImage)

    manualValue = 100
    _, preparedImage1 = cv2.threshold(gray_image, manualValue, 255, cv2.THRESH_BINARY)
    cv2.imwrite(r'testergebnis2.jpg', preparedImage1)
    extrahierter_text2 = pytesseract.image_to_string(preparedImage1, lang='deu', config=custom_config)
    text = extrahierter_text2.replace(" ", "")
    text = text.replace("/n", "")
    count2 = len(text)

    manualValue = 150
    _, preparedImage2 = cv2.threshold(gray_image, manualValue, 255, cv2.THRESH_BINARY)
    cv2.imwrite(r'testergebnis3.jpg', preparedImage2)
    extrahierter_text3 = pytesseract.image_to_string(preparedImage2, lang='deu', config=custom_config)
    text = extrahierter_text3.replace(" ", "")
    text = text.replace("/n", "")
    count3 = len(text)
    extrahierter_text4 ="2" #pytesseract.image_to_string(image)
    text = extrahierter_text3.replace(" ", "")
    text = text.replace("/n", "")
    count4 = len(text)
    print("1 Anzahl"+str(count)+ extrahierter_text)
    print("2 Anzahl" + str(count2)+extrahierter_text2)
    print("3 Anzahl" + str(count3)+extrahierter_text3)
    print("4 Anzahl" + str(count4) + extrahierter_text4)

    if count >= count2 and count >= count3 and count >= count4:
        return extrahierter_text, preparedImage, (extrahierter_text3+extrahierter_text2+extrahierter_text4)
    if count2 >= count3 and count2 >= count4:
        return extrahierter_text2, preparedImage1,(extrahierter_text+extrahierter_text3+extrahierter_text4)
    if count3 >= count4:
        return extrahierter_text3, preparedImage2,(extrahierter_text,extrahierter_text2+extrahierter_text4)
    else:
        return extrahierter_text4, image, (extrahierter_text, extrahierter_text2 + extrahierter_text3)

#Im Bild erkannte Objekte einzeichnen
def editImage(preparedImage, image):

    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(preparedImage, config=custom_config, lang='deu',
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


# Morphologische Operationen, um die Konturen zu bereinigen
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
#a,b,c = prepareImage(cv2.imread(r'static\\test'+'\\PXL_20240813_155317004.MP.jpg'))

#cv2.imwrite(r'static\\Auswertungen\\PXL_20240813_155335143.MP.jpg', b)
#print(a)
