from setup import *
import pandas as pd

_time = str(int(datetime.datetime.now().timestamp()))
_domain = "https://zingmp3.vn/"

class Zingmp3_vn(ProgressBar):
    LIST_TEST = '''
https://zingmp3.vn/Mr-Siro/bai-hat

https://zingmp3.vn/Mr-Siro/playlist

https://zingmp3.vn/Mr-Siro/video

https://zingmp3.vn/nghe-si/Huong-Giang-Idol/bai-hat

https://zingmp3.vn/nghe-si/Huong-Giang-Idol/video

https://zingmp3.vn/top-new-release/index.html

https://zingmp3.vn/zing-chart/bai-hat.html

https://zingmp3.vn/zing-chart-tuan/video-US-UK/IWZ9Z0BU.html

https://zingmp3.vn/zing-chart-tuan/bai-hat-US-UK/IWZ9Z0BW.html

https://zingmp3.vn/album/Khoc-Cung-Em-Single-Mr-Siro-Gray-Wind/ZF90UA9I.html

https://zingmp3.vn/playlist/Sofm-s-playlist/IWE606EA.html

https://zingmp3.vn/chu-de/Nhac-Hot/IWZ9Z0C8.html

https://zingmp3.vn/the-loai-video/Nhac-Tre/IWZ9Z088.html

https://zingmp3.vn/the-loai-album/Rap-Hip-Hop/IWZ9Z09B.html

https://zingmp3.vn/video-clip/Tim-Ve-Loi-Ru-New-Version-Thanh-Hung-Various-Artists/ZW6ZOIZ7.html

https://zingmp3.vn/video-clip/Yeu-Nhieu-Ghen-Nhieu-Thanh-Hung/ZWB087B9.html

https://zingmp3.vn/bai-hat/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html

https://zingmp3.vn/embed/song/ZWBW6WE8?start=false
'''

    _regex_url = r'''(?x)^
        ((?:http[s]?|fpt):)\/?\/(?:www\.|m\.|)
        (?P<site>
            (zingmp3\.vn)
        )\/(?P<type>(?:bai-hat|video-clip))\/(?P<slug>.*?)\/(?P<id>.*?)\W
        '''

    def __init__(self, *args, **kwargs):
        self._default_host = "https://zingmp3.vn/"
        self._headers = HEADERS
        self._save_media = kwargs.get('save_media', False)
        self._output_path = kwargs.get("output_path")
        self._show_json_info = kwargs.get("show_json_info")
        self._down_lyric = kwargs.get("down_lyric")
        self._add_index = kwargs.get('add_index')
        self._save_info = kwargs.get('save_info', False)
        self._log_path = kwargs.get('log_path')
        self._log_batch = 16
        self._columns = self.get_columns()
        self._df = pd.DataFrame(columns=self._columns)
        self.f = True
        self._item_count = 0

        if self._add_index:
            self._index_media = 1
        else:
            self._index_media = -1
    
    def get_columns(self):
        columns = ['ID', 'title', 'link', 'download_link', 'thumbnail', 'type']
        if self._save_info:
            columns.extend(['alias', 'artists', 'duration', 'release_date', 
            'mv_link', 'genres', 'like', 'listen', 'comment'])
        return columns

    def run(self, url):
        mobj = re.search(self._regex_url, url)
        if not mobj:
            return
        video_id = mobj.group('id')
        _type = mobj.group('type')
        slug = mobj.group('slug')
        return self.extract_info_media(_type, slug, video_id, url)

    def extract_info_media(self, _type, slug, video_id, url):
        sys.stdout.write("\n")
        name_api = ''
        if _type == 'bai-hat':
            name_api = '/api/v2/song/getDetail'
        elif _type == 'video-clip':
            name_api = "/api/v2/video/getDetail"

        api = self.get_api_with_signature(name_api=name_api, param={
            "ctime": _time,
            "id": video_id,
        })
        info = self.fr(api=api, note="Downloading json from %s" % video_id)
        
        if info.get('msg') == 'Success':
            data = info.get('data')
            
            # Extract data
            item_dict = self.extract_item_dict(data, _type)
            
            title = data.get('title')
            streaming = self.get_source(_id=video_id, _type=_type) or self.get_streaming(_id=video_id, _type=_type)
            lyric = ""
            if self._down_lyric:
                lyric = data.get('lyric') or try_get(data, lambda x: x['lyrics'][0]['content'],
                                                     str) or self.get_url_lyric(_id=video_id)
            
            if streaming:
                self.start_download(streaming=streaming, _type=_type, title=title, lyric=lyric, item_dict=item_dict)
            else:
                to_screen("Can not get download link for {}".format(video_id))
                self.log_item(item_dict)
        else:
            to_screen("Error can not find media data.")
    
    def extract_item_dict(self, data, type):
        item_dict = {}
        for column in self._columns:
            item_dict[column] = ""
        
        item_dict['ID'] = data.get("encodeId")
        item_dict['title'] = data.get("title")
        item_dict['link'] = urljoin(_domain, data.get("link"))
        item_dict['thumbnail'] = data.get("thumbnailM") or data.get("thumbnail")
        item_dict['type'] = "song" if type == "bai-hat" else "video"
        if self._save_info:
            item_dict['alias'] = data.get("alias")
            item_dict['artists'] = data.get("artistsNames")
            item_dict['duration'] = data.get("duration")
            timestamp = data.get("releaseDate") or data.get("createdAt")
            if timestamp:
                item_dict['release_date'] = str(datetime.datetime.fromtimestamp(int(timestamp)))
            if data.get("mvlink", "") != "":
                item_dict['mv_link'] = urljoin(_domain, data.get("mvlink"))
            item_dict['like'] = data.get("like", 0)
            item_dict['listen'] = data.get("listen", 0)
            item_dict['comment'] = data.get("comment", 0)
            item_dict['genres'] = ", ".join([genre.get("name") for genre in data.get("genres", [])])
        
        return item_dict

    def start_download(self, streaming, _type, title, lyric, item_dict):
        DirDownload = self._output_path
        if self._save_media and not os.path.exists(DirDownload):
            os.mkdir(DirDownload)

        def add_protocol(url):
            if not url.startswith("http"):
                return 'https:' + url
            return url

        def remove_p_quality(text):
            return search_regex(r'([0-9]+)', text)

        def get_lyric(lyric):
            if is_url(lyric):
                lyric = session.get(url=lyric, headers=self._headers).text
            if lyric:
                return lyric

        def down_lyric():
            if self._down_lyric:
                with open(os.path.join(DirDownload, "%s.lrc" % title), 'w', encoding='utf-8-sig') as f:
                    str_lyric = get_lyric(lyric)
                    if str_lyric:
                        f.write(str_lyric)
                        to_screen("Download lyric .... DONE.")
                    else:
                        to_screen("This media don't have lyric.")

        formats = []
        title = removeCharacter_filename(title)
        if self._index_media != -1:
            media_title = "%s - %s" % (self._index_media, title)
            self._index_media += 1
        else:
            media_title = title
        to_screen("Title : %s" % media_title)
        if _type == 'video-clip':
            for quality, url in streaming.items():
                if url:
                    if ".m3u8" in url:
                        formats.append({
                            "quality": remove_p_quality(quality),
                            "url": url,
                            "protocol": "hls",
                            'ext': "mp4"
                        })
                    else:
                        formats.append({
                            'url': add_protocol(url),
                            "quality": remove_p_quality(quality),
                            "protocol": "http",
                            "ext": "mp4"
                        })
            formats = sorted(formats, key=lambda x: (
                int(x['quality']),
                1 if x["protocol"] == "http" else 0
            ))
        else:
            for quality, url in streaming.items():
                if url != "" and url != "VIP":
                    if quality == 'lossless':
                        formats.append({
                            'url': add_protocol(url),
                            'ext': 'flac',
                            'protocol': 'http'
                        })
                    else:
                        formats.append({
                            'url': add_protocol(url),
                            'ext': 'mp3',
                            'protocol': 'http'
                        })
        will_down = formats[-1]
        protocol = will_down.get("protocol")
        _url = will_down.get('url')
        _ext = will_down.get("ext")
        item_dict['download_link'] = _url
        self.log_item(item_dict)
        if not self._save_media:
            return

        output_path = os.path.join(DirDownload, r"%s.%s" % (title, _ext))
        if not os.path.exists(output_path):
            if protocol == "http":
                down = Downloader(url=_url)
                down.download(
                    filepath=output_path,
                    callback=self.show_progress
                )
                time.sleep(1)
        else:
            to_screen("Already downloaded")

        down_lyric()

    def fr(self, api, params={}, note=""):
        if self.f:
            get_req(url=api, headers=self._headers)
            info = get_req(url=api, headers=self._headers, params=params, type='json', note=note)
            self.f = False
        else:
            info = get_req(url=api, headers=self._headers, params=params, type='json', note=note)
        return info

    def get_url_lyric(self, _id):
        api = self.get_api_with_signature(name_api="/api/v2/lyric", param={
            "ctime": _time,
            "id": _id,
        })
        res = self.fr(api=api)
        return try_get(res, lambda x: x["data"]["file"])

    def get_source(self, _id, _type):
        if _type == "video-clip":
            _api_video = """http://api.mp3.zing.vn/api/mobile/video/getvideoinfo?requestdata={"id":"%s"}"""
            _json_video = self.fr(api=_api_video % _id)
            time.sleep(2)
            return _json_video.get("source")
        return {
            "128": "https://api.mp3.zing.vn/api/streaming/song/{}/128".format(_id),
            "320": "https://api.mp3.zing.vn/api/streaming/song/{}/320".format(_id)
        }
    
    def get_streaming(self, _id, _type):
        if _type == "video-clip":
            _api_video = """http://api.mp3.zing.vn/api/mobile/video/getvideoinfo?requestdata={"id":"%s"}"""
            _json_video = self.fr(api=_api_video % _id)
            time.sleep(2)
            return _json_video.get("source")
        api = self.get_api_with_signature(name_api="/api/v2/song/getStreaming", param={
            "ctime": _time,
            "id": _id,
        })
        res = self.fr(api=api)
        if res.get("msg") != "Success":
            return None
        return res.get("data")

    def get_api_with_signature(self, name_api, param, another_param=None):
        API_KEY = 'kI44ARvPwaqL7v0KuDSM0rGORtdY1nnw'
        SECRET_KEY = b'882QcNXV4tUZbvAsjmFOHqNC1LpcBRKW'
        if not name_api:
            return

        def get_hash256(string):
            return hashlib.sha256(string.encode('utf-8')).hexdigest()

        def get_hmac512(string):
            return hmac.new(SECRET_KEY, string.encode('utf-8'), hashlib.sha512).hexdigest()

        url = f"https://zingmp3.vn{name_api}?"
        text = ""
        for k, v in param.items():
            text += f"{k}={v}"
        sha256 = get_hash256(text)
        data = {
            'ctime': param.get("ctime"),
            'apiKey': API_KEY,
            'sig': get_hmac512(r"%s%s" % (name_api, sha256))
        }
        data.update(param)
        if another_param:
            data.update(another_param)
        return url + urlencode(data)
    
    def log_item(self, item_dict):
        self._df = self._df.append(item_dict, ignore_index=True)
        self._item_count += 1
        if self._item_count % self._log_batch == 0:
            self.save_log()

    def save_log(self):
        extension = self._log_path.split('.')[-1]
        if extension == 'csv':
            self._df.to_csv(self._log_path, index=False)
        elif extension in ('xlsx', 'xls'):
            self._df.to_excel(self._log_path, index=False)
        elif extension == 'json':
            self._df.to_json(self._log_path, indent=4, orient='records')


