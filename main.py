from flask import Flask , render_template ,request, redirect, url_for, jsonify
import segno
from io import BytesIO
import base64
import cv2
import uuid
import os
import Yolo
import Tesseract
import re
import sql


app = Flask(__name__)
#get: Startseite aufrufen
#post: Bild speichern (localer Upload) und weiterleitung
@app.route("/" ,methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'datei' in request.files :
            file = request.files['datei']
            variable =  request.form.get('Id', None)
            if variable==None:
                variable= uuid.uuid4()
            file_path = os.path.join('static/Upload', str(variable)+".jpg")
            file.save(file_path)

                
            return edit(variable)#jsonify(success=True, variable=variable, file_path=file_path)


    return  render_template('index.html')


#upload von extern speichern, ohne weiterleitung
@app.route("/uploadcompleted" ,methods=["GET", "POST"])
def uploadMobile():
    if request.method == "POST":
        if 'datei' in request.files :
            file = request.files['datei']
            variable =  request.form.get('Id', None)
            if variable==None:
                variable= uuid.uuid4()
            file_path = os.path.join('static/Upload', str(variable)+".jpg")
            file.save(file_path)
            return jsonify(success=True, variable=variable, file_path=file_path)


    return render_template('index.html')

#Upload Seite extern
@app.route("/upload/<variable>")
def upload(variable):
    return render_template('upload.html', variable=variable)

#Seite um Pflanzen hinzuzufügen Localer Upload  + QR Code für externen Upload
@app.route("/add")
def add():
    myuuid= uuid.uuid4()

    qrcode = segno.make_qr("http://192.168.0.28:5000/upload/"+str(myuuid))
    buffer = BytesIO()
    qrcode.save(buffer, kind='png',scale=10)
    buffer.seek(0) # für pointer
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    img_data_url = f"data:image/png;base64,{img_str}"

    
    return render_template('add.html', image_data_url=img_data_url, UUID=str(myuuid))

#Überprüft ob Bild mit übergebenen Namen existiert
@app.route("/check_file/<filename>")
def check_file(filename):
    file_path = os.path.join('static/Upload', str(filename)+".jpg")
    file_exists = os.path.exists(file_path)
    return jsonify(exists=file_exists)
#Bild wird analysiert +Seite zum Auswahl der Eigenschaften anzeigen
@app.route("/editimage/<id>")
def edit(id):
    file_path = os.path.join('static/Upload', str(id)+".jpg")
    file_exists = os.path.exists(file_path)
    if  not file_exists :
        return "kein Bild hochgeladen"
    image =cv2.imread("static/Upload/"+str(id)+".jpg")
    text,a,b=Tesseract.prepareImage(image)
    result =Yolo.YoloModel.prediction(image)
    image1=Tesseract.editImage(a,image)
    image1=Yolo.YoloModel.draw_predictions(image1,result)
    success =cv2.imwrite('static/Auswertungen/'+str(id)+'.jpg', image1)
    print(success)
    labels = Yolo.YoloModel.getObjekts(result)
    result=analyse((str(text)+str(b)),labels)
    _, buffer = cv2.imencode('.png', image1)
    img_str = base64.b64encode(buffer).decode('utf-8')
    img_data_url = f"data:image/png;base64,{img_str}"
    return render_template('editImage.html', image_data_url=img_data_url, dictionary=result,id=id, text=str(text))

# Nach Auswahl der Eigenschaften Daten in DB speichern
@app.route("/save",methods=["GET", "POST"])
def save():
    if request.method == "POST":
        id = request.form.get('id')
        Düngen=request.form.get('Düngen')
        name = request.form.get('name')
        rubrik_values = request.form.getlist('rubrik')
        standort_values = request.form.getlist('standort')
        text = request.form.get('text')
        sql.insert(id,Düngen,name,rubrik_values,standort_values,text)
        return index()


    return "error"


#Info Seite
@app.route("/info")
def info():
    result=sql.getallplants()
      
    return render_template('info.html', rows=result)


#Benachrichtigung Seite
@app.route("/benachrichtigung",methods=["GET", "POST"])
def benachrichtigung():
    result=sql.getBenachrichtigung()
      
    return render_template('benachrichtigung.html', rows=result)
#Benachrichtigung löschen
@app.route("/benachrichtigung/<id>",methods=["GET", "POST"])
def completed(id):
    sql.deleteBenachrichtigung(id)
    return benachrichtigung()


#Informationen zu einzelner Pflanze anzeigen
@app.route("/info/<variable>" )
def info2(variable):
    a,b,c,d =sql.getInformation(variable)
    dictonary ={
        'Zimmerpflanze':"", 
        'dungen':"", 
        'halb sonnig schattig':"", 
        'keine Sonne':"", 
        'mittel gießen':"", 
        'schattig':"", 
        'sonnig':"", 
        'viel gießen':"",
        'wenig gießen':""
    }

    for label in b:
        dictonary[label["Bezeichnung"]]="checked"
    return render_template('info2.html', a=a,dictionary=dictonary,c=c,d=d)


# Wenn Symbole erkannt wurden, wird ein Dictionary mit den Eigenschaften als "checked" zurück gegeben . Ansonsten wird eine Text Analyse versucht ( Sucht nach Signalwörtern -> Falls gefunden innerhalb eines begrenzten Bereichs nach Maßeinheit suchen) "
def analyse(text,labels):
    dictonary ={
        'Zimmerpflanze':"", 
        'dungen':"", 
        'halb sonnig schattig':"", 
        'keine Sonne':"", 
        'mittel giesen':"", 
        'schattig':"", 
        'sonnig':"", 
        'viel giesen':"",
        'wenig giesen':""
    }
    if len(labels)!=0:
        for text in labels:
            dictonary[text]="checked"
        return dictonary
    
    bewässerungs_wörter = [
        "feucht",
        "gießen",
        "bewässern",
        "benetzen",
        "sprühen",
        "tröpfchen",
        "hydratisieren",
        "wässern",
        "feucht halten",
        "wasser"

    ]
    

    wenig_worte = [
        "gering",
        "minimal",
        "knapp",
        "spärlich",
        "beschränkt",
        "selten",
        "wenig",
        "klein",
        "marginal",
        "wenig",
        "gelegentlich",
        "nicht",
        "sparsam"
    ]


    mittel_worte = [
        "moderat",
        "durchschnittlich",
        "mäßig",
        "gemäßigt",
        "normal",
        "ausgewogen",
        "mittelmäßig",
        "mäßig",
        "entsprechend",
        "regelmäßig",
        "rythmus",
        "gleichmäßig"
    ]

    viel_worte = [
        "reichlich",
        "umfangreich",
        "groß",
        "vielfältig",
        "zahlreich",
        "überschwänglich",
        "intensiv",
        "erheblich",
        "stark",
        "ausgedehnt"
    ]
    text=text.lower()
    signal_pattern = '|'.join(bewässerungs_wörter)
    match =re.findall(signal_pattern,text)
    if(match):
        quantity_pattern= '|'.join(wenig_worte)
        pattern = rf'({quantity_pattern}).{{0,50}}({signal_pattern})|({signal_pattern}).{{0,50}}({quantity_pattern})'
        pattern =  re.compile(pattern, re.IGNORECASE | re.DOTALL) # Zeilenumbruch ignorieren
        match=re.findall(pattern,text)
        if match:
            dictonary['wenig giesen']="checked"
        quantity_pattern= '|'.join(mittel_worte)
        pattern = rf'({quantity_pattern}).{{0,50}}({signal_pattern})|({signal_pattern}).{{0,50}}({quantity_pattern})'
        pattern =  re.compile(pattern, re.IGNORECASE | re.DOTALL)
        match=re.findall(pattern,text)
        if match:
            dictonary['mittel giesen']="checked"
        quantity_pattern= '|'.join(viel_worte)
        pattern = rf'({quantity_pattern}).{{0,50}}({signal_pattern})|({signal_pattern}).{{0,50}}({quantity_pattern})'
        pattern =  re.compile(pattern, re.IGNORECASE | re.DOTALL)
        match=re.findall(pattern,text)
        if match:
            dictonary['viel giesen']="checked"
    
    match =re.findall("düngen",text)
    if match:
        dictonary['dungen']="checked"


    standort_wortliste = [
    "position", "lage", "ort", "platz", "stelle", "standortwahl", 
    "standort",  "niederlassung",  
    "sitz", "stützpunkt"
    ]

    hell_wortliste = [
    "hell","sonnig","licht"
    ]

    schattig_wortliste=["schattig","schatten"]

    verneinung_wortliste=["kein","ohne","vermeiden"]

    sonnig_wortliste = [
    "sonnig","sonne","direkte sonne"
    ]
    patternStandort= '|'.join(standort_wortliste)
    match=re.findall(patternStandort,text)
    if match:
        pattern= '|'.join(hell_wortliste)
        pattern = rf'({patternStandort}).{{0,50}}({pattern})|({pattern}).{{0,50}}({patternStandort})'
        pattern =  re.compile(pattern, re.IGNORECASE | re.DOTALL)
        match=re.findall(pattern,text)
        if match:
            dictonary["sonnig"]="checked"
        pattern= '|'.join(schattig_wortliste)
        pattern = rf'({patternStandort}).{{0,50}}({pattern})|({pattern}).{{0,50}}({patternStandort})'
        pattern =  re.compile(pattern, re.IGNORECASE | re.DOTALL)
        match=re.findall(pattern,text)
        if match:
            dictonary["halb sonnig schattig"]="checked"
        pattern= '|'.join(sonnig_wortliste)
        pattern1= '|'.join(verneinung_wortliste)
        pattern = rf'({patternStandort}).{{0,50}}({pattern}).{{0,50}}({pattern1})|({patternStandort}).{{0,50}}({pattern1}).{{0,50}}({pattern})'
        pattern =  re.compile(pattern, re.IGNORECASE | re.DOTALL)
        match=re.findall(pattern,text)
        if match:
            dictonary["keine Sonne"]="checked"
        
    return dictonary

if __name__ == "__main__":
    
#analyse("""Wwächst sehr schlank und kann hohe Stamrr =
#bilden. Beheimatet ist diese in Madagaskar
#Dracaena marginata hat glänzend dunkelgrun=
#und braunrot gerandete Blätter.

#Standort
#Bevorzugt einen hellen Standort ohne direkte
#Sonneneinstrahlung. Die ideale Raumtemperatu
#der Dracaena liegt zwischen 18 und 24 C.

#Pflege
#Während der Wachstumsperiode
#regelmäßig gießen und alle 14 Tage düngen
#In den Wintermonaten kann das Substrat
#ab und zu austrocknen.

#Detiner Gartencenter  Dehner Gartencenter BE Pilanzenpass
#| ErnbH &tO.KG Österreich GmbH & Co. KG Plant Passport
#. auworther Str. 35 Pluskaufstr. 10 A Dracaena marginala
#a ee: ji A 4061 Pasching B DE-BY-112

#Ä >, Service@dehner.dt
#= gehner.at
#8""",[])
#"""
    #edit("06d89a8b-44a4-4ba1-a983-8124501d825e")
    app.run(host="192.168.0.28")
    