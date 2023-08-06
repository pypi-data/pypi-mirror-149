

class Api:
    def __init__(self):
        self.config = None

    def init_app(self, app):
        self.config = app.config

    def __repr__(self):
        return f"api.init_app({self.config})"

    def __str__(self):
        return f"Flask application factory config: {self.config}"


class GhettoApi:

    def __init__(self):
        self.lis_btn_dict = None
        self.rec_btn_dict = None
        self.radios_in_view_dict = None
        self.ghetto_radios_metadata_text = None
        self.ghetto_dict_error = None
        self.ghetto_measure_dict = None
        self.ghetto_audio_stream_dict = None
        self.ghetto_show_analyser = True
        self.local_play_suffix = None
        self.local_play_queue = None
        self.listen_active_dict = None
        self.recorder_new_title_dict = None
        self.all_blacklists_dict = None
        self.stop_blacklist_writer = None
        self.blacklist_enabled_global = None
        self.skipped_in_session_dict = None
        self.work_port = None

    def init_lis_btn_dict(self, lis_btn_dict):
        self.lis_btn_dict = lis_btn_dict

    def init_rec_btn_dict(self, rec_btn_dict):
        self.rec_btn_dict = rec_btn_dict

    """key:db id, val: radio name shown on html"""
    def init_radios_in_view(self, radios_in_view_dict):
        self.radios_in_view_dict = radios_in_view_dict

    """key:radio name, val: text from metadata"""
    def init_ghetto_radios_metadata_text(self, ghetto_radios_metadata_text):
        self.ghetto_radios_metadata_text = ghetto_radios_metadata_text

    """key:radio name, val: error"""
    def init_ghetto_dict_error(self, ghetto_dict_error):
        self.ghetto_dict_error = ghetto_dict_error

    """"show meta data"""
    def init_ghetto_measurements(self, ghetto_measure_dict):
        self.ghetto_measure_dict = ghetto_measure_dict

    """show frequency analyser, transfer buffer data for js AudioContext , ..dict[key + ',audio']"""
    def init_ghetto_audio_stream(self, ghetto_audio_stream_dict):
        self.ghetto_audio_stream_dict = ghetto_audio_stream_dict

    """set cookie to show or hide analyser, true or false"""
    def init_ghetto_show_analyser(self, ghetto_show_analyser):
        self.ghetto_show_analyser = ghetto_show_analyser

    """upload local sound to server to make byte array and get duration info (*aacp files), not working so far """
    def init_eisen_local_play_suffix(self, local_play_suffix):
        self.local_play_suffix = local_play_suffix

    """get sample rate, frequency and channel num to calculate time,some aac show no time, audio element stuck"""
    def init_eisen_local_play_queue(self, local_play_queue):
        self.local_play_queue = local_play_queue

    def init_ghetto_listen_active_dict(self, listen_active_dict):
        self.listen_active_dict = listen_active_dict

    """radios write a title from metadata here (minus remove_special_chars() in g_recorder, like copied file name)"""
    def init_ghetto_recorder_new_title(self, recorder_new_title_dict):
        self.recorder_new_title_dict = recorder_new_title_dict
    """a dict where all radios show their blacklist, so recorder can compare title from metadata """
    def init_ghetto_all_blacklists_dict(self, all_blacklists_dict):
        self.all_blacklists_dict = all_blacklists_dict
    """timer set stop to kill thread loop"""
    def init_ghetto_stop_blacklist_writer(self, stop_blacklist_writer):
        self.stop_blacklist_writer = stop_blacklist_writer
    """check box on or off, recorder use it to copy or not copy the files"""
    def init_ghetto_blacklist_enabled_global(self, blacklist_enabled_global):
        self.blacklist_enabled_global = blacklist_enabled_global
    """radio writes skipped titles, to show in blacklist html page"""
    def init_ghetto_skipped_in_session_dict(self, skipped_in_session_dict):
        self.skipped_in_session_dict = skipped_in_session_dict
    """alter the port number on startup wsgi.py or app.py alter the endpoint and push it to java"""
    def init_work_port(self, work_port):
        self.work_port = str(work_port)


api = Api()
ghettoApi = GhettoApi()
