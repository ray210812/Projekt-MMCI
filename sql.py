import mysql.connector 
import json
from datetime import datetime
def connect():
  Servername = 'localhost' # Rechnername (localhost ist dein eigener Rechner)
  Benutzer   = 'root'
  Passwort   = '' #muss angepasst werden
  Datenbank  = 'mydb'

  # Verbindung mit der Datenbank
  con = mysql.connector.connect(
              host     = Servername,
              user     = Benutzer,
              password = Passwort)
  con.database = Datenbank
  return con


#Pflanze in DB anlegen
def insert(id,düngen,name,gießen,standort,text):
  now = datetime.now()


  formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')
  con = connect()
  cursor = con.cursor()
  SQLBefehl = """
          INSERT INTO `Pflanzen` (`Bezeichnung`, `UUID`, `Angelegt_am`, `Text`)
          VALUES (%s, %s, %s, %s)
          """
          
  values = (str(name), str(id), str(formatted_now), str(text))
  cursor.execute(SQLBefehl,values)
  con.commit()
  if düngen:
    SQLBefehl = """
INSERT INTO `Label_has_Pflanzen` (`Label_ID`, `Pflanzen_ID`)
VALUES (
  (SELECT `ID` FROM Label WHERE Bezeichnung=%s),
  (SELECT `ID` FROM Pflanzen WHERE Bezeichnung=%s AND UUID=%s)
)
"""
    values = (str("dungen"), str(name), str(id))
    cursor.execute(SQLBefehl, values)
    con.commit()

  for a in gießen:
    SQLBefehl = """
INSERT INTO `Label_has_Pflanzen` (`Label_ID`, `Pflanzen_ID`)
VALUES (
  (SELECT `ID` FROM Label WHERE Bezeichnung=%s),
  (SELECT `ID` FROM Pflanzen WHERE Bezeichnung=%s AND UUID=%s)
)
"""
    values = (str(a),str(name), str(id))
    cursor.execute(SQLBefehl,values)
    con.commit()

  for a in standort:
    SQLBefehl = """
INSERT INTO `Label_has_Pflanzen` (`Label_ID`, `Pflanzen_ID`)
VALUES (
  (SELECT `ID` FROM Label WHERE Bezeichnung=%s),
  (SELECT `ID` FROM Pflanzen WHERE Bezeichnung=%s AND UUID=%s)
)
"""
    values = (str(a),str(name), str(id))
    cursor.execute(SQLBefehl,values)
    con.commit()

  now = datetime.now().date()


  formatted_now = now.strftime('%Y-%m-%d')

  SQLBefehl = """
INSERT INTO `Bilder(original)` (`Bildbezeichnung`, `Pfad`, `Pflanzen_ID` ,`Datum`)
VALUES (%s, %s, (SELECT `ID` FROM Pflanzen WHERE Bezeichnung=%s AND UUID=%s), %s)
"""
  values = (str(id)+'.jpg',str('static/Upload/'), str(name),str(id),str(formatted_now))
  cursor.execute(SQLBefehl,values)

  SQLBefehl = """
INSERT INTO `Bilder(bearbeitet)` (`Bildbezeichnung`, `Pfad`, `Pflanzen_ID` ,`Datum`)
VALUES (%s, %s, (SELECT `ID` FROM Pflanzen WHERE Bezeichnung=%s AND UUID=%s), %s)
"""
  values = (str(id)+'.jpg',str('static/Auswertungen/'), str(name),str(id),str(formatted_now))
  cursor.execute(SQLBefehl,values)
  con.commit()

  SQLBefehl = """
          INSERT INTO `Gießen` (`Datum`, `Pflanzen_ID`)
          VALUES (%s,  (SELECT `ID` FROM Pflanzen WHERE Bezeichnung=%s AND UUID=%s))
          """
          
  values = (str(formatted_now), str(name),str(id))
  cursor.execute(SQLBefehl,values)
  con.commit()
  
  cursor.close()

  con.disconnect()


def getallplants():
  con = connect()
  querry='''Select * from Pflanzen'''
  cursor = con.cursor(dictionary=True)  
  cursor.execute(querry)
  results = cursor.fetchall()
  cursor.close()

  con.disconnect()
  return results

