import configparser
import json
import shutil
import random

import eisenradio.lib.eisdb as eisen_db
import eisenradio.eisenutil.monitor_records as mo_rec

from os import path, remove, listdir
from flask import flash
from eisenradio.eisenutil.eisutil import is_in_db_view


def delete_all_radios():
    no_error = True
    posts = get_radios()

    for radio in posts:
        rv = eisen_db.delete_radio(radio['id'])
        if not rv:
            no_error = False
    # vakuum db
    eisen_db.get_db_smaller()
    if no_error:
        flash('Delete all radios. Done.', 'success')
    else:
        flash('not all radios where deleted', 'warning')
    return no_error


def export_radios():
    # BLUES_UK = http://149.255.59.3:8232/stream
    posts = get_radios()
    if not posts:
        return False

    radio_url_dict, export_path = export_radios_dump(posts)
    if not path.exists(export_path):
        return False

    dump_file_path = path.join(export_path, 'eisenradio_settings.ini')
    dump_file_path_backup = path.join(export_path, 'eisenradio_settings.ini_backup')
    dump_radio_export_backup(dump_file_path_backup, dump_file_path)

    print(dump_file_path)
    with open(dump_file_path, 'w') as writer:
        writer.write('[GLOBAL]' + '\n')
        writer.write('SAVE_TO_DIR = ' + export_path + '\n')
        writer.write('[STATIONS]' + '\n')
        for radio, url in radio_url_dict.items():
            writer.write(radio + ' = ' + url + '\n')
        writer.flush()

    return True


def export_radios_dump(posts):
    radio_url_dict = {}
    download_path = ''
    for station in posts:
        station_name = eisen_db.status_read_status_set(False, 'posts', 'title', station['id'])
        station_url = eisen_db.status_read_status_set(False, 'posts', 'content', station['id'])
        download_path = eisen_db.status_read_status_set(False, 'posts', 'download_path', station['id'])
        radio_url_dict[station_name] = station_url
    return radio_url_dict, download_path


def upload_radios(str_ini):
    """
    Master def of uploading radios and urls
    """
    config = configparser.ConfigParser()
    config.optionxform = str    # not squeeze the names lower case
    download_path = upload_radios_read_global(config, str_ini)
    name_url_dict = upload_radios_read_stations(config, str_ini)
    if not name_url_dict:
        return False
    upload_radios_db_import_ini(name_url_dict, download_path)
    return True


def upload_radios_read_global(config, str_ini):
    try:
        config.read_string(str_ini)
        global_dict = config['GLOBAL']
    except Exception as error:
        print(f'minor error in upload_radios() no [GLOBAL]: {error} - will proceed')
        return
    try:
        download_path = global_dict['SAVE_TO_DIR']
    except Exception as error:
        print(f'minor error in upload_radios() no [SAVE_TO_DIR]: {error} - will proceed')
        # return None, False is bool leads to error later in if
        return
    return download_path


def upload_radios_read_stations(config, str_ini):
    try:
        config.read_string(str_ini)
        station_dict = config['STATIONS']
    except Exception as error:
        print(f' error in upload_radios(), no mandatory [STATIONS]: {error} give up.')
        # return None, False is bool leads to error in if
        return
    return station_dict


def upload_radios_db_import_ini(station_dict, download_ini_path=None):
    """
    imports only new radios with url from ini file into db, [STATION] section, download_path is in [GLOBAL]
    two scenarios, restore all after complete deletion, append new radios
    download path is preferred from db, then ini, then put a message as path
    """
    conn = eisen_db.get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    download_db_path = upload_radios_db_get_download_path(posts)

    if download_db_path is not None:
        download_path = download_db_path
    elif download_ini_path is not None:
        download_path = download_ini_path
    else:
        download_path = '/Please/use/Save/from/menu'

    for radio, url in station_dict.items():
        if is_in_db_view(radio):
            continue
        radio_image, image_content_type = radio_spare_image()  # pull a random image for the new radios
        conn.execute('INSERT INTO posts (title, content, download_path, pic_data, pic_content_type) VALUES ('
                     '?, ?, ?, ?, ?)', (radio, url, download_path, radio_image, image_content_type))
        conn.commit()

    conn.close()


def upload_radios_db_get_download_path(posts):
    try:
        download_path = posts[0]["download_path"]
    except Exception as error:
        message = f'no path in db, {error}, proceed.'
        print(message)
        return
    return download_path


def get_radios():
    conn = eisen_db.get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return posts


def radio_spare_image():
    """
    get a random image from static folder
    """
    this_dir = path.dirname(__file__)
    # rip off one dir
    app_root = path.dirname(this_dir)
    image_list = listdir(path.join(app_root, 'static', 'images', 'styles', 'small'))
    img_path = path.join(app_root, 'static', 'images', 'styles', 'small', random.choice(image_list))
    with open(img_path, 'rb') as pic_reader:
        image_bin = pic_reader.read()
    img_base64 = eisen_db.render_picture(image_bin, 'encode')
    content_type = 'image/png'
    return img_base64, content_type


