import base64
import os
import sqlite3
from pathlib import Path as Pathlib_path

static_images = os.path.dirname(os.path.abspath(__file__)) + "/static/images/styles/small/"
save_parent_folder = "/storage/emulated/0/Music/EisenRadio"
script_path = os.path.dirname(__file__)


def convert_ascii(file_name):
    with open(file_name, "rb") as reader:
        img_bytes = reader.read()
        img_ascii = render_picture(img_bytes, 'encode')
    return img_ascii


def render_picture(byte_data, de_enc):
    render_pic = ''
    if de_enc == 'encode':
        render_pic = base64.b64encode(byte_data).decode('ascii')
    if de_enc == 'decode':
        render_pic = base64.b64decode(byte_data).decode('ascii')
    return render_pic


def make_db_from_schema():
    # # # # custom filled db # # #
    connection = ''
    is_snap_device = 'SNAP' in os.environ
    is_android_device = 'ANDROID_STORAGE' in os.environ

    if not is_snap_device:
        connection = sqlite3.connect((os.path.join(script_path, 'database.db')))
    if is_android_device:
        return
    if is_snap_device:
        # not overwrite db from old version, where an existing 'database.db' was copied
        snap_db = Pathlib_path(os.path.join(os.environ["SNAP_USER_COMMON"], 'pre_configured.db'))
        if snap_db.is_file():
            return
        if not snap_db.is_file():
            connection = sqlite3.connect(str(snap_db))

    with open((os.path.join(script_path, 'schema.sql'))) as f:
        connection.executescript(f.read())

    cur = connection.cursor()
    cur.execute("INSERT INTO eisen_intern (browser_open,statistics,commercials) VALUES (?,?,?)", (str(1), 1, 1))

    cur.execute(
        "INSERT INTO posts (title, content, download_path, pic_comment, pic_content_type, pic_data) VALUES (?, ?, ?, "
        "?, ?, ?)",
        ('classic',
         'http://37.251.146.169:8000/streamHD',
         save_parent_folder,
         '',
         "image/png",
         convert_ascii(static_images + "radio3d-style-white-brown_120x200.png"))
        )
    cur.execute(
        "INSERT INTO posts (title, content, download_path, pic_comment, pic_content_type, pic_data) VALUES (?, ?, ?, "
        "?, ?, ?)",
        ('goa_psi',
         'http://amoris.sknt.ru:8004/stream',
         save_parent_folder,
         '',
         "image/png",
         convert_ascii(static_images + "radio3d-style-white-black_120x200.png"))
        )
    cur.execute(
        "INSERT INTO posts (title, content, download_path, pic_comment, pic_content_type, pic_data) VALUES (?, ?, ?, "
        "?, ?, ?)",
        ('time_machine',
         'http://98.211.68.9:8765/listen',
         save_parent_folder,
         'usa - Classic Old Time Radio, Sci Fi, Comedy, Drama',
         "image/png",
         convert_ascii(static_images + "radio3d-style-white-blue_120x200.png"))
        )
    cur.execute(
        "INSERT INTO posts (title, content, download_path, pic_comment, pic_content_type, pic_data) VALUES (?, ?, ?, "
        "?, ?, ?)",
        ('nerd-sound-tracks',
         'http://167.114.210.232:8259/stream',
         save_parent_folder,
         'sound tracks of japanese anime videos and games',
         "image/jpeg",
         convert_ascii(static_images + "mixer-tempelhof-airport.jpg"))
        )
    cur.execute(
        "INSERT INTO posts (title, content, download_path, pic_comment, pic_content_type, pic_data) VALUES (?, ?, ?, "
        "?, ?, ?)",
        ('BLUES_UK',
         'http://149.255.59.3:8232/stream',
         save_parent_folder,
         '',
         "image/jpeg",
         convert_ascii(static_images + "mixer-reload.jpg"))
        )
    cur.execute(
        "INSERT INTO posts (title, content, download_path, pic_comment, pic_content_type, pic_data) VALUES (?, ?, ?, "
        "?, ?, ?)",
        ('relax',
         'https://listen.openstream.co/6781/audio',
         save_parent_folder,
         '',
         "image/jpeg",
         convert_ascii(static_images + "mixer-construction-site.jpg"))
        )
    cur.execute(
        "INSERT INTO posts (title, content, download_path, pic_comment, pic_content_type, pic_data) VALUES (?, ?, ?, "
        "?, ?, ?)",
        ('Nachtflug',
         'http://85.195.88.149:11810/sid=1',
         save_parent_folder,
         '',
         "image/png",
         convert_ascii(static_images + "radio3d-style-white-red_120x200.png"))
        )
    cur.execute(
        "INSERT INTO posts (title, content, download_path, pic_comment, pic_content_type, pic_data) VALUES (?, ?, ?, "
        "?, ?, ?)",
        ('hm',
         'https://hirschmilch.de:7001/prog-house.mp3',
         save_parent_folder,
         '',
         "image/png",
         convert_ascii(static_images + "radio3d-style-whiteneongelb_120x200.png"))
        )
    cur.execute(
        "INSERT INTO posts (title, content, download_path, pic_comment, pic_content_type, pic_data) VALUES (?, ?, ?, "
        "?, ?, ?)",
        ('zen',
         'https://radio4.cdm-radio.com:18004/stream-mp3-Zen',
         save_parent_folder,
         '',
         "image/png",
         convert_ascii(static_images + "radio3d-style-white-white_120x200.png"))
        )
    cur.execute(
        "INSERT INTO posts (title, content, download_path, pic_comment, pic_content_type, pic_data) VALUES (?, ?, ?, "
        "?, ?, ?)",
        ('B2',
         'https://radiob2-national.cast.addradio.de/radiob2/national/mp3/high/stream.mp3',
         save_parent_folder,
         'german (deutsch) only',
         "image/png",
         convert_ascii(static_images + "radio3d-style-white-violet_120x200.png"))
        )
    cur.execute(
        "INSERT INTO posts (title, content, download_path, pic_comment, pic_content_type, pic_data) VALUES (?, ?, ?, "
        "?, ?, ?)",
        ('Reggae',
         'http://hd.lagrosseradio.info:8000/lagrosseradio-reggae-192.mp3',
         save_parent_folder,
         '',
         "image/png",
         convert_ascii(static_images + "radio3d-style-white-neongreen_120x200.png"))
        )
    connection.commit()
    connection.close()


def empty_db_from_schema():
    # # # # custom filled db # # #
    connection = ''
    is_snap_device = 'SNAP' in os.environ
    is_android_device = 'ANDROID_STORAGE' in os.environ

    if is_android_device:
        return
    if not is_snap_device:
        connection = sqlite3.connect((str(os.path.join(script_path, 'database.db'))))
    if is_snap_device:
        connection = sqlite3.connect((str(os.path.join(os.environ["SNAP_USER_COMMON"], 'pre_configured.db'))))

    with open((os.path.join(script_path, 'schema.sql'))) as f:
        connection.executescript(f.read())

    cur = connection.cursor()
    cur.execute("INSERT INTO eisen_intern (browser_open,statistics,commercials) VALUES (?,?,?)", (str(1), 1, 1))
    connection.commit()
    connection.close()