def getInformation(id):
  con = connect()
  querry='''SELECT a.id, b.pfad as pfadOriginal,b.Datum,b.bildbezeichnung as original ,c.pfad as pfadBearbeitet,c.bildbezeichnung as bearbeitet

FROM Pflanzen a 
JOIN `Bilder(original)` b ON a.ID = b.Pflanzen_ID
left join `Bilder(bearbeitet)` c on a.ID = c.Pflanzen_ID
where a.id=%s
 ;'''
  
  value=(id)
  cursor = con.cursor(dictionary=True)  
  cursor.execute(querry,(value,))
  result = cursor.fetchall()

  querry=''' select a.ID,c.Bezeichnung
 from Pflanzen a join label_has_pflanzen b on a.ID= b.Pflanzen_ID
 join label c on b.Label_ID=c.ID 
 where a.id=%s
 ;'''
  cursor.execute(querry,(value,))
  result1 = cursor.fetchall()

  querry='''   select a.ID,a.bezeichnung,b.Datum
 from Pflanzen a join gießen b on a.ID= b.Pflanzen_ID
 where a.id=%s
 ;'''
  cursor.execute(querry,(value,))
  result2 = cursor.fetchall()

  querry='''Select * from Pflanzen where ID=%s'''
  cursor.execute(querry,(value,))
  result3 = cursor.fetchall()
  print (result1[0]['ID'])
  #print (result[0]ID)
  cursor.close()

  con.disconnect()
  
  return result,result1,result2,result3


def getallplants():
  con = connect()
  querry='''Select * from Pflanzen'''
  cursor = con.cursor(dictionary=True)  
  cursor.execute(querry)
  results = cursor.fetchall()
  cursor.close()

  con.disconnect()
  return results

def getBenachrichtigung():
  con = connect()
  querry='''select Datum, Bezeichnung, Pflanzen_ID as ID  from Benachrichtigung b join Pflanzen a on a.ID=b.Pflanzen_ID '''
  cursor = con.cursor(dictionary=True)  
  cursor.execute(querry)
  results = cursor.fetchall()
  cursor.close()

  con.disconnect()
  return results


def deleteBenachrichtigung(ID):
  con = connect()
  querry='''delete from Benachrichtigung where Pflanzen_ID=%s; '''
  value = (ID)
  cursor = con.cursor(dictionary=True)  
  cursor.execute(querry,(value,))
  now = datetime.now().date()


  formatted_now = now.strftime('%Y-%m-%d')
  querry='''INSERT INTO `Gießen` ( `Datum`, `Pflanzen_ID`)
          VALUES (%s, %s);
          '''
  values = (str(formatted_now), str(ID))
  cursor.execute(querry,values)
  con.commit()
  cursor.close()

  con.disconnect()
  return 

def getInformationasJSON():
  con = connect()
  querry='''Select Pflanzen.ID, Bezeichnung  from Pflanzen join Benachrichtigung on Pflanzen.ID= Benachrichtigung.Pflanzen_ID; '''
  querry2='''select Label.Bezeichnung as Bezeichnung_Label, Pflanzen_ID, Pflanzen.Bezeichnung from Label_has_Pflanzen join Label join Pflanzen on Pflanzen.ID=Pflanzen_ID where Label_ID=Label.ID ;'''
  
  cursor = con.cursor(dictionary=True)  
  cursor.execute(querry)
  results = cursor.fetchall()

  cursor = con.cursor(dictionary=True)  
  cursor.execute(querry2)
  results1 = cursor.fetchall()

  json_results = {
    "Benachrichtigung": results,
    "Labels": results1
  }


  json_output = json.dumps(json_results, ensure_ascii=False, indent=4)

  with open("test.json", 'w', encoding='utf-8') as file:
    file.write(json_output)


  print(json_output)

  return json_output





