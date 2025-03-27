import sqlite3 as SQL

db = SQL.connect("/Users/gui/Desktop/School/originaldocument/Webwinkel.db")
cur = db.cursor()
###
cur.execute(''' SELECT Bestelnr, Artikelnr, Aantal
                FROM Bestelregels
                WHERE  Bestelnr = 6;
                ''')

bestelregels = cur.fetchall()
print(bestelregels)
totaal = 0
for regel in bestelregels:
    aantal = regel[2]
    totaal += aantal
print(totaal)
###
bestelnr = int(input("Geef bestelnummer: "))
cur.execute(''' SELECT Bestelnr, Artikelnr, Aantal
                FROM Bestelregels
                WHERE Bestelnr = ?; ''', (bestelnr,) ### Variabele in SQL
            )
bestelregels = cur.fetchall()
print(bestelregels)
###
bestelnr = 15
artikelnr = 512050
aantal = 3
cur.execute(''' INSERT INTO Bestelregels
            VALUES (?, ?, ?); ''', (bestelnr, artikelnr, aantal)
            )
db.commit()

mutatie = 5
artikelnr = 512050
cur.execute('''
UPDATE Artikelen
SET Voorraad = Voorraad + ?
WHERE Artikel = ?;
''', (mutatie, artikelnr)
            )
db.commit()

bestelnr = 15
cur.execute('''
DELETE FROM BESTELREGELS
WHERE Bestelnr = ?;
''', (bestelnr)
            )
db.commit()

# Rapport
cur.execute('''
SELECT 
    B.Besteldatum, 
    K.Achternaam, 
    BR.Aantal, 
    A.Prijs * BR.Aantal AS Totaalprijs
FROM 
    Bestellingen AS B,
    Klanten AS K,
    Bestelregels AS BR,
    Artikelen AS A
WHERE
    strftime('%Y', B.Besteldatum) = '2014'
    AND B.Klantnr = K.Klantnr
    AND B.Bestelnr = BR.Bestelnr
    AND BR.Artikelnr = A.Artikelnr
''')

print(cur.fetchall())
                