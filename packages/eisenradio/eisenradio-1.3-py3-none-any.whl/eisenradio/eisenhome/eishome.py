import os
import threading
from time import sleep
from flask import jsonify, request, flash, redirect, url_for

from eisenradio.eisenhome import watchdog
from eisenradio.eisenutil import monitor_records
import eisenradio.lib.ghetto_recorder as ghetto
from eisenradio.lib.eisdb import get_db_connection, status_read_status_set, get_download_dir
from eisenradio.api import ghettoApi

first_run_index = True

status_listen_btn_dict = {}  # {table id 15: 1 } on
status_record_btn_dict = {}
radios_in_view_dict = {}
ghettoApi.init_lis_btn_dict(status_listen_btn_dict)
ghettoApi.init_rec_btn_dict(status_record_btn_dict)
ghettoApi.init_radios_in_view(radios_in_view_dict)
stop_blacklist_writer = False
ghettoApi.init_ghetto_stop_blacklist_writer(stop_blacklist_writer)
# make a drop-down dialog to jump to the rec stations
active_streamer_dict = {}

last_btn_id_global = None  # current button pressed, or btn predecessor
combo_master_timer = 0
progress_master_percent = 0


def index_first_run(posts):
    global first_run_index
    if first_run_index:
        first_run_index = False
        check_write_protected()
        start_progress_timer_daemon()
        monitor_records.start_blacklist_writer_daemon()
        # watchdog.start_watchdog_daemon()

        feed_status_btn_dicts(posts)
        feed_radios_in_view_dict(posts)


def feed_status_btn_dicts(posts):
    for row in posts:
        # init btn not pressed
        status_listen_btn_dict[row['id']] = 0
        status_record_btn_dict[row['id']] = 0


def feed_radios_in_view_dict(posts):
    for row in posts:
        # api
        radios_in_view_dict[row['id']] = status_read_status_set(False, 'posts', 'title', row['id'])


def curr_radio_listen():
    """
    get calls from @eisenhome_bp.route
    """
    current_station = ''
    current_table_id = ''
    for key_table_id, val in status_listen_btn_dict.items():
        if val:
            current_station = status_read_status_set(False, 'posts', 'title', key_table_id)
            current_table_id = key_table_id
    return current_station, current_table_id


def index_posts_clicked(post_request):
    """
    route /
    If listen button pressed, java auto clicker event is possible to change the button type (color).
    Auto clicker launches the whole event $("button").click(function () {} from $(document).ready(function () {
    AFTER the original button was pressed.
    Two scenarios for a 1 in status_listen_btn_dict[int(table_id)]:
    1) auto clicker
    2) same listen button was pressed on/off (twice)
    Distribute button clicks to listen, rec dispatcher functions
   """
    global last_btn_id_global

    try:
        button_list = post_request['name'].split('_')
    except KeyError:
        return
    table_id = button_list[1]     # this id from db table will control the action here
    button = button_list[0]

    if button == 'Listen':

        if int(table_id) not in status_listen_btn_dict.keys():
            print('app restart required to listen to a new radio')
            return False

        radio_name = status_read_status_set(False, 'posts', 'title', table_id)

        if status_listen_btn_dict[int(table_id)]:     # 1, hello auto clicker; or on/off press
            status_listen_btn_dict[int(table_id)] = 0
            dispatch_master(int(table_id), 'Listen', 0)
            if not last_btn_id_global == table_id:    # only auto clicker, since id is not the same id
                return jsonify({'result': 'auto_clicker, no_audio_action, no_action_at_all'})

            last_btn_id_global = None                 # twice pressed, reset var
            # eject src or audio element plays the rest of buffer; the other clicks change endpoint srv:/sound/<radio>
            return jsonify(
                {'result': 'deactivate_audio',
                 'former_button_to_switch': False,
                 'table_ident': radio_name,
                 'radio_table_id': table_id
                 })
        else:
            status_listen_btn_dict[int(table_id)] = 1  # 0, real click, set pressed to True
            dispatch_master(int(table_id), 'Listen', 1)
            btn_to_switch = last_btn_id_global         # activate auto clicker
            last_btn_id_global = table_id
            # last_btn_id_global init with None, so first radio do not trigger a click
            return jsonify(
                {'result': 'activate_audio',
                 'former_button_to_switch': btn_to_switch,
                 'table_ident': radio_name,
                 'radio_table_id': table_id,
                 'sound_endpoint': "http://localhost:" + ghettoApi.work_port + "/sound/"
                 })

    if button == 'Record':
        return index_posts_record(table_id)


def index_posts_record(table_id):
    """
    start, stop rec
    make a combo box with anchor to jump to the rec radio from console
    """
    if int(table_id) not in status_record_btn_dict.keys():
        print('app restart required to record')
        return False

    conn = get_db_connection()
    radio_name = status_read_status_set(False, 'posts', 'title', table_id)
    conn.close()

    if status_record_btn_dict[int(table_id)]:
        del active_streamer_dict[radio_name]
        status_record_btn_dict[int(table_id)] = 0
        dispatch_master(int(table_id), 'Record', 0)
    else:
        active_streamer_dict[radio_name] = str(table_id)
        status_record_btn_dict[int(table_id)] = 1
        dispatch_master(int(table_id), 'Record', 1)

    # make combo box with anchor jumper from active_streamer_dict
    json_streamer = ''
    for streamer_name, streamer_id in active_streamer_dict.items():
        json_streamer = json_streamer + str(streamer_name) + '=' + str(streamer_id) + ','
    if not json_streamer:
        json_streamer = str('empty_json')

    return jsonify(
        {'result': 'no_audio_result',
         'rec_btn_id': table_id,
         'streamer': json_streamer,        # $("button").click(function () {
         'former_button_to_switch': False,
         'radio_table_id': table_id
         })


