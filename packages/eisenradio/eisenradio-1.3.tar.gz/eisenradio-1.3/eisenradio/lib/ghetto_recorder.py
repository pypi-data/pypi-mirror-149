# 0.1.2a
##################################################################################
#   MIT License
#
#   Copyright (c) [2021] [René Horn]
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
###################################################################################
import io
import os
import queue
import shutil
import threading
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from time import sleep, strftime, time
from urllib.error import URLError, HTTPError

import urllib3
from eisenradio.api import ghettoApi

# logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
# logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

version = '2.0'
print(f'ghettorecorder {version} (eisen_radio module)')  # ########## version #############


class GBase:
    # class attribute
    dict_exit = {}  # all "single" started (this time four, each station)
    dict_error = {}
    ghettoApi.init_ghetto_dict_error(dict_error)
    sleeper = 2  # for exit of all threads
    pool = ThreadPoolExecutor(200)
    radio_base_dir = os.path.dirname(os.path.abspath(__file__)) + '//radiostations'  # if not set set_radio_base_dir()
    settings_path = os.path.dirname(os.path.abspath(__file__)) + '//settings.ini'  # if not set in set_settings_path()
    path = os.getcwd()
    path_to = path + '//'
    timer = 0

    def __init__(self, radio_base_dir=None, settings_path=None):
        self.instance_attr_time = 0
        self.trigger = False
        self.radio_base_dir = radio_base_dir
        self.settings_path = settings_path

    @staticmethod
    def make_directory(str_path):
        try:
            os.mkdir(str_path)
        except FileExistsError:
            pass
        else:
            print('\t--> created directory: ' + str_path)

    @staticmethod
    def remove_special_chars(str_name):
        ret_value = str_name.translate({ord(string): "" for string in '"!@#$%^*()[]{};:,./<>?\|`~=+"""'})
        return ret_value

    @staticmethod
    def this_time():
        time_val = strftime("_%Y_%m_%d_%H.%M.%S")
        return time_val

    def countdown(self, instance_attr_time):
        t = 0
        while not t == instance_attr_time:
            sleep(1)
            self.timer = t
            print(self.timer)
            t += 1
            if t == 0:
                self.trigger = True
        print(f' done {instance_attr_time} {self.trigger}')
        return self.trigger


class GIni(GBase):  # remnant of command line version

    content_type = {}  # header info audio/mpeg

    @staticmethod
    def parse_url_simple_url(radio_url):
        url = radio_url  # whole url is used for connection to radio server

        # 'http:' is first [0], 'ip:port/xxx/yyy' second item [1] in list_url_protocol
        list_url_protocol = url.split("//")
        list_url_ip_port = list_url_protocol[1].split("/")  # 'ip:port' is first item in list_url_ip_port
        radio_simple_url = list_url_protocol[0] + '//' + list_url_ip_port[0]
        return radio_simple_url


class GNet(GBase):
    http_pool = urllib3.PoolManager(num_pools=20)

    @staticmethod
    def load_url(url):
        # returns status code, if server is alive conn.getcode()
        # use urllib, urllib3 causes response to wait "forever" and timeout is not working either
        # print(f' load_url {url}')
        with urllib.request.urlopen(url, timeout=15) as response:
            return response.getcode()

    @staticmethod
    def is_server_alive(url, str_radio):
        # don't delete - urllib3 timeout=5, placebo, retries=None or =2, screw yourself, since half of conn. die
        # we have server up, but content not presented - zombie
        try:
            GNet.load_url(url)
        except HTTPError as error:
            print(f' ---> {str_radio} server failed: {error} , {url}')
            GBase.dict_error[str_radio] = f'{str_radio} radio: {error} {url}'
            return True
        except URLError as error:  # <urlopen error timed out>
            print(f' ---> {str_radio} server failed: {error} , {url}')
            GBase.dict_error[str_radio] = f'{str_radio} radio: {error} {url}'
            return False
        except Exception as error:
            print(f' ---> {str_radio} server exception: {error} , {url}')
            GBase.dict_error[str_radio] = f'{str_radio} radio: {error} {url}'
            return False
        return True

    @staticmethod
    def stream_filetype_url(url, str_radio):
        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                headers = response.getheader('Content-Type')
        except Exception as ex:
            print(ex)
            return False

        content_type = ''
        if headers == 'audio/aacp' or headers == 'application/aacp':
            content_type = '.aacp'
        if headers == 'audio/aac':
            content_type = '.aac'
        if headers == 'audio/ogg' or headers == 'application/ogg':
            content_type = '.ogg'
        if headers == 'audio/mpeg':
            content_type = '.mp3'
        if headers == 'audio/x-mpegurl' or headers == 'text/html':
            content_type = '.m3u'
        # application/x-winamp-playlist , audio/scpls , audio/x-scpls ,  audio/x-mpegurl

        try:
            GIni.content_type[str_radio] = headers
            if len(headers) <= 5:
                GIni.content_type[str_radio] = 'audio/mpeg'
            # print(f' stream_filetype_url: {GIni.content_type[str_radio]}')
        except Exception as e:
            print(e)
            pass

        return content_type


