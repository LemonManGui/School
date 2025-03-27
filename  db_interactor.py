import sqlite3 as SQL

filepath = "/Users/gui/Desktop/School/Eindopdracht/chinook.db"
conn = SQL.connect(filepath)
cur = conn.cursor()

def check_track():

    query = '''
        SELECT
            T.Name,
            A.Name
        FROM
            tracks AS T,
            artists AS A,
            albums AS AB
        WHERE
            T.Name LIKE ?
        AND T.AlbumId = AB.AlbumId
        AND AB.ArtistId = A.ArtistId;
        '''
    
    cmd = str(input("Zoekterm: "))

    cur.execute(query, (f"%{cmd}%",))
    res = cur.fetchall()

    if len(res) == 1:
        print(f"--- 1 track gevonden ---")
        for tup in res:
            for string in tup:
                print(string, end=' ')
        print("\n")
    
    elif len(res) > 1:
        print(f"{len(res)} tracks gevonden: ")
        for i, track in enumerate(res, start=1):
            name, artist = track
            print(f"{i} - {name} - {artist}")
        print("\n")

    else:
        print(f"--- Geen resultaat voor zoekterm '{cmd}' ---\n")

def check_playlist():

    query = '''
    SELECT 
        T.Name,
        A.Name
    FROM 
        playlists AS P,
        tracks AS T,
        artists AS A,
        playlist_track AS PT,
        albums AS AB
    WHERE
        P.Name = ?
    AND P.PlaylistId = PT.PlaylistId
    AND PT.TrackId = T.TrackId
    AND T.AlbumId = AB.AlbumId
    AND AB.ArtistId = A.ArtistId;
    '''   

    zoekterm = input("Zoek playlist: ")
    cur.execute(query, (zoekterm,))
    res = cur.fetchall() # Een lijst met tupils

    try:
        if res:
            print(f"--- {len(res)} tracks gevonden in playlist '{zoekterm}' ---")
            print(f"Toon inhoud van {zoekterm}? (Ja/Nee)")
            
            toon_inhoud = str(input("\nUw keuze: "))

            if toon_inhoud.lower() == 'ja':
                for i, track in enumerate(res, start=1):
                    tr, artist = track
                    print(f"{i} - {tr} - {artist}")

            elif toon_inhoud.lower() == 'nee':
                pass
        else:
            print(f"--- Geen resultaten gevonden voor '{zoekterm}' ---\n")

    except Exception as e:
        print(f"Error: {e}")

def check_album():
    # Zoek albumnaam in albums.Name
    query = '''
    SELECT A.Title
    FROM albums as A
    WHERE A.Title LIKE ?;
    '''
    while True:
        try:
            zoekterm = str(input("Geef albumnaam: "))

            cur.execute(query, (f"%{zoekterm}%",))
            res = cur.fetchall()

            if len(res) == 1:
                print("1 album gevonden:")
                for albumnaam in res:
                    print(albumnaam[0])
                print("Display tracks in album? (Ja/Nee)")
                keuze = str(input("\nUw keuze: "))  

                if keuze.lower() == 'ja':
                    dispaly_album_content('ja', res)
                    return False
                
                elif keuze.lower() == 'nee':
                    return False
                
                else:
                    print("ERROR")

            elif len(res) > 1:
                print(f"{len(res)} albums gevonden")
                print("Display albums? (Ja/Nee)")
                keuze = str(input("\nUw keuze: "))

                if keuze.lower() == 'ja':
                    for i, album in enumerate(res, start=1):
                        print(f"{i} - {album[0]}")
                elif keuze.lower() == 'nee':
                    pass
                else:
                    print("ongeldige keuze")
                return False
                
            
            else:
                print("--- Geen album gevonden ---")
                return False

        except Exception as e: print(f"ERROR: {e}")
        
def dispaly_album_content(cmd, AlbumName): # cmd format = (Ja/Nee) [(AlbumName,)]
    
    AlbumString = ''

    for tup in AlbumName:
        for string in tup:
            AlbumString += string + " "

    AlbumString = AlbumString.strip()  # Remove trailing space
    print(f"Album titel: '{AlbumString}'") 

    try:
        if cmd.lower() == 'ja':
            cur.execute('''
                        SELECT
                            T.Name
                        FROM
                            tracks AS T,
                            albums AS AB
                        WHERE
                            T.AlbumId = AB.AlbumId
                        AND AB.Title = ?;
                        ''', (AlbumString,))
            res = cur.fetchall()
            for i, track in enumerate(res, start=1):
                print(f"{i} - {track[0]}")
    except Exception as e: print(f"ERROR: {e}")      

def __main__():
    while True:
        print("\n--- Main menu ---")
        print("1. Check of track in database zit")
        print("2. Check of playlist bestaat")
        print("3. Check of album in database zit")
        print("4. Exit\n")
        
        try:
            cmd = int(input("Uw keuze: "))

            if cmd == 1:
                check_track()
            elif cmd == 2:
                check_playlist()
            elif cmd == 3:
                check_album()
            elif cmd == 4:
                print("- Programma sluiten -\n")
                break
            else:
                print("!!! Ongeldige input !!!\n")

        except ValueError: print("ERROR: keuze moet een getal zijn\n")
        except Exception as e: print(f"ERROR: {e}")

if __name__ == '__main__':
    __main__()
    


