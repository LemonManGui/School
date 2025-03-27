import sqlite3 as SQL

# Activeer SQL connectie
path_to_file = "/Users/gui/Desktop/School/Eindopdracht/chinook.db" # Vervang met /Path/To/DataBase_File.db
db = SQL.connect(path_to_file)
cur = db.cursor()



def open_file(): # Returnt een lijst met zoektermen
    input_namen = []

    while True:
        bestand = input("Geef naam van het te importeren bestand: ") # Geef path_to_file 
        
        if not bestand.lower().endswith('.txt'):
            print("\n--- Ongeldig bestandstype. Dit programma accepteerd alleen bestanden met een .txt-extensie ---")

        try:
            with open(bestand, 'r') as b:
                for line in b:
                    stripped_line = line.strip()
                    if stripped_line:
                        input_namen.append(stripped_line.lower())
                
            break
        
        except FileNotFoundError:
            print(f"\n--- Bestand '{bestand}' niet gevonden ---\n")
        except Exception as e:
            print(f"\n--- Onverwachte fout: {e} ---\n")

    return input_namen



def choose_playlist(): # Returnt de playlistnaam
    bestaande_playlists = []

    query = '''
    SELECT Name FROM Playlists
    '''
    cur.execute(query)
    res = cur.fetchall()

    for item in res:
        naam = item[0]
        bestaande_playlists.append(naam)
    
    while True:
        playlist = input("Geef naam van de playlist: ")

        if playlist in bestaande_playlists:
            print("\n--- Deze playlist bestaat al ---\n")
        else:
            print("\n--- Start import van playlist ---\n")
            return playlist



def choose_tracks(input_namen): # Returnt een lijst met gekozen tracks
    gekozen_tracks = []

    query = '''
    SELECT 
        T.Name,
        A.Name
    FROM 
        tracks AS T,
        artists AS A,
        albums AS AB
    WHERE
        T.AlbumId = AB.AlbumId
        AND AB.ArtistId = A.ArtistId
        AND T.Name LIKE ?;
    '''

    for line in input_namen:
        cur.execute(query, (f"%{line}%",))
        res = cur.fetchall()

        if len(res) > 1:
            print(f"\n--- Meerdere keuzes gevonden voor zoekterm: '{line}' ---")
            print("--- Maak een keuze uit de volgende tracks ---\n")
            for i, nummer in enumerate(res, start=1):
                track, artiest = nummer
                print(f"{i}\t{track} - {artiest}")

            while True:      
                try:
                    keuze = int(input("\nUw keuze: "))
                    if keuze >= 1 and keuze <= len(res):
                        gekozen_tracks.append(res[keuze - 1])
                        break
                    else: 
                        raise IndexError

                except IndexError: print(f"--- ERROR: Keuze moet een getal zijn van 1 tot {len(res)} ---")
                except ValueError: print("--- ERROR: Keuze moet een getal zijn ---")
                except Exception as e: print(f"--- ERROR: {e} ---")

        elif len(res) == 1:
            print(f"\n--- 1 track gevonden voor zoekterm: '{line}' ---")
            # Exctract string in tuple in lijst
            for nummer in res:
                track, artiest = nummer
                print(f"-> {track} - {artiest}")
            
            gekozen_tracks.append(res[0])

        else:
            print(f"\n--- Geen tracks gevonden voor zoekterm: '{line}' ---")

    print("\nGevonden tracks:")
    for i, track in enumerate(gekozen_tracks, start=1):
        tracknaam, artiestnaam = track
        print(f"{i}\t{tracknaam}\t{artiestnaam}")
    
    return gekozen_tracks



def save_playlist(gekozen_tracks, playlist_naam): # Bied de keuze om playlist op te slaan
    
    print(f"\nSla gevonden tracks op als playlist: '{playlist_naam}'? (Ja/Nee)")

    while True:
        try:
            cmd = input("\nUw keuze: ")

            if cmd.lower() == "ja":
                # Neemt laatste ID en berekend nieuw ID
                cur.execute('''SELECT MAX(playlistId) FROM playlists''')
                last_pl_id = cur.fetchone()[0]
                new_pl_id = (last_pl_id + 1)
                
                # Insert nieuwe playlist
                cur.execute('''
                INSERT INTO playlists
                    (PlaylistId, Name)
                VALUES 
                    (?, ?);
                ''', (new_pl_id, playlist_naam)
                )
                db.commit()
                

                for track in gekozen_tracks:
                    cur.execute('''
                                SELECT TrackId FROM tracks WHERE Name = ?;
                                ''', (track[0],))
                    res = cur.fetchone()

                    if res is not None:
                        track_id = res[0]
                        # Insert TrackID en nieuwe PlaylistID
                        cur.execute('''
                        INSERT INTO
                            playlist_track
                            (PlaylistId, TrackId)
                        VALUES
                            (?, ?)
                        ''', (new_pl_id, track_id))
                    else:
                        print(f"ERROR: Track '{track[0]}' not found in database")
                        
                db.commit()

                print(f"--- Playlist '{playlist_naam}' is opgeslagen in de database ---")
                print("--- Programma sluiten ---")
                return False

            elif cmd.lower() == "nee":
                print("--- De playlist is NIET opgeslagen ---")
                print("--- Programma sluiten ---")
                return False
            
            else:
                print("--- ERROR: Ongeldige keuze. Typ 'Ja' of 'Nee' ---")
            
        except ValueError:
            print("ERROR: Ongeldige input")
        except Exception as e:
            print(f"ERROR: {e}")


def close_connection():
    cur.close()
    db.close()

def __main__():

    namen = open_file() # Returnt een lijst met zoektermen

    playlist = choose_playlist() # Returnt de nieuwe playlistnaam

    keuze = choose_tracks(namen) # Returnt een lijst met gekozen nummers

    save_playlist(keuze, playlist) # Slaat playlist op in database

    close_connection() # Sluit de connectie met DataBase



if __name__ == "__main__":
    __main__()