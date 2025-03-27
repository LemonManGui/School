# Step 1
# Create a database with bible verses
# Fields: book, chapter, verse, text

import sqlite3 as SQL

PATH ='/Users/gui/Desktop/RTDE/Jezus/bible_verses.db'
db = SQL.connect(PATH)
cur = db.cursor()

# cur.execute('''
# CREATE TABLE IF NOT EXISTS Verses (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             book TEXT,
#             chapter TEXT,
#             verse TEXT,
#             text TEXT
#             )
# ''')

# db.commit()
# db.close()

###
# Step 2
# fill database with verses
# use bible-api

import requests
import time


# motivational_verses = [
#     "Joshua 1:9",
#     "Isaiah 41:10",
#     "Philippians 4:13",
#     "Romans 8:28",
#     "Jeremiah 29:11",
#     "Matthew 11:28",
#     "Psalm 23:1",
#     "Psalm 34:17",
#     "Psalm 46:1",
#     "Isaiah 40:31",
#     "Deuteronomy 31:6",
#     "John 16:33",
#     "2 Timothy 1:7",
#     "1 Peter 5:7",
#     "Proverbs 3:5",
#     "Romans 15:13",
#     "Hebrews 11:1",
#     "Matthew 6:33",
#     "John 14:27",
#     "Colossians 3:23",
#     "Psalm 37:4",
#     "Psalm 55:22",
#     "1 Corinthians 16:13",
#     "Isaiah 26:3",
#     "James 1:12",
#     "Romans 12:12",
#     "Psalm 118:24",
#     "Matthew 19:26",
#     "2 Corinthians 12:9",
#     "John 8:12",
#     "Psalm 119:105",
#     "Luke 1:37",
#     "Romans 5:3",
#     "Psalm 91:2",
#     "Isaiah 43:2",
#     "Ephesians 6:10",
#     "Psalm 27:1",
#     "Proverbs 18:10",
#     "1 John 4:4",
#     "2 Corinthians 4:16",
#     "Psalm 121:1",
#     "Jeremiah 17:7",
#     "Psalm 62:6",
#     "Isaiah 12:2",
#     "1 Thessalonians 5:16",
#     "Philippians 1:6",
#     "Psalm 31:24",
#     "Hebrews 13:5",
#     "Psalm 138:3",
#     "Nehemiah 8:10",
#     "Mark 10:27",
#     "Romans 14:8",
#     "Exodus 14:14",
#     "Psalm 56:3",
#     "John 10:10",
#     "Isaiah 54:17",
#     "Hebrews 12:1",
#     "Micah 7:7",
#     "Matthew 5:16",
#     "Romans 8:31",
#     "Psalm 16:8",
#     "Psalm 27:14",
#     "1 Corinthians 10:13",
#     "Matthew 28:20",
#     "Psalm 63:7",
#     "Romans 8:38",
#     "Zephaniah 3:17",
#     "Psalm 32:8",
#     "1 Peter 2:9",
#     "Isaiah 30:21",
#     "2 Timothy 4:7",
#     "Psalm 20:4",
#     "Galatians 6:9",
#     "Lamentations 3:22",
#     "Ephesians 3:20",
#     "Proverbs 16:3",
#     "Psalm 112:7",
#     "John 6:35",
#     "Psalm 37:5",
#     "Isaiah 33:2",
#     "Psalm 145:18",
#     "Romans 10:9",
#     "Isaiah 58:11",
#     "Psalm 23:4",
#     "James 4:7",
#     "Luke 18:27",
#     "Psalm 94:19",
#     "Isaiah 9:6",
#     "Psalm 34:8",
#     "2 Thessalonians 3:3",
#     "Romans 12:21",
#     "Matthew 7:7",
#     "Psalm 40:1",
#     "Titus 3:5",
#     "Psalm 103:2",
#     "John 15:7",
#     "Colossians 1:11",
#     "Romans 15:4",
#     "1 Samuel 16:7",
#     "Psalm 139:14",
#     "Philippians 4:19",
#     "Psalm 28:7",
#     "Isaiah 50:7"
# ]

# for verse in motivational_verses:

#     response = requests.get(f"https://bible-api.com/{verse}")
#     data = response.json()

#     reference = data["reference"]
#     parts = reference.rsplit(" ", 1)
#     book = parts[0]
#     chapter, verse_number = map(int, parts[1].split(":"))
#     text = data["text"]

#     insert_verse_query = '''
#         INSERT INTO Verses (book, chapter, verse, text)
#         VALUES (?, ?, ?, ?)
#     '''
#     cur.execute(insert_verse_query, (book, chapter, verse_number, text))
#     time.sleep(2)
#     print(f"Imported verse: {book}, {chapter}:{verse_number}")

# db.commit()
# db.close()

###

# Step 3
# Random output generator

def get_verse():
    cur.execute('''
                SELECT book, chapter, verse, text FROM Verses ORDER BY RANDOM() LIMIT 1
                ''')
    res = cur.fetchone()
    book, chapter, verse, text = res
    print(f"{book} {chapter}:{verse} - {text}")
    db.close()

# Step 4
# Text to speech

