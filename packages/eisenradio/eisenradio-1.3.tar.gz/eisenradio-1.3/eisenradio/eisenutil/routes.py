import os
import eisenradio.lib.ghetto_recorder as ghetto
import eisenradio.eisenutil.eisutil as eis_util
import eisenradio.eisenutil.browser_stream as browser_stream
import eisenradio.eisenutil.stopped_stations as stopped_stations
from flask import Blueprint, render_template, request, url_for, flash, redirect, make_response, jsonify, Response
from eisenradio.eisenutil import request_info
from eisenradio.eisenutil import tools as util_tools
from eisenradio.lib import eisdb as lib_eisdb
from eisenradio.api import ghettoApi
from eisenradio.eisenutil import monitor_records as mon_rec

blacklist_enabled_global = False
ghettoApi.init_ghetto_blacklist_enabled_global(blacklist_enabled_global)

# Blueprint Configuration
eisenutil_bp = Blueprint(
    'eisenutil_bp', __name__,
    template_folder='bp_util_templates',
    static_folder='bp_util_static',
    static_url_path='/bp_util_static'
)


@eisenutil_bp.after_request
def add_header(response):
    """
    only computer internal traffic from browser to server,
    BUT browser looks for allow-origin header plus localhost to disable cors restrictions
    put it here, so it will be not forgotten
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@eisenutil_bp.route('/tools_radio_blacklist_set', methods=['GET'])
def tools_radio_blacklist_set():
    """
    enable blacklist first time, then switch status
    a call to this endpoint will change the value in db and delete all lists of all radios in db
    button is fashioned in tools()
    """
    is_enabled = mon_rec.status_db_blacklist_get()
    enabled = mon_rec.feature_blacklist_switch_status(is_enabled)
    mon_rec.delete_all_blacklists(enabled)
    if enabled:
        flash('Monitoring of records enabled.', 'success')
    else:
        flash('Monitoring of records disabled', 'warning')
    return redirect(url_for('eisenhome_bp.index'))


@eisenutil_bp.route('/<string:radio_name>/tools_blacklist_skipped', methods=['GET'])
def tools_blacklist_skipped(radio_name):
    """
    the count of skipped titles per session, show in html
    add link to start page
    """
    radio_start_page_url = eis_util.radio_start_page_url_get(radio_name)

    skiplist, skip_count = '', 0
    try:
        skiplist = ghettoApi.skipped_in_session_dict[radio_name]
        skip_count = len(skiplist)
    except KeyError:
        pass
    return render_template('bp_util_skip_blacklist.html',
                           radio_start_page_url=radio_start_page_url,
                           radio_name=radio_name,
                           skiplist=skiplist,
                           skip_count=skip_count)


@eisenutil_bp.route('/tools_blacklist_overview', methods=['GET'])
def tools_blacklist_overview():
    """
    creates a html page with buttons for every radio to go to the blacklists edit page
    change btn color for radios with active rec
    shows the count of blacklisted titles
    """
    skip_count = 0
    view_dict = ghettoApi.radios_in_view_dict  # key db id: val name
    skip_title_dict = ghettoApi.skipped_in_session_dict    # key radio: val title list
    blacklist_dict = ghettoApi.all_blacklists_dict
    streamer_name_list = []
    radio_blacklist_count = {}

    for db_id, btn_pressed in ghettoApi.rec_btn_dict.items():
        if btn_pressed:
            streamer_name_list.append(view_dict[db_id])
    for title_list in skip_title_dict.values():
        if title_list is not None:
            for _ in title_list:
                skip_count += 1
    for radio, title in blacklist_dict.items():
        blacklist_count = 0
        if title is not None:
            for _ in title:
                blacklist_count += 1
            radio_blacklist_count[radio] = blacklist_count

    return render_template('bp_util_radio_all_blacklist.html',
                           radios_dict=view_dict,
                           streamer_name_list=streamer_name_list,
                           skip_count=skip_count,
                           radio_blacklist_count=radio_blacklist_count)


@eisenutil_bp.route('/<string:radio_name>/tools_radio_blacklist', methods=['GET'])
def tools_radio_blacklist(radio_name):
    """
    html page for a blacklist of one radio
    """
    radio_start_page_url = eis_util.radio_start_page_url_get(radio_name)

    blacklist = mon_rec.dump_radio_blacklist_from_col(radio_name)
    sorted_title_dict = mon_rec.sort_dictionary_by_value(blacklist)
    skip_count = 0
    try:
        skip_count = len(ghettoApi.skipped_in_session_dict[radio_name])
    except KeyError:
        pass
    return render_template('bp_util_radio_blacklist.html',
                           radio_start_page_url=radio_start_page_url,
                           counter=len(blacklist),
                           sorted_title_dict=sorted_title_dict,
                           skip_count=skip_count,
                           radio_name=radio_name)


@eisenutil_bp.route('/tools_radio_blacklist_del_from_list', methods=['POST'])
def tools_radio_blacklist_del_from_list():
    """
    can delete one or more title from the list, can delete the whole list
    java: delFromBlacklist(), html: bp_util_radio_blacklist.html
    """
    if request.method == 'POST':
        request_dict = request.form.to_dict()
        radio_name = request_dict['radio_name']
        delete_list = request_dict['delAll']
        # java
        if delete_list == 'false':
            mon_rec.del_single_title_master(radio_name, request_dict)
        if delete_list == 'true':
            mon_rec.delete_blacklist(radio_name)
        msg = "_ok_"
        return jsonify({'delFromBlacklist': msg})


@eisenutil_bp.route('/tools_export_blacklists', methods=['GET'])
def tools_export_blacklists():
    """
    java toolsExportBlacklists() creates alert for error success
    simple buttons can work with onclick event, button in a form disliked it
    to see the effort between flash and java alert, same
    """
    rv = util_tools.dump_radio_blacklist()
    json_result = 'true' if rv else "-empty-"
    return jsonify({'toolsExportBlacklists': json_result})


@eisenutil_bp.route('/tools_upload_blacklists', methods=['POST'])
def tools_upload_blacklists():
    """
    upload, this is a flask web server
    restore the blacklists from *json file
    must return something other than bool or None to flash a message
    """
    file = request.files['inputFile']
    try:
        json_file = file.read()
        rv = util_tools.upload_blacklists(json_file)
    except Exception as error:
        print(error)
        return f'Something went wrong. error :: {error}'
    if rv:
        flash('Successfully imported! Lists are loaded. Can proceed, if "Monitor Records" is enabled.', 'success')
        return render_template('bp_util_flash.html')
    else:
        flash('Something went wrong, use "Tools" Menu to go back! Wrong text utf-format? Wrong file? \nRead terminal '
              'messages, please. If possible', 'warning')
        return render_template('bp_util_flash.html')


@eisenutil_bp.route('/tools_delete_all', methods=['POST'])
def tools_delete_all():
    """
    delete all radios from db
    used to restore from ini file with preferred radios and urls afterwards
    """
    rv = util_tools.delete_all_radios()
    if rv:
        flash('Successfully deleted! Restart App', 'success')
        return render_template('bp_util_flash.html')
    else:
        flash('Some were not deleted! Restart App', 'warning')
        return render_template('bp_util_flash.html')


@eisenutil_bp.route('/tools_export_ini', methods=['GET'])
def tools_export_ini():
    """
    export radios, urls to ini file
    java toolsExportIni()
    """
    rv = util_tools.export_radios()
    json_result = 'true' if rv else "-empty-"
    return jsonify({'toolsExportIni': json_result})


@eisenutil_bp.route('/tools_upload_ini', methods=['POST'])
def tools_upload_ini():
    """
    restore radios, urls from ini to db
    """
    file = request.files['inputFile']
    print(f' name {file.name} content-type {file.content_type}')
    try:
        settings_ini = file.read()
        rv = util_tools.upload_radios(settings_ini.decode('ascii'))
    except Exception as error:
        print(error)
        return f'Something went wrong. error :: {error}'
    if rv:
        flash('Successfully imported! Restart the App!', 'success')
        return render_template('bp_util_flash.html')
    else:
        flash('Something went wrong, use "Tools" Menu to go back! Wrong text utf-format? Wrong file? \nRead terminal '
              'messages, please. If possible', 'warning')
        return render_template('bp_util_flash.html')


@eisenutil_bp.route('/tools', methods=('GET', 'POST'))
def tools():
    """
    main menu
    button to switch blacklist feature on/off
    display path for exported files (same as parent download path)
    """

    is_enabled = mon_rec.status_db_blacklist_get()
    enabled = mon_rec.blacklist_enabled_button_outfit_get(is_enabled)
    button_label = ' ON' if enabled else 'OFF'
    btn_msg = "Turn OFF to delete all lists and stop monitoring." if enabled else "Turn ON to start monitoring."
    export_path = util_tools.get_export_path()
    return render_template('bp_util_tools.html',
                           export_path=export_path,
                           button_label=button_label,
                           button_message=btn_msg,
                           enabled=enabled)


@eisenutil_bp.route('/about', methods=('GET', 'POST'))
def about():
    """
    main menu
    the app info, license, help, shows radios parent dir and db path
    """
    if request.method == 'POST':
        if request.form['browser']:
            lib_eisdb.status_read_status_set(True, 'eisen_intern', 'browser_open', '1')
            return redirect(url_for('eisenutil_bp.about'))

    is_browser_on = lib_eisdb.status_read_status_set(False, 'eisen_intern', 'browser_open', '1')
    download_path = lib_eisdb.get_download_dir()
    db_path = lib_eisdb.get_db_path()
    return render_template('bp_util_about.html',
                           is_browser_on=is_browser_on,
                           download_path=download_path,
                           db_path=db_path)


@eisenutil_bp.route('/create', methods=('GET', 'POST'))
def create():
    """
    "New" main menu
    """
    if request.method == 'POST':
        rv_req = request.form['title']
        title = eis_util.remove_blank(rv_req)
        name_in_db = eis_util.is_in_db_view(title)
        content = request.form['content']
        radio_image = None
        content_type = None

        if not title:
            flash('Name is required!', 'warning')
            return render_template('bp_util_create.html')
        if name_in_db:
            flash('Name is already used!', 'warning')
            return render_template('bp_util_create.html')
        if not content:
            flash('URL is required!', 'warning')
            return render_template('bp_util_create.html')

        # Image
        if request.files['inputFile']:
            file = request.files['inputFile']
            content_type = file.content_type
            print(f' name {file.name} content-type {file.content_type}')
            try:
                db_img = file.read()
                radio_image = lib_eisdb.render_picture(db_img, 'encode')
            except Exception as e:
                print(e)
                radio_image = None
                content_type = None

        else:
            if not name_in_db:
                radio_image, content_type = util_tools.radio_spare_image()

        if request.form['text']:
            text = request.form['text']
        else:
            text = None

        conn = lib_eisdb.get_db_connection()
        posts = conn.execute('SELECT * FROM posts').fetchall()
        # if we later want extra save folders for each radio
        try:
            request_path = posts[0]["download_path"]
        except Exception as e:
            print(e)
            print(' looks like the first radio to create, no save to path set')
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
        else:
            conn.execute('INSERT INTO posts (title, content, download_path, pic_data, pic_content_type, pic_comment) '
                         'VALUES (?, ?, ?, ?, ?, ?)',
                         (title, content, request_path, radio_image, content_type, text))

        conn.commit()
        conn.close()
        return redirect(url_for('eisenhome_bp.index'))

    return render_template('bp_util_create.html')


@eisenutil_bp.route('/save', methods=('GET', 'POST'))
def save():
    """
    main menu
    """
    if request.method == 'GET':
        """
        fail if db empty
        """
        try:
            os.path.abspath(lib_eisdb.get_download_dir())
        except TypeError:
            return render_template('bp_util_save.html', save_to='no-directory-found')
        return render_template('bp_util_save.html', save_to=os.path.abspath(lib_eisdb.get_download_dir()))

    if request.method == 'POST':
        request_path = os.path.abspath(request.form['Path_Save_To'])

        if not request_path:
            flash('A folder is required!', 'warning')
            try:
                os.path.abspath(lib_eisdb.get_download_dir())
            except TypeError:
                return render_template('bp_util_save.html', save_to='no-directory-found')
            return render_template('bp_util_save.html', save_to=os.path.abspath(lib_eisdb.get_download_dir()))

        if request_path:
            made_it = eis_util.make_folder(request_path)
            if not made_it:
                flash('No folder created! exists or denied', 'warning')
                return render_template('bp_util_save.html', save_to=os.path.abspath(lib_eisdb.get_download_dir()))

            conn = lib_eisdb.get_db_connection()
            records = conn.execute('select id from posts').fetchall()
            if not records:
                flash('Noting in Database!', 'warning')
                try:
                    return render_template('bp_util_save.html', save_to=os.path.abspath(lib_eisdb.get_download_dir()))
                except TypeError:
                    return render_template('bp_util_save.html', save_to='no-row-in-table-create-a-radio')
            for id_num in records:
                # print("Radio Id:", id_num[0])
                conn.execute('UPDATE posts SET download_path = ? WHERE id = ?', (request_path, id_num[0]))
            conn.commit()
            conn.close()

            flash(('Save files to: ' + request_path), "success")
            return redirect(url_for('eisenhome_bp.index'))

        return render_template('bp_util_save.html', save_to=os.path.abspath(lib_eisdb.get_download_dir()))


@eisenutil_bp.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    """
    edit button
    """
    post = lib_eisdb.get_post(id)

    if request.method == 'POST':
        rv_req = request.form['title']
        title = rv_req.replace(" ", "")
        content = request.form['content']

        if not title:
            flash('Title is required!', 'warning')
        # Image, if empty keep db entry as it is
        if request.files['inputFile']:
            file = request.files['inputFile']
            content_type = file.content_type
            print(f' name {file.name} content-type {file.content_type}')
            try:
                db_img = file.read()
                image = lib_eisdb.render_picture(db_img, 'encode')
            except Exception as e:
                print(e)
                image = None
                content_type = None

        else:
            image = None
            content_type = None

        if request.form['text']:
            text = request.form['text']
            if text == 'None':
                text = ' '
        else:
            text = ' '

        conn = lib_eisdb.get_db_connection()
        if image:
            conn.execute('UPDATE posts SET title = ?, content = ?, pic_data = ?, pic_content_type = ?, '
                         'pic_comment = ? WHERE id = ?',
                         (title, content, image, content_type, text, id))
        else:
            conn.execute('UPDATE posts SET title = ?, content = ?, pic_comment = ?  WHERE id = ?',
                         (title, content, text, id))

        conn.commit()
        conn.close()
        return redirect(url_for('eisenhome_bp.index'))

    return render_template('bp_util_edit.html', post=post)


@eisenutil_bp.route('/<int:post_id>')
def post(post_id):
    """
    picture of the radio, go to external site if possible
    """
    post = lib_eisdb.get_post(post_id)
    url_port = ghetto.GIni.parse_url_simple_url(post["content"])

    return render_template('bp_util_post.html',
                           post=post,
                           url_port=url_port)


@eisenutil_bp.route('/sw')
def stream_watcher():
    resp = make_response("stream watcher    (ಠ_ಠ)")
    return resp


@eisenutil_bp.route('/header_info', methods=['GET'])
def header_info():
    """
    returns all possible header info of radio request, name, bit rate, website ...
    """
    json_lists = request_info.header_data_read()
    if len(json_lists) == 0:
        json_lists = '-empty-'
    return jsonify({"header_result": json_lists})


@eisenutil_bp.route('/delete_info', methods=['GET'])
def delete_info():
    """
    return a list of all inactive radio ids to clean html page
    """
    json_list = stopped_stations.inactive_id_read()
    if len(json_list) == 0:
        json_list = '-empty-'
    return jsonify({"stopped_result": json_list})


@eisenutil_bp.route('/sound/<radio_name>', methods=['GET'])
def sound(radio_name):
    """
    streams audio to html audio element if connected, local audio via javascript (use upload functionality)
    """
    name = str(radio_name)
    try:
        content_type = os.environ[name]
    except KeyError:
        content_type = browser_stream.get_stream_content_type(name)

    audio_chunks = browser_stream.stream_audio_feed(name)

    response = Response(audio_chunks, mimetype=content_type)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