class Zingmp3_vnPlaylist(Zingmp3_vn):
    _regex_playlist = r'''(?x)^
            ((?:http[s]?|fpt):)\/?\/(?:www\.|m\.|)
                (?P<site>
                    (zingmp3\.vn)
                )\/(?P<type>(?:album|playlist|the-loai-video|hub))\/(?P<slug>.*?)\/(?P<playlist_id>.*?)\W
                '''

    def __init__(self, *args, **kwargs):
        super(Zingmp3_vnPlaylist, self).__init__(*args, **kwargs)
        self.name_api_album_or_playlist = '/api/v2/playlist/getDetail'
        self.name_api_the_loai_video = "/api/v2/video/getList"
        self.name_api_hub = "/api/v2/hub/getDetail"

    def run_playlist(self, url):
        mobj = re.search(self._regex_playlist, url)
        _type = mobj.group('type')
        playlist_id = mobj.group('playlist_id')
        slug = mobj.group('slug')
        if _type == "the-loai-video":
            return self._entries_for_the_loai_video(id_the_loai_video=playlist_id, slug=slug)
        elif _type == "hub":
            return self._entries_for_hub(hub_id=playlist_id)
        return self._extract_playlist(id_playlist=playlist_id)

    def _entries_for_the_loai_video(self, id_the_loai_video, slug):
        to_screen("the-loai-video :  %s  %s" % (slug, id_the_loai_video))
        start = 1
        count = 30
        while True:
            api = self.get_api_with_signature(name_api=self.name_api_the_loai_video, param={
                "count": count,
                "ctime": _time,
                "id": id_the_loai_video,
                "page": start,
                "type": "genre"
            })
            info = self.fr(api=api)
            if info.get("msg").lower() != "success":
                break
            items = try_get(info, lambda x: x["data"]["items"], list) or []
            if not items:
                break
            for item in items:
                if not item:
                    continue
                url = urljoin(self._default_host, item.get("link"))
                if 'album' in url or 'playlist' in url:
                    self.run_playlist(url)
                else:
                    self.run(url)
            start += 1
            has_more = try_get(info, lambda x: x["data"]['hasMore'])

            if not has_more:
                break

    def _entries_for_hub(self, hub_id):
        api = self.get_api_with_signature(name_api=self.name_api_hub, param={
            "ctime": _time,
            "id": hub_id
        })
        info = self.fr(api=api)
        if info.get("msg").lower() != "success":
            to_screen("Can not find data, something was wrong, pls check url again.")
            return
        title_hub = try_get(info, lambda x: x["data"]["title"])
        to_screen(f"Hub : {title_hub}")
        items = try_get(info, lambda x: x["data"]["sections"][0]["items"]) or []
        for item in items:
            if not item:
                continue
            url = urljoin(self._default_host, item.get('link'))
            media_id = item.get('encodeId')
            if 'album' in url or 'playlist' in url:
                self._extract_playlist(media_id)

    def _extract_playlist(self, id_playlist):
        api = self.get_api_with_signature(name_api=self.name_api_album_or_playlist, param={
            "ctime": _time,
            "id": id_playlist
        })
        info = self.fr(api=api)
        title_playlist = try_get(info, lambda x: x['data']['title'], str) or ''
        items = try_get(info, lambda x: x['data']['song']['items'], list) or []
        to_screen(f"Playlist : {title_playlist}")
        for item in items:
            if not item:
                continue
            url = urljoin(self._default_host, item.get('link'))
            self.run(url)


