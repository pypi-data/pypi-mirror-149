import eisenradio.eisenutil.request_info as request_info
from eisenradio.api import ghettoApi


def inactive_id_read():
    """
    return a list of all inactive radio ids to clean html page
    """
    active_id_list = request_info.active_buttons()
    radio_all_id_list = [radio_id for radio_id in ghettoApi.lis_btn_dict.keys()]
    inactive_id_list = [radio_id for radio_id in radio_all_id_list if radio_id not in active_id_list]
    return inactive_id_list
