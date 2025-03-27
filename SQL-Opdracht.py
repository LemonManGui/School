import sqlite3 as SQL

# Connect to db
db = SQL.connect("/Users/gui/Desktop/School/originaldocument/Webwinkel.db")
cur = db.cursor()

# Fetching info
query = '''
SELECT
    B.Besteldatum,
    K.Achternaam,
    SUM(BR.Aantal) AS "Aantal art.",
    SUM(BR.Aantal * A.Prijs) AS "Totaalbedrag"
FROM
    Bestellingen AS B,
    Klanten AS K,
    Bestelregels AS BR,
    Artikelen AS A
WHERE 
    B.Klantnr = K.Klantnr
    AND B.Bestelnr = BR.Bestelnr
    AND BR.Artikelnr = A.Artikelnr
    AND strftime('%Y', B.Besteldatum) = '2014'
GROUP BY
    B.Bestelnr, 
    B.Besteldatum, 
    K.Achternaam
ORDER BY
    B.Besteldatum;
'''
cur.execute(query)
res = cur.fetchall()

# Rapport genereren
rapport = "Besteldatum\tKlantnaam\tAantal art.\tTotaalbedrag\n"
for rij in res:
    besteldatum, achternaam, totaal_ant, totaal_bedrag = rij
    rapport += f"{besteldatum}\t{achternaam}\t{totaal_ant}\t{totaal_bedrag}\n"

# Rapport opslaan als .txt bestand    
with open('rapport_2014.txt', 'w') as bestand:
    bestand.write(rapport)

# Sluit connectie
db.close()