class Zingmp3_vnChart(Zingmp3_vnPlaylist):
    _regex_chart = r'''(?x)^
            ((?:http[s]?|fpt):)\/?\/(?:www\.|m\.|)
            (?P<site>
                (zingmp3\.vn)
            )\/(?P<name>(?:zing-chart(\/|$)|zing-chart\/realtime|moi-phat-hanh(\/|$)|top100(\/|$)|zing-chart-tuan\/(?P<name_slug>.*?)\/(?P<id_name>.*?\.)))
            '''

    def __init__(self, *args, **kwargs):
        super(Zingmp3_vnChart, self).__init__(*args, **kwargs)

    def run_chart(self, url):
        mobj = re.search(self._regex_chart, url)
        name = mobj.group('name')
        if "zing-chart-tuan" in name:
            name_slug = mobj.group("name_slug")
            _id = mobj.group("id_name")
            return self._entries_zing_chart_tuan(name_slug, _id)
        elif "zing-chart" in name:
            return self._entries_zing_chart()
        elif "moi-phat-hanh" in name:
            return self._entries_moi_phat_hanh()
        elif "top100" in name:
            return self._entries_top100()

    def _entries_zing_chart(self):
        name_api = "/api/v2/chart/getRTChart"
        api = self.get_api_with_signature(name_api=name_api, param={
            "count": "100",
            "ctime": _time,
            "type": "song",
        })
        info = self.fr(api=api)
        items = try_get(info, lambda x: x["data"]["items"]) or []
        for item in items:
            if not item:
                continue
            url = urljoin(self._default_host, item.get('link'))
            if "bai-hat" in url:
                self.run(url)

    def _entries_moi_phat_hanh(self):
        name_api = "/api/v2/chart/getNewReleaseChart"
        api = self.get_api_with_signature(name_api=name_api, param={
            "ctime": _time
        })
        info = self.fr(api)
        items = try_get(info, lambda x: x["data"]["items"]) or []
        for item in items:
            if not item:
                continue
            url = urljoin(self._default_host, item.get('link'))
            if "bai-hat" in url:
                self.run(url)

    def _entries_top100(self):
        name_api = "/api/v2/top100"
        api = self.get_api_with_signature(name_api=name_api, param={
            "ctime": _time
        })
        info = self.fr(api)
        for data in info.get("data") or []:
            if not data:
                continue
            name = try_get(data, lambda x: x["genre"]["name"])
            to_screen(f"Name : {name}")
            items = data.get("items") or []
            for item in items:
                if not item:
                    continue
                url = urljoin(self._default_host, item.get('link'))
                if 'album' in url or 'playlist' in url:
                    self.run_playlist(url=url)

    def _entries_zing_chart_tuan(self, name_slug, _id):
        name_api = "/api/v2/chart/getWeekChart"
        to_screen(f"Zing chart tuan : {name_slug}")
        api = self.get_api_with_signature(name_api=name_api, param={
            "ctime": _time,
            "id": _id
        })
        info = self.fr(api)
        items = try_get(info, lambda x: x["data"]["items"]) or []
        for item in items:
            if not item:
                continue
            url = urljoin(self._default_host, item.get('link'))
            if "bai-hat" in url:
                self.run(url)


