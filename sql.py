import mysql.connector 
from datetime import datetime
def connect():
  Servername = 'localhost' # Rechnername (localhost ist dein eigener Rechner)
  Benutzer   = 'root'
  Passwort   = 'masche210'
  Datenbank  = 'mydb'

  # Verbindung mit der Datenbank
  con = mysql.connector.connect(
              host     = Servername,
              user     = Benutzer,
              password = Passwort)
  con.database = Datenbank
  return con



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
  # Abmelden
  con.disconnect()


def getallplants():
  con = connect()
  querry='''Select * from Pflanzen'''
  cursor = con.cursor(dictionary=True)  
  cursor.execute(querry)
  results = cursor.fetchall()
  cursor.close()
  # Abmelden
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
  # Abmelden
  con.disconnect()
  
  return result,result1,result2,result3


def getallplants():
  con = connect()
  querry='''Select * from Pflanzen'''
  cursor = con.cursor(dictionary=True)  
  cursor.execute(querry)
  results = cursor.fetchall()
  cursor.close()
  # Abmelden
  con.disconnect()
  return results

def getBenachrichtigung():
  con = connect()
  querry='''select Datum, Bezeichnung, Pflanzen_ID as ID  from Benachrichtigung b join Pflanzen a on a.ID=b.Pflanzen_ID '''
  cursor = con.cursor(dictionary=True)  
  cursor.execute(querry)
  results = cursor.fetchall()
  cursor.close()
  # Abmelden
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
  # Abmelden
  con.disconnect()
  return 



#deleteBenachrichtigung(12)