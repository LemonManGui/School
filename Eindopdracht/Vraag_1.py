import sqlite3 as SQL

# Connect SQL to db
file_path = "/Users/gui/Desktop/School/Eindopdracht/chinook.db" # Vervang met /Path/To/DataBase_file.db
db = SQL.connect(file_path)
cur = db.cursor()

# Query to retreve desired results
query = '''
SELECT
    AT.Name,
    AB.Title,
    SUM(I_I.Quantity) AS Total_Quantity
FROM
    Artists AS AT,
    Albums AS AB,
    Invoice_items AS I_I,
    Tracks AS T
WHERE
    AT.ArtistId = AB.ArtistId
    AND AB.AlbumId = T.AlbumId
    AND T.TrackId = I_I.TrackId
GROUP BY
    AB.AlbumId,
    AT.Name,
    AB.Title
ORDER BY
    Total_Quantity DESC
LIMIT 10;
'''

# Execute and retreve query
cur.execute(query)
res = cur.fetchall()

# Print in desired format
print("\n--- Top 10 Albums ---")
for i, rij in enumerate(res, start=1):
    name, album, quantity = rij
    print(f"{i}\t{name}\t{album}\t{quantity}")
    
# Ik zou persoonlijk printen in het format f"{i} - {name} - {album} - {quantity}" omdat dat overzichtelijker is maar de opdracht vraagt om een \t