from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, jsonify

import eisenradio.eisenhome.eishome as eis_home
from eisenradio.lib.eisdb import get_post, delete_radio, enum_radios
from eisenradio.api import ghettoApi

# Blueprint Configuration
eisenhome_bp = Blueprint(
    'eisenhome_bp', __name__,
    template_folder='bp_home_templates',
    static_folder='bp_home_static',
    static_url_path='/bp_home_static'
)


@eisenhome_bp.route('/', methods=('GET', 'POST'))
def index():
    """
    main page
    replace "ghettorecorder.win"
    """
    local_host_sound_route = "http://localhost:" + ghettoApi.work_port + "/sound/"
    listen_last_url = ""

    if eis_home.first_run_index:
        eis_home.check_write_protected()
    posts = enum_radios()
    eis_home.index_first_run(posts)
    current_station, current_table_id = eis_home.curr_radio_listen()

    if request.method == 'POST':
        # print_request_values(request.form.values())
        post_request = request.form.to_dict()  # flat dict werkzeug doc
        # $("button").click(function () {}, ajax
        json_post = eis_home.index_posts_clicked(post_request)
        # returns False on error to deactivate buttons for newly created radios, app restart required
        if json_post:
            return json_post

    if current_station:
        listen_last_url = local_host_sound_route + current_station

    return render_template('bp_home_index.html',
                           posts=posts,
                           combo_master_timer=eis_home.combo_master_timer,
                           status_listen_btn_dict=eis_home.status_listen_btn_dict,
                           status_record_btn_dict=eis_home.status_record_btn_dict,
                           current_station=current_station,
                           current_table_id=current_table_id,
                           # listen_last_url=eis_home.listen_last_url    # may not be internet - cors zeroes out
                           listen_last_url=listen_last_url)


@eisenhome_bp.route('/page_flash', methods=('GET', 'POST'))
def page_flash():
    eis_home.combo_master_timer = 0  # master timer recording
    eis_home.progress_master_percent = 0

    flash('Count down timer ended all activities. App restart recommended!', 'success')
    return render_template('bp_home_page_flash.html')


@eisenhome_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    if eis_home.status_listen_btn_dict[id] or eis_home.status_record_btn_dict[id]:
        flash('Radio is active. No deletion.', 'warning')
        return redirect(url_for('eisenhome_bp.index'))

    post = get_post(id)
    rv = delete_radio(id)
    if rv:
        flash('"{}" was successfully deleted!'.format(post['title']), 'success')
    if not rv:
        flash('"{}" was not deleted!'.format(post['title']), 'warning')
    return redirect(url_for('eisenhome_bp.index'))


@eisenhome_bp.route('/cookie_set_dark', methods=['GET', 'POST'])
def cookie_set_dark():
    """
    secure=False for http and https
    localhost is an inner Network of the computer used by Eisenradio server and browser, therefore a save place
    secure=True without external signed ssl certs will NOT rise security nor let disappear errors in InetExplorer
    """
    resp = make_response("Eisenkekse sind die besten")
    resp.set_cookie('eisen-cookie', 'darkmode', max_age=60*60*24*365*2, secure=False, httponly=True)
    return resp


@eisenhome_bp.route('/cookie_get_dark', methods=['GET'])
def cookie_get_dark():
    mode = request.cookies.get('eisen-cookie', None)
    return jsonify({'darkmode': mode})


@eisenhome_bp.route('/cookie_del_dark', methods=['POST'])
def cookie_del_dark():
    resp = make_response("necesito nuevas cookies")
    resp.set_cookie('eisen-cookie', max_age=0)
    return resp


@eisenhome_bp.route('/station_get', methods=['GET'])
def station_get():
    """
    the active radio name listened; rebuild console after page refresh
    empty dict if no listen, else send name and db table id
    """
    listen_dict = {}
    current_station, current_table_id = eis_home.curr_radio_listen()
    if len(current_station) > 0:
        listen_dict[current_station] = current_table_id
    return jsonify({'stationGet': listen_dict})


@eisenhome_bp.route('/streamer_get', methods=['GET'])
def streamer_get():
    """
    all stations with active rec; populate dropdown in console after page refresh
    empty dict if no streamer, else send name and db table id
    """
    streamer_dict = {}
    if len(eis_home.active_streamer_dict) > 0:
        for rec_station, rec_station_id in eis_home.active_streamer_dict.items():
            streamer_dict[rec_station] = rec_station_id
    return jsonify({'streamerGet': streamer_dict})


@eisenhome_bp.route('/cookie_set_show_visuals', methods=['GET', 'POST'])
def cookie_set_show_visuals():
    resp = make_response("disable visualisation")
    resp.set_cookie('eisen-cookie-visuals', 'show_visuals', max_age=60*60*24*365*2, secure=False, httponly=True)
    ghettoApi.init_ghetto_show_analyser(False)
    return resp


@eisenhome_bp.route('/cookie_get_show_visuals', methods=['GET'])
def cookie_get_show_visuals():
    rv = request.cookies.get('eisen-cookie-visuals', None)

    if rv == 'show_visuals':
        return jsonify({'str_visuals': 'show_visuals'})
    if not rv:
        return jsonify({'str_visuals': '-empty-'})


@eisenhome_bp.route('/cookie_del_show_visuals', methods=['POST'])
def cookie_del_show_visuals():
    resp = make_response("bye\neisen-cookie-visuals")
    resp.set_cookie('eisen-cookie-visuals', max_age=-1)
    ghettoApi.init_ghetto_show_analyser(True)
    return resp


@eisenhome_bp.route('/index_posts_combo', methods=['POST'])
def index_posts_combo():
    eis_home.combo_master_timer = request.form['timeRecordSelectAll']
    return eis_home.combo_master_timer


@eisenhome_bp.route('/index_posts_percent', methods=['POST'])
def index_posts_percent():
    return jsonify({'result': eis_home.progress_master_percent})


@eisenhome_bp.route('/display_info', methods=['GET'])
def display_info():
    """
    updateDisplay() ajax
    """
    if request.method == "GET":
        id_text_dict = {}
        try:
            for radio_name, radio_text in ghettoApi.ghetto_radios_metadata_text.items():
                for radio_db_id, radio_title in ghettoApi.radios_in_view_dict.items():
                    if radio_name == radio_title:
                        if len(radio_text) > 0:
                            id_text_dict[str(radio_db_id)] = str(radio_text)

            for radio_name, radio_error in ghettoApi.ghetto_dict_error.items():
                for radio_db_id, radio_title in ghettoApi.radios_in_view_dict.items():
                    if radio_name == radio_title:
                        id_text_dict[str(radio_db_id)] = str(radio_error)
        except Exception as error:
            print(f'display_info: {error}')

        return jsonify({"updateDisplay": id_text_dict})