class GRecorder:
    path_record_dict = {}  # {station : file path}
    current_song_dict = {}  # each thread writes the new title to the station key name {station : title}
    ghettoApi.init_ghetto_radios_metadata_text(current_song_dict)
    start_write_command = {}  # recorder head thread set command to copy first file
    record_active_dict = {}
    listen_active_dict = {}
    ghettoApi.init_ghetto_listen_active_dict(listen_active_dict)
    ghetto_measure = {}
    ghettoApi.init_ghetto_measurements(ghetto_measure)
    audio_stream_queue_dict = {}
    ghettoApi.init_ghetto_audio_stream(audio_stream_queue_dict)
    recorder_new_title_dict = {}
    ghettoApi.init_ghetto_recorder_new_title(recorder_new_title_dict)
    skipped_in_session_dict = {}
    ghettoApi.init_ghetto_skipped_in_session_dict(skipped_in_session_dict)

    @staticmethod
    def ghetto_recorder_head(directory_save, stream_suffix, str_radio, str_action):
        """create file name from current meta for recorder"""
        if str_action == "listen":
            return

        sleep(3)  # chance to get stream meta info
        first_record = True

        display_info = ""
        while GRecorder.record_active_dict[str_radio] or not GBase.dict_exit[str_radio]:
            stream_info = GRecorder.current_song_dict[str_radio]  # unknown_title, None, icy metadata if avail

            if not display_info == stream_info:
                if not stream_info == "":
                    display_info = stream_info
                    stripped_info = GBase.remove_special_chars(stream_info)

                    if first_record:
                        fresh_file_path = directory_save + '//' + '_incomplete_' + stripped_info + stream_suffix
                        GRecorder.path_record_dict[str_radio] = fresh_file_path
                        GRecorder.start_write_command[str_radio] = True
                        first_record = False
                    else:
                        fresh_file_path = directory_save + '//' + stripped_info + stream_suffix
                        GRecorder.path_record_dict[str_radio] = fresh_file_path  # NEW PATH ... ... ...

            if not GRecorder.record_active_dict[str_radio] or GBase.dict_exit[str_radio]:
                stripped_info = GBase.remove_special_chars(stream_info)
                fresh_file_path = directory_save + '//' + '_incomplete_' + stripped_info + stream_suffix
                GRecorder.path_record_dict[str_radio] = fresh_file_path
                break
            sleep(1)

    @staticmethod
    def g_recorder_make_dir(path_to_save, str_radio):
        try:
            GBase.make_directory(path_to_save)
            return True
        except FileNotFoundError:
            GRecorder.current_song_dict[str_radio] = '[{-_-}] ZZZzz zz z... Recorder Failure!'
            GBase.dict_exit[str_radio] = True  # all str_radio treads-will-stop
            print('\t---> Recorder Write Failure in : ' + path_to_save)
            return False

    @staticmethod
    def g_recorder_await_head(str_radio):
        while not GBase.dict_exit[str_radio]:
            try:
                if GRecorder.start_write_command[str_radio]:
                    break
            except KeyError:
                pass
            else:
                sleep(.1)

    @staticmethod
    def g_recorder_path_transfer_test(str_radio):
        try:
            file_path = GRecorder.path_record_dict[str_radio]
            return file_path
        except KeyError:
            GRecorder.current_song_dict[str_radio] = '[{-_-}] ZZZzz zz z... Recorder Failure!'
            GBase.dict_exit[str_radio] = True  # all str_radio threads stop, major problem
            return False

    @staticmethod
    def g_recorder_request(url):
        # url was tested in Gnet
        try:
            request = GNet.http_pool.request('GET', url,
                                             headers={'Connection': 'keep-alive'},
                                             timeout=3000,
                                             preload_content=False)
            return request
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def g_recorder_cache_the_file(str_radio, full_file_path, record_file, ghetto_recorder, stream_request_size):
        # extract title from path and write to "recorder_new_title_dict"
        title = GRecorder.g_recorder_record_trace(str_radio, full_file_path)
        if ghettoApi.blacklist_enabled_global:
            if title not in ghettoApi.all_blacklists_dict[str_radio]:
                GRecorder.g_recorder_remove_file(full_file_path, record_file)
                GRecorder.g_recorder_copy_file(full_file_path, ghetto_recorder, stream_request_size)
                print(f'\n-WRITE->>> {str_radio}: {title}\n')
            else:
                print(f'\n-SKIP->>> {str_radio}: {title}\n')
                GRecorder.skipped_in_session_dict[str_radio].append(title)
        else:
            GRecorder.g_recorder_remove_file(full_file_path, record_file)
            GRecorder.g_recorder_copy_file(full_file_path, ghetto_recorder, stream_request_size)
            print(f'\n-write--> {str_radio}: {title}\n')

    @staticmethod
    def g_recorder_reset_file_offset(record_file):
        record_file.seek(0)
        record_file.truncate()

    @staticmethod
    def g_recorder_copy_file(full_file_path, ghetto_recorder, stream_request_size):
        ghetto_size = os.path.getsize(ghetto_recorder)
        if int(ghetto_size) >= int(stream_request_size):
            try:
                shutil.copyfile(ghetto_recorder, full_file_path)
            except Exception as error:
                message = f' Exception in g_recorder_copy_file; error: {error}'
                print(message)
        else:
            print('Skip file - size is too small.')

    @staticmethod
    def g_recorder_remove_file(full_file_path, record_file):
        if os.path.exists(full_file_path):
            os.remove(full_file_path)
        record_file.flush()

    @staticmethod
    def g_recorder_record_trace(str_radio, full_file_path):
        """
        extract the cleaned file name (in head) from path string, add to recorder_new_title_dict
        """
        head, tail = os.path.split(full_file_path)
        title = ""
        try:
            tail_list = tail.split('.')
            title = tail_list[0]
        except Exception as error:
            message = f' Exception in g_recorder_record_trace; error: {error}'
            print(message)

        GRecorder.recorder_new_title_dict[str_radio] = title
        return title

    @staticmethod
    def g_recorder_teardown(str_radio, record_file, ghetto_recorder, stream_request_size):
        try:
            sleep(5)
            file_size = os.path.getsize(ghetto_recorder)
            if int(file_size) >= int(stream_request_size):
                awaited_head_incomplete_tag = GRecorder.path_record_dict[str_radio]
                shutil.copyfile(ghetto_recorder, awaited_head_incomplete_tag)

            record_file.seek(0)
            record_file.truncate()
            record_file.flush()
            record_file.close()

            if os.path.exists(ghetto_recorder):
                os.remove(ghetto_recorder)
        except OSError as ex:
            print(ex)

    @staticmethod
    def g_recorder_empty_queue(str_radio):
        """try to not feed Html audio element, it will switch faster"""
        while not GRecorder.audio_stream_queue_dict[str_radio + ',audio'].empty():
            GRecorder.audio_stream_queue_dict[str_radio + ',audio'].get()

    @staticmethod
    def g_recorder_write_queue(str_radio, chunk):
        if not GRecorder.audio_stream_queue_dict[str_radio + ',audio'].full():
            GRecorder.audio_stream_queue_dict[str_radio + ',audio'].put(chunk)

    @staticmethod
    def g_recorder_ask_bit_rate(url):
        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                bit_rate = response.getheader('icy-br')
                try:
                    if int(bit_rate) % 1 == 0:
                        return bit_rate
                except ValueError:
                    # got server with '128, 128' and 64, 64 http://live02.rfi.fr/rfienvietnamien-64.mp3
                    print(f'g_recorder_ask_bit_rate ValueError: {bit_rate} {url}')
                    try:
                        bit_rate_list = bit_rate.split(',')
                        this_rate = bit_rate_list[0].strip()
                        if int(this_rate) % 1 == 0:
                            print(f'g_recorder_ask_bit_rate use: {this_rate} for {url}')
                            return this_rate
                    except Exception as error:
                        message = f'use fallback rate 320, error {error}'
                        print(message)
                        return 320
        except Exception as ex:
            print(ex)
            return 320

    @staticmethod
    def g_recorder_calc_chunk_size(url):
        """avoid digital noise, delays and connection breaks"""
        stream_chunk_size = io.DEFAULT_BUFFER_SIZE * 4  # 8KB * x; HQ audio 320kB/s
        if GRecorder.g_recorder_ask_bit_rate(url):
            bit_rate = int(GRecorder.g_recorder_ask_bit_rate(url))
            if bit_rate <= 80:
                stream_chunk_size = io.DEFAULT_BUFFER_SIZE
            if (bit_rate > 80) and (bit_rate <= 160):
                stream_chunk_size = io.DEFAULT_BUFFER_SIZE * 2
            if (bit_rate > 160) and (bit_rate <= 240):
                stream_chunk_size = io.DEFAULT_BUFFER_SIZE * 3
        return stream_chunk_size

    @staticmethod
    def g_recorder_rec(request, str_radio, ghetto_recorder, stream_chunk_size, full_file_path, suffix):
        """
        rec loop
        start with correct path
        must recognize change in metadata to work on header and tail of datastructure is cut out of the stream
        """
        with open(ghetto_recorder, 'wb') as record_file:
            for chunk in request.stream(stream_chunk_size):

                if not full_file_path == GRecorder.path_record_dict[str_radio]:
                    # new file path found
                    GRecorder.record_write_last(chunk, record_file, suffix)
                    GRecorder.g_recorder_cache_the_file(str_radio,
                                                        full_file_path,
                                                        record_file,
                                                        ghetto_recorder,
                                                        stream_chunk_size)
                    GRecorder.g_recorder_reset_file_offset(record_file)
                    GRecorder.record_write_first(chunk, record_file, suffix)
                    full_file_path = GRecorder.path_record_dict[str_radio]
                else:
                    # fill a current file, write chunk
                    record_file.write(chunk)

                if not GRecorder.record_active_dict[str_radio] or GBase.dict_exit[str_radio]:  # timer dict_exit
                    GRecorder.g_recorder_teardown(str_radio, record_file, ghetto_recorder, stream_chunk_size)
                    request.release_conn()
                    break

    @staticmethod
    def record_write_first(chunk, record_file, suffix):
        if suffix == ".aacp":
            acp_header = GRecorder.record_acp_fff1_sync_word_header(chunk)
            if acp_header is not None:
                record_file.write(acp_header)
        else:
            # ('write first chunk of new file')
            record_file.write(chunk)

    @staticmethod
    def record_write_last(chunk, record_file, suffix):
        if suffix == ".aacp":
            # ('write cleaned file tail')
            acp_tail = GRecorder.record_acp_fff1_sync_word_tail(chunk)
            if acp_tail is not None:
                record_file.write(acp_tail)
        else:
            # ('last normal chunk of current file')
            record_file.write(chunk)

    @staticmethod
    def record_acp_fff1_sync_word_tail(chunk):
        """
        clean cut at the end, cut out the last bytes starting with ff f1 (if not, result is a defective payload),
        so browser do not stop with silent error and will play next file
        start is -1, so loose one byte, but can not start with None or 0 for variable "start" in this setup
        can reverse chunk and start from 0, but for ONE byte drowning in the sea of useless information ...
        """
        hex_chunk = chunk.hex()
        start, end = -1, -5
        search_string = "fff1"
        while 1:
            if end < -(len(hex_chunk)):
                break
            if hex_chunk[end:start] == search_string:
                # return bytes before end variable
                return bytes.fromhex(hex_chunk[:end])
            start -= 1
            end -= 1
        return

    @staticmethod
    def record_acp_fff1_sync_word_header(chunk):
        """
        cut files out of the stream on metadata change, so the end of a file is not likely the correct start for new
        search aacp (acp plus) frame start sequence to clean the file so browser do not stop with silent error
        convert byte stream to hex, search ff f1 index_of_chunk[0] to index_of_chunk[3]
        shift the search frame in hex to right, cut out and return as bytes
        """
        hex_chunk = chunk.hex()
        start, end = 0, 4
        search_string = "fff1"
        while 1:
            if end > len(hex_chunk):
                break
            if hex_chunk[start:end] == search_string:
                # return bytes slice from shifted start to the end of chunk
                return bytes.fromhex(hex_chunk[start:])
            start += 1
            end += 1
        return

    @staticmethod
    def ghetto_recorder_tail(url, str_radio, path_to_save, suffix, str_action):

        audio_stream_queue = queue.Queue(maxsize=10)  # maxsize for safety, normal one in use
        stream_chunk_size = GRecorder.g_recorder_calc_chunk_size(url)

        GRecorder.audio_stream_queue_dict[str_radio + ',audio'] = audio_stream_queue
        ghetto_recorder = os.path.join(path_to_save, '__ghetto_recorder' + str(suffix))
        request = GRecorder.g_recorder_request(url)

        if str_action == "record":
            GRecorder.g_recorder_await_head(str_radio)
            full_file_path = GRecorder.g_recorder_path_transfer_test(str_radio)
            if not full_file_path:
                print(f'{str_radio} Recorder can not get filepath')
                return
            if not GRecorder.g_recorder_make_dir(path_to_save, str_radio):
                print(f'{str_radio} Recorder can not create directory')
                return
            GRecorder.g_recorder_rec(request, str_radio, ghetto_recorder, stream_chunk_size, full_file_path, suffix)

        if str_action == "listen":
            for chunk in request.stream(stream_chunk_size):

                GRecorder.g_recorder_write_queue(str_radio, chunk)
                if not GRecorder.listen_active_dict[str_radio] or GBase.dict_exit[str_radio]:
                    GRecorder.g_recorder_empty_queue(str_radio)
                    request.release_conn()
                    break

    @staticmethod
    def metadata_header_info(request, str_radio, request_time):
        try:
            GRecorder.ghetto_measure[str_radio + ',request_time'] = request_time
        except KeyError:
            pass
        try:
            GRecorder.ghetto_measure[str_radio + ',suffix'] = request.headers['content-type']
        except KeyError:
            pass
        try:
            GRecorder.ghetto_measure[str_radio + ",icy_br"] = request.headers["icy-br"]
        except KeyError:
            pass
        try:
            GRecorder.ghetto_measure[str_radio + ",icy_name"] = request.headers["icy-name"]
        except KeyError:
            pass
        try:
            GRecorder.ghetto_measure[str_radio + ",icy_genre"] = request.headers["icy-genre"]
        except KeyError:
            pass
        try:
            GRecorder.ghetto_measure[str_radio + ",icy_url"] = request.headers["icy-url"]
        except KeyError:
            pass

    @staticmethod
    def metadata_icy_info(request, str_radio):
        try:
            icy_meta_int = int(request.headers['icy-metaint'])
            request.read(icy_meta_int)
            start_byte = request.read(1)
            start_int = ord(start_byte)
            num_of_bytes = start_int * 16
            metadata_content = request.read(num_of_bytes)
            return metadata_content
        except Exception as error:
            message = f'metadata_icy_info(), {str_radio}: no or false metadata; {error}'
            print(message)
            return False

    @staticmethod
    def metadata_request(url):

        request = GNet.http_pool.request('GET', url,
                                         headers={'Icy-MetaData': '1'},
                                         preload_content=False)
        return request

    @staticmethod
    def metadata_get_display_extract(icy_info):
        # StreamTitle='X-Dream - Panic In Paradise * anima.sknt.ru';StreamUrl='';
        try:
            title_list = icy_info.split(";")
            if not len(title_list) > 1 or title_list is None:
                return  # empty list
            title_list = title_list[0].split("=")
            title = str(title_list[1])
            title = GBase.remove_special_chars(title)
            if title is not None:
                return title
        except IndexError:
            pass
        except OSError:
            pass
        return

    @staticmethod
    def metadata_get_display_info(icy_info):
        # <class 'bytes'> decode to <class 'str'> actually b''
        try:
            title = GRecorder.metadata_get_display_extract(icy_info.decode('utf-8'))
            if not title:
                return
            if title:
                return title
        except AttributeError:
            """AttributeError: Server sends no metadata; bool value instead"""
            return
        except Exception as error:
            print(f' Exception in metadata_get_display_info: {error}')
            return

    @staticmethod
    def get_metadata_from_stream_loop(url, str_radio, str_action):
        stop_while = False
        icy_info = ''
        while 1:
            try:
                start_time = time()
                response = GRecorder.metadata_request(url)
                request_time = round((time() - start_time) * 1000)
                GRecorder.metadata_header_info(response, str_radio, request_time)
                icy_info = GRecorder.metadata_icy_info(response, str_radio)
                response.release_conn()  # preload_content=False
            except HTTPError:
                pass
            except URLError:
                """url was checked in is_server_alive. assume short conn error"""
                pass
            except Exception as error:
                print(f' ---> get_metadata_from_stream_loop {str_radio}, exception info: {error} , {url}')
                pass

            title = GRecorder.metadata_get_display_info(icy_info)
            if title:
                try:
                    if title[0] == "'" and title[-1] == "'":
                        GRecorder.current_song_dict[str_radio] = title[1:-1]  # |sequence, ex 0 and last char |0 |1 |²2
                    else:
                        GRecorder.current_song_dict[str_radio] = title
                except KeyError:
                    pass
                except Exception as error:
                    print(f' ---> metadata_get_display_info {str_radio}, exception info: {error} , {url}')
                    pass

            for sec in range(2):
                if str_action == "listen":
                    if GBase.dict_exit[str_radio] or not GRecorder.listen_active_dict[str_radio]:
                        stop_while = True
                        break
                if str_action == "record":
                    if GBase.dict_exit[str_radio] or not GRecorder.record_active_dict[str_radio]:
                        stop_while = True
                        break
                sleep(1)
            if stop_while:
                GRecorder.current_song_dict[str_radio] = ""
                break

    @staticmethod
    def playlist_m3u(url, str_radio):
        # returns the first server of the playlist (not only m3u)
        try:
            read_url = GNet.http_pool.request('GET', url, preload_content=False)
        except Exception as ex:
            print(ex)
        else:
            file = read_url.read().decode('utf-8')

            m3u_lines = file.split("\n")
            # print(' \n    m3u_lines    ' + file)
            m3u_lines = list(filter(None, m3u_lines))  # remove empty rows
            m3u_streams = []
            for row_url in m3u_lines:
                if row_url[0:4].lower() == 'http'.lower():
                    m3u_streams.append(row_url)  # not to lower :)
                    # print(len(m3u_streams))

            if len(m3u_streams) > 1:
                print(f' {str_radio} Have more than one server in playlist_m3u. !!! Take first stream available.')
                play_server = m3u_streams[0]
                return play_server
            if len(m3u_streams) == 1:
                # print(' One server found in playlist_m3u')
                play_server = m3u_streams[0]
                return play_server
            if len(m3u_streams) == 0:
                # print(' No http ... server found in playlist_m3u !!! -EXIT-')
                return False


