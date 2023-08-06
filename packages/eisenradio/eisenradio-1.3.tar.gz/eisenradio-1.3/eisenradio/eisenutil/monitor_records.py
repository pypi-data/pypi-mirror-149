"""
    module description:
    - normal behavior: recorder copy new file (deletes existing file)
    - monitored: recorder writes title to dict, copy new file only if title is not found in blacklist
    - blacklist_writer thread collects new titles from recorder dicts and updates radio blacklists
    - route endpoints added to utils route i.a. to create an DB entry and set, check status from java
    - ajax enable monitoring, 'insert' (add row in internal table)
    - ghettoApi got a variable to break the run_blacklist_writer() loop, if timer is set
    - Tools menu got Export/Import options
    - Tools Export/Import menus are displayed or hidden Html Div elements (bp_utils.js)
"""
import copy
import json
import threading
import time

import eisenradio.lib.eisdb as eisen_db
from eisenradio.api import ghettoApi

all_blacklists_dict = {}
ghettoApi.init_ghetto_all_blacklists_dict(all_blacklists_dict)

is_new_in_title_compare_dict = {}


def start_blacklist_writer_daemon():
    threading.Thread(name="blacklist_writer", target=run_blacklist_writer, daemon=True).start()


def run_blacklist_writer():
    first_run = True
    while not ghettoApi.stop_blacklist_writer:
        if first_run:
            enabled = status_db_blacklist_get()
            status_api_blacklist_set(enabled)
            feed_api_radios_blacklists()
            first_run = False

        if ghettoApi.blacklist_enabled_global:
            update_radios_blacklists()

        for _ in range(5):
            if ghettoApi.stop_blacklist_writer:
                break
            time.sleep(1)


def status_db_blacklist_get():
    """
    called by
    @eisenutil_bp.route('/tools'
    @eisenutil_bp.route('/tools_radio_blacklist_set'
    """
    conn = eisen_db.get_db_connection()
    status = conn.execute('SELECT browser_open FROM eisen_intern WHERE id = 2').fetchone()
    conn.close()
    if status:
        return status
    return


def status_api_blacklist_set(status):
    """
    set status
    """
    if not status:
        # not enabled at all, no insert added a new row 2
        ghettoApi.blacklist_enabled_global = False
    if status:
        if int(status[0]) == 0:
            ghettoApi.blacklist_enabled_global = False
        if int(status[0]) == 1:
            ghettoApi.blacklist_enabled_global = True


def blacklist_enabled_button_outfit_get(is_enabled):
    """
    read status
    called by @eisenutil_bp.route('/tools'
    """
    enabled = False
    if not is_enabled:
        enabled = False
    if is_enabled:
        if int(is_enabled[0]) == 0:
            enabled = False
        if int(is_enabled[0]) == 1:
            enabled = True
    return enabled


def update_radios_blacklists():
    """
    get filename (title) from recorder, write it to the radios list in database and in global dict, if filename is new
    recorder to dict : recorder_new_title_dict['radio5'] = 'ASAP - I want to be part of the blacklist'
    recorder compares:    all_blacklists_dict['radio5'] = ['The Listies - I am on a list', 'OMG - Mee Too']
    recorder (not found) writes: 'ASAP - I want to be part of the blacklist.aacp'
    blacklist_writer: all_blacklists_dict['radio5'].append(recorder_new_title_dict['radio5'])

    recorder_new_title_dict has max. one string (value) for each recorder (key) at a time - the title
    the all_blacklists_dict hosts the blacklist [list] of the radio in the value field

    check if title is the same as in last function call to not permanently open the db, is_new_in_title_compare_dict
    """
    global is_new_in_title_compare_dict
    # make a copy of dict to prevent 'RuntimeError: dictionary changed size during iteration'
    recorder_new_title_dict_cp = copy.deepcopy(ghettoApi.recorder_new_title_dict)

    conn = eisen_db.get_db_connection()

    for radio, new_title in recorder_new_title_dict_cp.items():
        if radio in is_new_in_title_compare_dict.keys():
            # check for new title in radio; copy of recorder_new_title_dict['radio5'] = 'ASAP - I want to ...'
            if recorder_new_title_dict_cp[radio] == is_new_in_title_compare_dict[radio]:
                continue    # no db access

        known_files = conn.execute('SELECT display FROM posts WHERE title = ?;', (radio,)).fetchone()
        blacklist = json_loads_blacklist(known_files, radio)
        if new_title not in blacklist:
            ghettoApi.all_blacklists_dict[radio].append(new_title)
            blacklist.append(new_title)
            conn.execute('UPDATE posts SET display = ? WHERE title = ?;', (json.dumps(blacklist), radio))
            conn.commit()

        is_new_in_title_compare_dict[radio] = new_title

    conn.close()