#erzeugt eine Json mit allgemeinen Informationen von Pflanze + Benachrichtigungen
getInformationasJSON()
'''
def load_json_data():
    json_data = {
        "Benachrichtigung": [
            {
                "Pflanzen_ID": 2,
                "Bezeichnung": "Test2",
                "Datum": "22.08.2024"
            }
        ],
        "Labels": [
            {
                "Bezeichnung_Label": "halb sonnig schattig",
                "Pflanzen_ID": 2,
                "Bezeichnung": "Test2"
            },
            {
                "Bezeichnung_Label": "halb sonnig schattig",
                "Pflanzen_ID": 3,
                "Bezeichnung": "Test3"
            },
            {
                "Bezeichnung_Label": "halb sonnig schattig",
                "Pflanzen_ID": 5,
                "Bezeichnung": "Test 5"
            },
            {
                "Bezeichnung_Label": "halb sonnig schattig",
                "Pflanzen_ID": 6,
                "Bezeichnung": "Test 6"
            },
            {
                "Bezeichnung_Label": "halb sonnig schattig",
                "Pflanzen_ID": 8,
                "Bezeichnung": "Test8"
            },
            {
                "Bezeichnung_Label": "halb sonnig schattig",
                "Pflanzen_ID": 11,
                "Bezeichnung": "Test11"
            },
            {
                "Bezeichnung_Label": "halb sonnig schattig",
                "Pflanzen_ID": 12,
                "Bezeichnung": "Test 12"
            },
            {
                "Bezeichnung_Label": "halb sonnig schattig",
                "Pflanzen_ID": 14,
                "Bezeichnung": "Test 13"
            },
            {
                "Bezeichnung_Label": "keine Sonne",
                "Pflanzen_ID": 1,
                "Bezeichnung": "Test"
            },
            {
                "Bezeichnung_Label": "keine Sonne",
                "Pflanzen_ID": 3,
                "Bezeichnung": "Test3"
            },
            {
                "Bezeichnung_Label": "keine Sonne",
                "Pflanzen_ID": 7,
                "Bezeichnung": "Test 7"
            },
            {
                "Bezeichnung_Label": "keine Sonne",
                "Pflanzen_ID": 8,
                "Bezeichnung": "Test8"
            },
            {
                "Bezeichnung_Label": "keine Sonne",
                "Pflanzen_ID": 11,
                "Bezeichnung": "Test11"
            },
            {
                "Bezeichnung_Label": "mittel gießen",
                "Pflanzen_ID": 1,
                "Bezeichnung": "Test"
            },
            {
                "Bezeichnung_Label": "mittel gießen",
                "Pflanzen_ID": 2,
                "Bezeichnung": "Test2"
            },
            {
                "Bezeichnung_Label": "mittel gießen",
                "Pflanzen_ID": 4,
                "Bezeichnung": "Test4"
            },
            {
                "Bezeichnung_Label": "mittel gießen",
                "Pflanzen_ID": 6,
                "Bezeichnung": "Test 6"
            },
            {
                "Bezeichnung_Label": "mittel gießen",
                "Pflanzen_ID": 8,
                "Bezeichnung": "Test8"
            },
            {
                "Bezeichnung_Label": "mittel gießen",
                "Pflanzen_ID": 11,
                "Bezeichnung": "Test11"
            },
            {
                "Bezeichnung_Label": "schattig",
                "Pflanzen_ID": 11,
                "Bezeichnung": "Test11"
            },
            {
                "Bezeichnung_Label": "sonnig",
                "Pflanzen_ID": 1,
                "Bezeichnung": "Test"
            },
            {
                "Bezeichnung_Label": "sonnig",
                "Pflanzen_ID": 4,
                "Bezeichnung": "Test4"
            },
            {
                "Bezeichnung_Label": "sonnig",
                "Pflanzen_ID": 9,
                "Bezeichnung": "Test 9"
            },
            {
                "Bezeichnung_Label": "sonnig",
                "Pflanzen_ID": 10,
                "Bezeichnung": "Test 10"
            },
            {
                "Bezeichnung_Label": "viel gießen",
                "Pflanzen_ID": 3,
                "Bezeichnung": "Test3"
            },
            {
                "Bezeichnung_Label": "viel gießen",
                "Pflanzen_ID": 12,
                "Bezeichnung": "Test 12"
            },
            {
                "Bezeichnung_Label": "viel gießen",
                "Pflanzen_ID": 14,
                "Bezeichnung": "Test 13"
            },
            {
                "Bezeichnung_Label": "wenig gießen",
                "Pflanzen_ID": 5,
                "Bezeichnung": "Test 5"
            },
            {
                "Bezeichnung_Label": "wenig gießen",
                "Pflanzen_ID": 7,
                "Bezeichnung": "Test 7"
            },
            {
                "Bezeichnung_Label": "wenig gießen",
                "Pflanzen_ID": 10,
                "Bezeichnung": "Test 10"
            },
            {
                "Bezeichnung_Label": "dungen",
                "Pflanzen_ID": 1,
                "Bezeichnung": "Test"
            },
            {
                "Bezeichnung_Label": "dungen",
                "Pflanzen_ID": 3,
                "Bezeichnung": "Test3"
            },
            {
                "Bezeichnung_Label": "dungen",
                "Pflanzen_ID": 5,
                "Bezeichnung": "Test 5"
            },
            {
                "Bezeichnung_Label": "dungen",
                "Pflanzen_ID": 8,
                "Bezeichnung": "Test8"
            },
            {
                "Bezeichnung_Label": "dungen",
                "Pflanzen_ID": 9,
                "Bezeichnung": "Test 9"
            },
            {
                "Bezeichnung_Label": "dungen",
                "Pflanzen_ID": 11,
                "Bezeichnung": "Test11"
            },
            {
                "Bezeichnung_Label": "dungen",
                "Pflanzen_ID": 12,
                "Bezeichnung": "Test 12"
            },
            {
                "Bezeichnung_Label": "dungen",
                "Pflanzen_ID": 14,
                "Bezeichnung": "Test 13"
            }
        ]
    }
    return json.loads(json_data)

data = load_json_data()
answer=""
for line in data['Benachrichtigung']:
  answer += "Benachrichtigung vom " + str(line["Datum"]) +" Die Pflanze " +str(line['Bezeichnung']) +" benötigt Wasser"
if not answer :
            answer = "keine Benachrichtigungen!"
print(answer)
'''