class Zingmp3_vnUser(Zingmp3_vnPlaylist):
    _regex_user = r'''(?x)^
        ((?:http[s]?|fpt):)\/?\/(?:www\.|m\.|)
        (?P<site>
            (zingmp3\.vn)
        )\/(?P<nghe_si>(?!bai-hat|video-clip|embed|album|playlist|chu-de|zing-chart|top-new-release|zing-chart-tuan|the-loai-video|the-loai-album)(?:nghe-si\/|))(?P<name>.*?)
        (?:$|\/)
        (?P<slug_name>(?:bai-hat|video|))$
            '''

    def __init__(self, *args, **kwargs):
        super(Zingmp3_vnUser, self).__init__(*args, **kwargs)
        self.list_name_api_user = {
            'bai-hat': "/api/v2/song/getList",
            "video": "/api/v2/video/getList",
        }

    def run_user(self, url):
        mobj = re.search(self._regex_user, url)
        name = mobj.group('name')
        slug_name = mobj.group('slug_name') or "bai-hat"
        name_api = self.list_name_api_user.get(slug_name) or None
        self.id_artist = None
        to_screen(f'{name} - {slug_name}')
        api = self.get_api_with_signature(name_api="/api/v2/artist/getDetail", param={
            "ctime": _time
        }, another_param={
            "alias": name
        })
        info = self.fr(api=api)
        if info.get('msg') == 'Success':
            self.id_artist = try_get(info, lambda x: x['data']['id'], str) or None
        if self.id_artist:
            return self._entries(name_api)

    def _entries(self, name_api):
        start = 1
        count = 30
        while True:
            api = self.get_api_with_signature(name_api=name_api, param={
                "count": count,
                "ctime": _time,
                "id": self.id_artist,
                "page": start,
                "type": "artist",
            }, another_param={
                "sort": "new"
            })
            info = self.fr(api=api)
            if info.get('msg').lower() != "success":
                break
            items = try_get(info, lambda x: x['data']['items'], list) or []
            if not items:
                break
            for item in items:
                if not item:
                    continue
                url = urljoin(self._default_host, item.get('link'))
                if 'album' in url or 'playlist' in url:
                    self.run_playlist(url)
                else:
                    self.run(url)
            start += 1
            has_more = try_get(info, lambda x: x["data"]['hasMore'])

            if not has_more:
                break


class ZingCrawler:
    def __init__(self, *args, **kwargs):
        
        url = kwargs.get("url")

        if "mp3.zing.vn" in url.lower():
            url = url.replace("mp3.zing.vn", "zingmp3.vn")

        if re.match(Zingmp3_vn._regex_url, url):
            tm = Zingmp3_vn(*args, **kwargs)
            tm.run(url)
        elif re.match(Zingmp3_vnPlaylist._regex_playlist, url):
            tm = Zingmp3_vnPlaylist(*args, **kwargs)
            tm.run_playlist(url)
        elif re.match(Zingmp3_vnChart._regex_chart, url):
            tm = Zingmp3_vnChart(*args, **kwargs)
            tm.run_chart(url)
        elif re.match(Zingmp3_vnUser._regex_user, url):
            tm = Zingmp3_vnUser(*args, **kwargs)
            tm.run_user(url)
        else:
            to_screen("URL not supported", status="error")
            return
        
        tm.save_log()