def verse_to_speech(verse_text): # Not working
    from elevenlabs import stream
    from elevenlabs.client import ElevenLabs
    import elevenlabs

    client = ElevenLabs(
    api_key = "sk_b2d71e9223864bfaad693ad8fc2f7bf70c17d39e54b160e9",
    )
    
    audio_stream = client.text_to_speech.convert_as_stream(
        text=verse_text,
        voice_id='flq6f7yk4E4fJM5XTYuZ',
        model_id='eleven_multilingual_v2'
    )
    
    audio_file = f"/Users/gui/Desktop/RTDE/Jezus/verse_audio/verse.mp3"
    elevenlabs.save(audio_stream, audio_file)

    print("Audio has been created...")

    return audio_file


# Step 5
# Create the video database

import os
def save_videos():
    PEXELS_API_KEY = 'rMS28W02ZqIUGv4WXFMwQZIG3iAn1VQBRY7uOSxyP01BEKWdZzyskTNE'

    video_folder = "/Users/gui/Desktop/RTDE/Jezus/background_videos"
    os.makedirs(video_folder, exist_ok=True)

    # 🔹 Keywords for Christian-themed videos
    search_terms = ['Christian', 'Jezus', 'faith', 'Bible', 'cross', 'church']

    downloaded_count = 0
    video_limit = 50  # Max videos to download

    # 🔹 Fetch and download videos
    for term in search_terms:
        if downloaded_count >= video_limit:
            break  # Stop once we hit the limit

        url = f"https://api.pexels.com/videos/search?query={term}&per_page=20"
        headers = {'Authorization': PEXELS_API_KEY}  # 🔹 Fixed typo here
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            videos = response.json().get('videos', [])
            for video in videos:
                if downloaded_count >= video_limit:
                    break

                # Get video details
                video_url = video['video_files'][0]['link']
                video_id = video['id']
                file_path = os.path.join(video_folder, f'video_{video_id}.mp4')

                # Download video
                video_data = requests.get(video_url)
                with open(file_path, 'wb') as f:
                    f.write(video_data.content)

                # Save metadata to MySQL
                cur.execute("INSERT INTO background_videos (file_name, file_path) VALUES (?, ?)", (f"video_{video_id}.mp4", file_path))
                db.commit()


                downloaded_count += 1
                print(f"✅ Downloaded: {file_path}")

    # 🔹 Close database connection
    cur.close()
    db.close()
    print("🎥 All videos downloaded and stored in the database!")





# Step 6
# Create a function to combine videos with text

from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from moviepy import *

# Final funcion !!!

def create_video(amount=1):
        
    for num in range(amount):
        # DB interaction
        PATH ='/Users/gui/Desktop/RTDE/Jezus/bible_verses.db'
        db = SQL.connect(PATH)
        cur = db.cursor()

        cur.execute('''
            SELECT file_path FROM Background_videos ORDER BY RANDOM() LIMIT 1;
        ''')
        video_path = cur.fetchone()[0]

        cur.execute('''
            SELECT book, chapter, verse, text FROM Verses ORDER BY RANDOM() LIMIT 1;
        ''')

        book, chapter, verse, verse_text = cur.fetchone()
        full_text = f'{verse_text}\n{book} {chapter}:{verse}'

        cur.close()
        db.close()


        #audio_path = verse_to_speech(full_text)

        clip = VideoFileClip(video_path)
        #audio_clip = AudioFileClip(audio_path)

        clip = clip.resized(height=1920)
        clip = clip.cropped(width=1080, height=1920, x_center=clip.w / 2, y_center=clip.h / 2)

        text_box_width = int(clip.w * 0.75)
        text_box_height = int(clip.h * 0.3)

        txt_clip = TextClip(
            font='Georgia', 
            text=full_text, 
            font_size=65, 
            color='white', 
            method='caption', 
            size=(text_box_width, text_box_height)
            )
        
        txt_clip = txt_clip.with_position(('center', int(1920 * 0.60))).with_duration(clip.duration)

        final_clip = CompositeVideoClip([clip, txt_clip])
        #final_clip_audio = final_clip.with_audio(audio_clip)
        
        output_video = f'/Users/gui/Desktop/RTDE/Jezus/one_week/final_video_{num}.mp4'

        final_clip.write_videofile(output_video, codec='libx264', fps=30) #  audio_codec="aac"

        print(f"🎥 Video created: {output_video}")


create_video()


def create_video_menu():

    print("Clip will consists of a video, a audio and a text")

    video_path = str(input("Enter path to video: "))
    audio_path = str(input("Enter path to audio: "))
    text_ = str(input("Enter text: "))
    tag = str(input("Enter video tag: "))
    
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    clip = video.resized(height=1920)
    clip = clip.cropped(width=1080, height=1920, x_center=clip.w / 2, y_center=clip.h / 2)

    text_box_width = int(clip.w * 0.75)
    text_box_height = int(clip.h * 0.3)

    txt_clip = TextClip(
        font='Georgia', 
        text=text_, 
        font_size=65, 
        color='white', 
        method='caption', 
        size=(text_box_width, text_box_height)
        )
    
    txt_clip = txt_clip.with_position(('center', int(1920 * 0.60))).with_duration(clip.duration)

    final_clip = CompositeVideoClip([clip, txt_clip])
    final_with_audio = final_clip.with_audio(audio)

    store_location = f'/Users/gui/Desktop/RTDE/Jezus/one_week/final_video_{tag}.mp4'

    final_with_audio.write_videofile(store_location, codec='libx264', fps=30, audio_codec="aac")

    print(f'Video saved to: {store_location}')