def query_radio_url(table_id):
    radio_url = status_read_status_set(False, 'posts', 'content', table_id)
    return radio_url


def set_radio_path(table_id):
    """
    overwrites the default path in GhettoRecorder with download_path
    """
    radio_path = status_read_status_set(False, 'posts', 'download_path', table_id)
    ghetto.GBase.radio_base_dir = radio_path


def dispatch_master(table_id, button, btn_status):
    """
    btn_status is 0 or 1
    """
    set_radio_path(table_id)
    radio_name = status_read_status_set(False, 'posts', 'title', table_id)

    if button == 'Listen':
        dispatch_listen_btn(radio_name, table_id, btn_status)

    if button == 'Record':
        dispatch_record_btn(radio_name, table_id, btn_status)


def dispatch_listen_btn(radio_name, table_id, lis_btn_pressed):
    if lis_btn_pressed:
        ghetto.GRecorder.listen_active_dict[radio_name] = True
        if not status_record_btn_dict[table_id]:  # rec btn not pressed
            ghetto.GRecorder.record_active_dict[radio_name] = False  # rec not active
        dispatch_record_start(table_id, 'listen')

    if not lis_btn_pressed:
        ghetto.GRecorder.listen_active_dict[radio_name] = False


def dispatch_record_btn(radio_name, table_id, rec_btn_pressed):
    if rec_btn_pressed:
        ghetto.GRecorder.record_active_dict[radio_name] = True
        if not status_listen_btn_dict[table_id]:  # listen btn not pressed
            ghetto.GRecorder.listen_active_dict[radio_name] = False

        dispatch_record_start(table_id, 'record')

    if not rec_btn_pressed:
        ghetto.GRecorder.record_active_dict[radio_name] = False    # rec thread stops, parameter action 'record'


def dispatch_record_start(table_id, action):
    """
    test if server is alive
    test dict_error, entry if url had failed
    start thread with either listen or record action
    """
    radio_name = status_read_status_set(False, 'posts', 'title', table_id)
    radio_url = status_read_status_set(False, 'posts', 'content', table_id)

    playlist_url = dispatch_record_is_alive(radio_name, radio_url)
    if playlist_url is not None:
        radio_url = playlist_url

    if radio_name not in ghetto.GBase.dict_error.keys():
        ghetto.record(radio_name, radio_url, action)
    else:
        print(ghetto.GBase.dict_error[radio_name])
        ghetto.GBase.dict_exit[radio_name] = True    # end all threads of a failed radio; if any


def dispatch_record_is_alive(radio_name, radio_url):
    """
    test server is alive, if not writes in error dict to later display msg in html
    url is a playlist; grabs first url from playlist, mostly the best quality
    https://streams.br.de/bayern1obb_2.m3u
    """
    is_url_m3u = ghetto.check_alive_playlist_container(radio_name, radio_url)
    if is_url_m3u:
        return is_url_m3u
    return


def start_progress_timer_daemon():
    threading.Thread(name="progress_timer", target=progress_timer, daemon=True).start()


def progress_timer():
    global combo_master_timer  # combo in Tk/Tcl for drop-down dialog on ghetto_recorder package, first front-end
    global progress_master_percent  # separate for future us; go to single timer for each radio

    current_timer = 0
    while 1:
        if combo_master_timer:
            if int(combo_master_timer) <= -1:
                combo_time = 1
            else:
                combo_time = (int(combo_master_timer) * 60 * 60)  # * 60
            percent = progress_bar_percent(current_timer, combo_time)
            if percent:
                progress_master_percent = percent
            else:
                progress_master_percent = 0
                current_timer = 0

            if percent >= 100:
                ghettoApi.stop_blacklist_writer = True
                found = 0
                for _ in ghetto.GBase.dict_exit:
                    found += 1
                if found:
                    for recorder in ghetto.GBase.dict_exit:
                        ghetto.GBase.dict_exit[recorder] = True

        if not combo_master_timer:
            current_timer = 0
            progress_master_percent = 0

        current_timer += 1
        sleep(1)


def progress_bar_percent(current_timer, max_value):
    if not max_value:
        return False
    # doing some math, p = (P * 100) / G, percent = (math.percentage value * 100) / base
    cur_percent = round((current_timer * 100) / max_value, 4)  # 0,0001 for 24h reaction to show
    return cur_percent


def print_request_values(values):
    for val in values:
        print(' -- start print --')
        print(f'\tval in request.form.values(): {val}')
        print(f'\trequest.data {request.data}')
        print(f'\trequest.form {request.form}')
        print(f'\trequest.values {request.values}')
        print(f'\trequest.form.to_dict() {request.form.to_dict()}')
        print(' -- end print --')


def check_write_protected():
    try:
        download_dir = os.path.abspath(get_download_dir())
    except TypeError:
        return
    if download_dir is None:
        flash('Can not write to folder! No folder specified.', 'danger')
        return redirect(url_for('eisenhome_bp.index'))
    if download_dir:
        write_file = download_dir + '/eisen_write_test'
        try:
            with open(write_file, 'wb') as record_file:
                record_file.write(b'\x03')
            os.remove(write_file)
        except OSError:  # master of desaster
            flash('Can not write to folder!.' + download_dir, 'danger')
            return redirect(url_for('eisenhome_bp.index'))
    if not download_dir:
        flash('Can not write to folder! no folder specified' + download_dir, 'danger')
        return redirect(url_for('eisenhome_bp.index'))
