import threading
import time

from eisenradio.api import ghettoApi


def start_watchdog_daemon():
    """
    call in eishome
    should never do any actions, only reporting
    """
    threading.Thread(name="watchdog", target=run_watchdog, daemon=True).start()


def run_watchdog():

    while not ghettoApi.stop_blacklist_writer:
        # [print(f' {thread.name}') for thread in threading.enumerate()]

        # print(f'\n\tblacklist_enabled {ghettoApi.blacklist_enabled_global}\n')

        # [print(f'header: {key}: {value}') for key, value in ghettoApi.ghetto_measure_dict.items()]

        # for radio_name, blacklist in ghettoApi.all_blacklists_dict.items():
        #     print('\n')
        #     [print(f'bl: {radio_name[:3]}: {index} {value}') for index, value in enumerate(blacklist)]

        # [print(f'title_new: {key}: {value}') for key, value in ghettoApi.recorder_new_title_dict.items()]

        for _ in range(30):
            if ghettoApi.stop_blacklist_writer:
                break
            time.sleep(1)