def get_export_path():
    download_path = eisen_db.get_download_dir()
    if not download_path:
        export_path = "use Save from Navigation Menu"
    else:
        export_path = download_path
    return export_path


def dump_radio_blacklist():
    """
    create a dump_dict[radio] = blacklist dictionary for all radios with a list to export it to a file
    parent folder for radios is used as place to store the file (json dict)
    first dict entry is a message
    import only if Key (RadioName) is matching, upper, lower case
    """
    dump_dict = {}
    conn = eisen_db.get_db_connection()
    download_path = conn.execute('SELECT download_path FROM posts;').fetchone()
    export_path = download_path[0]
    radios_list = conn.execute('SELECT title FROM posts').fetchall()

    dump_dict['Eisenradio message'] = json.dumps('This is a json formatted dictionary. Rename radios you do not want.')
    if radios_list:
        for row in radios_list:
            radio_name = row[0]
            file_list = []
            # table column 'display' was used to store current title for displaying, now in api; reuse for list
            known_files = conn.execute('SELECT display FROM posts WHERE title = ?;', (radio_name,)).fetchone()
            if known_files:
                if known_files[0]:
                    try:
                        file_list = json.loads(known_files[0])
                    except Exception as error:
                        print(error)

            if len(file_list) > 0:
                dump_dict[radio_name] = file_list

    conn.close()
    if export_path:
        rv = dump_write_radio_blacklist(dump_dict, export_path)
        return rv
    else:
        return False


def dump_write_radio_blacklist(dump_dict, export_path):
    dump_file_path = path.join(export_path, 'eisenradio_blacklists.json')
    dump_file_path_backup = path.join(export_path, 'eisenradio_blacklists.json_backup')
    dump_radio_export_backup(dump_file_path_backup, dump_file_path)
    try:
        with open(dump_file_path, 'w') as writer:
            writer.write(json.dumps(dump_dict, indent=4))    # no indent, one long line

        rv = True
    except OSError:
        rv = False
    return rv


def dump_radio_export_backup(dump_file_path_backup, dump_file_path):
    """
    make a copy from last backup before overwrite file
    """
    if path.exists(dump_file_path_backup):
        remove(dump_file_path_backup)
    if path.exists(dump_file_path):
        shutil.copyfile(dump_file_path, dump_file_path_backup)


def upload_blacklists(json_file):
    """
    called from routes.tools_upload_trace_lists(), delivers the json_file raw, must be loaded
    dump_dict[radio] is the import list for the radio
    returns False on error to display a warning on html
    """
    upload_ok = True
    dump_dict = upload_blacklists_dump(json_file)
    if not len(dump_dict) > 0:
        return False

    radios_list = upload_blacklists_get_radio_names_from_db()
    if radios_list:
        imported_all_ok = upload_blacklists_import(dump_dict, radios_list)
        if not imported_all_ok:
            upload_ok = False
        mo_rec.feed_api_radios_blacklists()
    else:
        print('\n\tImport error. No radios in db.\n')
        upload_ok = False

    if upload_ok:
        print('\n\tBlacklists updated and loaded.\n')
    else:
        print('\n\tSome error occurred. See terminal messages.\n')
    return upload_ok


def upload_blacklists_import(dump_dict, radios_list):
    import_no_err = True
    for row in radios_list:
        radio = row[0]
        if radio in dump_dict.keys():
            print(f'import list for: {radio}')
            print(dump_dict[radio])
            merged_blacklist, rv = upload_blacklists_merge(dump_dict[radio], radio)
            if rv:
                rv = upload_blacklists_write(merged_blacklist, radio)
            if not rv:
                import_no_err = False
    return import_no_err


def upload_blacklists_get_radio_names_from_db():
    conn = eisen_db.get_db_connection()
    radios_list = conn.execute('SELECT title FROM posts').fetchall()
    conn.close()
    return radios_list


def upload_blacklists_dump(json_file):
    dump_dict = {}
    try:
        dump_dict = json.loads(json_file)
    except Exception as error:
        message = f'unknown error in upload_blacklists_dump() {error}. Give up.'
        print(message)
    return dump_dict


def upload_blacklists_merge(import_list, radio):
    """
    concatenate lists, make a set of 'em to remove double values, convert set back to list
    """
    rv = True
    blacklist = mo_rec.dump_radio_blacklist_from_col(radio)
    merged_blacklist = []
    try:
        ext_list = []
        ext_list.extend(blacklist)
        ext_list.extend(import_list)
        merged_blacklist = list(set(ext_list))
    except Exception as error:
        message = f'unknown error in upload_blacklists_merge() {error}, try to proceed'
        print(message)
        rv = False
    return merged_blacklist, rv


def upload_blacklists_write(merged_blacklist, radio):
    rv = True
    try:
        conn = eisen_db.get_db_connection()
        conn.execute('UPDATE posts SET display = ? WHERE title = ?;', (json.dumps(merged_blacklist), radio))
        conn.commit()
        conn.close()
    except Exception as error:
        message = f'unknown error in upload_blacklists_write() {error}, try to proceed'
        print(message)
        rv = False
    return rv