def feed_api_radios_blacklists():
    """
    write known records for each radio to api
    recorder can check if record (title) is in the list and skip writing it
    """

    conn = eisen_db.get_db_connection()
    radios_list = conn.execute('SELECT title FROM posts').fetchall()

    if radios_list:
        for row in radios_list:
            radio = row[0]
            # table column 'display' was used to store current title for displaying, now in api; reuse for list
            known_files = conn.execute('SELECT display FROM posts WHERE title = ?;', (radio,)).fetchone()

            blacklist = json_loads_blacklist(known_files, radio)
            ghettoApi.all_blacklists_dict[radio] = blacklist
    conn.close()


def dump_radio_blacklist_from_col(radio):
    conn = eisen_db.get_db_connection()
    known_files = conn.execute('SELECT display FROM posts WHERE title = ?;', (radio,)).fetchone()
    conn.close()

    blacklist = json_loads_blacklist(known_files, radio)
    return blacklist


def json_loads_blacklist(known_files, radio):
    blacklist = []
    if known_files:
        if known_files[0]:
            try:
                blacklist = json.loads(known_files[0])
            except Exception as error:
                message = f'minor error in json_loads_blacklist(), {radio} {error}, can proceed with an empty list'
                print(message)
    return blacklist


def sort_dictionary_by_value(blacklist):
    """
    route endpoint shows it in Html for editing and deletion
    """
    sorted_dict = {}
    if not len(blacklist):
        return sorted_dict

    unsorted_dict = {index: value for index, value in enumerate(blacklist)}
    # Create a list of tuples sorted by value, value[1] is value field in dict/ value[0] mimics "key"
    sorted_tuples = sorted(unsorted_dict.items(), key=lambda value: value[1])
    sorted_dict = {elem[0]: elem[1] for elem in sorted_tuples}
    return sorted_dict


def delete_blacklist(radio):
    """
    delete a radios blacklist from db and all_blacklists_dict, ajax request
    """
    print(f'replace blacklist {radio} with an empty list!! ')
    blacklist = []
    conn = eisen_db.get_db_connection()
    conn.execute('UPDATE posts SET display = ? WHERE title = ?;', (json.dumps(blacklist), radio))
    conn.commit()
    conn.close()
    ghettoApi.all_blacklists_dict[radio] = []


def del_single_title_master(radio, request_dict):
    """
    Master of del_single_title
    del individual items from a radios blacklist, ajax request delivers the title indexes for deletion in request_dict
    avoid comparing values, if article in big_rack ... , your choice article with index 345, drive to shelf 345, can
    compare later if necessary (high-bay warehouse)
    """
    blacklist = dump_radio_blacklist_from_col(radio)
    if not blacklist:
        return

    for item in blacklist:
        print(f' {blacklist.index(item)} {item}')

    print("""\n --> Delete titles from blacklist \n""")
    # 1 sort del indexes in ascending list, 2 del a title and subtract one from original index in each loop
    # sorted values in new ordered list; sort to later remove items via index in a foreseen manner
    unsorted_del_idx = del_single_title_get_del_indexes(request_dict)
    sorted_del_idx = sorted(unsorted_del_idx)

    altered_blacklist = del_single_title_del_indexes(sorted_del_idx, blacklist, radio)
    del_single_title_write(altered_blacklist, radio)


def del_single_title_write(altered_blacklist, radio):
    conn = eisen_db.get_db_connection()
    conn.execute('UPDATE posts SET display = ? WHERE title = ?;', (json.dumps(altered_blacklist), radio))
    conn.commit()


