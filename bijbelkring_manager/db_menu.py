import sqlite3 as SQL

def connect_db():
    path = '/Users/gui/Desktop/RTDE/Jezus/bible_verses.db'

    db = SQL.connect(path)
    cur = db.cursor()

    return db, cur


def get_quote():
    db, cur = connect_db()

    query = '''
    SELECT book, chapter, verse, text
    FROM verses
    ORDER BY RANDOM()
    LIMIT 1;
    '''

    cur.execute(query)
    res = cur.fetchone()
    book, chapter, verse, text = res
    
    print(f"{book} {chapter}:{verse} - {text}")

    cur.close()
    db.close()

def insert_quote():
    db, cur = connect_db()

    book = str(input('Give book: '))
    chapter = str(input('Give chapter: '))
    verse = str(input('Give verse: '))
    text = str(input('Give text: '))

    query = '''
    INSERT INTO Verses (book, chapter, verse, text)
    VALUES (?, ?, ?, ?)
    '''

    while True:
        try:
            cmd = str(input('Do you want to save? (Yes/No): '))
            if cmd.lower() == 'yes':
                cur.execute(query, (book, chapter, verse, text))
                db.commit()
                break

            elif cmd.lower() == 'no':
                print('Verse NOT saved.')
                break
            else:
                print('ERROR, PLEASE ENTER "YES" OR "NO"')

        except Exception as e:
            print(f'ERROR {e}')
        
    cur.close()
    db.close()