def check_alive_playlist_container(str_radio, str_url):
    # playlist url?
    # https://streams.br.de/bayern1obb_2.m3u
    if str_url[-4:] == '.m3u' or str_url[-4:] == '.pls':  # or url[-5:] == '.m3u8' or url[-5:] == '.xspf':
        # take first from the list
        is_playlist_server = GRecorder.playlist_m3u(str_url, str_radio)

        if not is_playlist_server == '':
            if GNet.is_server_alive(str_url, str_radio):
                str_url = is_playlist_server
            else:
                print('   --> playlist_server server failed, no recording')
            return str_url
    else:
        GNet.is_server_alive(str_url, str_radio)
        return False


def record_start_radio(str_radio, url, stream_suffix, dir_save, str_action):
    threading.Thread(name=str_radio + '_' + str_action + "_head", target=GRecorder.ghetto_recorder_head,
                     args=(dir_save, stream_suffix, str_radio, str_action),
                     daemon=True).start()
    threading.Thread(name=str_radio + '_' + str_action + "_tail", target=GRecorder.ghetto_recorder_tail,
                     args=(url, str_radio, dir_save, stream_suffix, str_action),
                     daemon=True).start()
    threading.Thread(name=str_radio + '_' + str_action + "_meta", target=GRecorder.get_metadata_from_stream_loop,
                     args=(url, str_radio, str_action),
                     daemon=True).start()


def record(str_radio, url, str_action):
    stream_suffix = GNet.stream_filetype_url(url, str_radio)
    if str_action == "record":
        GRecorder.current_song_dict[str_radio] = 'unknown_title' + GBase.this_time()
        GRecorder.start_write_command[str_radio] = False
        GRecorder.skipped_in_session_dict[str_radio] = []
    if str_action == "listen":
        GRecorder.current_song_dict[str_radio] = ""

    GBase.dict_exit[str_radio] = False
    dir_save = os.path.join(GBase.radio_base_dir, str_radio)  # overwritten in eishome.set_radio_path()
    record_start_radio(str_radio, url, stream_suffix, dir_save, str_action)

    # ################################## end ########################################
    # this version ends here. no loop