def del_single_title_del_indexes(asc_ord_del_idx, blacklist, radio):
    """
    remove title(s) from all lists by deleting their indexes, no value compare
    list with indexes to delete is ordered ascending [7,23,467] (same as the blacklist[0] to blacklist[999])
    index deletion means -1 index number for all successors of the deleted element vs org. list
    returns altered blacklist
    """
    print(asc_ord_del_idx)
    i = 0
    for idx in asc_ord_del_idx:
        print(f'  {idx}: {blacklist[idx + i]} [{idx + i}: index in altered list]')
        del ghettoApi.all_blacklists_dict[radio][idx + i]
        del blacklist[idx + i]
        i -= 1

    return blacklist


def del_single_title_get_del_indexes(request_dict):
    """
    the request dict transports not only indexes via ajax
    pull del indexes from request
    """
    unsorted_indexes = []

    for key, value in request_dict.items():
        if (not key == 'radio_name') and (not key == 'delAll'):
            unsorted_indexes.append(int(value))
    return unsorted_indexes


def delete_all_blacklists(feature_enabled):
    """
    caller @eisenutil_bp.route('/radio_blacklist_set'
    delete all collected filenames from all radios if feature switch to disabled
    """
    if not feature_enabled:
        conn = eisen_db.get_db_connection()
        radios = conn.execute('SELECT title FROM posts;').fetchall()
        conn.close()

        if radios is not None:
            for row in radios:
                radio = row[0]
                delete_blacklist(radio)


def feature_blacklist_switch_status(status):
    """
    first run ever creates db entry for the feature,
    then switch and returns on or off
    """
    enabled = 0
    first_run = False
    if not status:
        enabled = 1
        ghettoApi.blacklist_enabled_global = True
        first_run = True
    if status:
        if int(status[0]) == 0:
            enabled = 1
            ghettoApi.blacklist_enabled_global = True
        if int(status[0]) == 1:
            enabled = 0
            ghettoApi.blacklist_enabled_global = False

    conn = eisen_db.get_db_connection()
    if first_run:
        # first app had no further cols in db, so reuse the existing col and add row 2
        conn.execute('INSERT INTO eisen_intern (browser_open) VALUES (?);', (enabled,))
    if not first_run:
        conn.execute('UPDATE eisen_intern SET browser_open = ? WHERE id = ?;', (enabled, 2))
    conn.commit()
    conn.close()
    return enabled


def fill_radio_display_col():
    """mocking the db entries for dev and test"""

    # call it in eishome.index_first_run()
    classic = ['Aurèle Marthan Rafaël Angster Guillaume Begni Philibert Perrine & Amaury Viduvier - Quintet in E-Flat '
               'Major K 452 III Allegretto', 'Vladimir Ashkenazy - Nocturne No 20 in C sharp Minor Op posth']
    goa_psi = ['Electric Universe - Activate  animaskntru', 'Bafoomay - Monosonicum Miles Away Mix  animaskntru']
    time_machine = ['Murder at Midnight - 12 The Man Who Died Yesterday', "The Adventures of Philip Marlowe - The "
                                                                          "Fox's Tail"]
    nerd_sound_tracks = ['Lyn - Autonomy', 'Takayuki Iwai Yuki Iwai Isao Abe Hideki Okugawa Tetsuya Shibata - Active '
                                           'Red Theme of Ken']  # nerd-sound-tracks
    BLUES_UK = ['Nothing But The Devil', 'Henrik - Schlader band']
    relax = ['Mission Brown - Another Beginning', 'Neil Davidge - Sensor Melo Remix']
    Nachtflug = ['Helium Vola - Selig', 'Kite - Hand Out the Drugs']
    hm = ['E-Spectro - Dawn On Sunset Vla DSound Rem', "Alex O'Rion - Komodo"]
    Boradio = ['AutoDJ - Various']
    B2 = ['Hör auf Dein Herz wwwSchlagerRadiode', 'Beatrice Egli - Verrückt Nach Dir']

    radio_dict = {
        'classic': classic,
        'goa_psi': goa_psi,
        'time_machine': time_machine,
        'nerd-sound-tracks': nerd_sound_tracks,
        'BLUES_UK': BLUES_UK,
        'relax': relax,
        'Nachtflug': Nachtflug,
        'hm': hm,
        'Boradio': Boradio,
        'B2': B2
    }

    conn = eisen_db.get_db_connection()

    for radio, blacklist in radio_dict.items():
        # json.dumps() to string, json.loads() to object
        conn.execute('UPDATE posts SET display = ? WHERE title = ?;', (json.dumps(blacklist), radio))
        conn.commit()

    conn.close()
