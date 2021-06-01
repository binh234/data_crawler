# ***Zingmp3***
***Zingmp3 - A tool crawl data from [`zingmp3.vn`](https://zingmp3.vn/).***

```
$ python zingmp3.py -h
usage: zingmp3.py [-h] [-c] [-s] [-j] [-l] [--add-index] url

Zingmp3 - A tool crawl data from zingmp3.vn

positional arguments:
  url             Url.

optional arguments:
  -h, --help            show this help message and exit

Options:
  -s, --save            Save media files
  -o OUTPUT_PATH, --output OUTPUT_PATH
                        Download directory to save media files
  -i, --info            Save info media.
  -l, --lyric           Download media lyric.
  --log LOG_PATH        Path to save log file (csv, json, excel supported)
  --add-index           Add index for crawled media.
```


## ***Installation***
- **Language**: Python3.x

- **Module**: requests, colorama
  ```
  pip install -r requirements.txt
  ``` 

## ***Options***
- ***`-s` or `--save` : Path to save file downloaded.***
- ***`-i` or `--info` : Save info media.***
- ***`-l` or `--lyric` : Download with lyric.***
- ***`--log` : Convert the audio output to .mp3.***
- ***`--add-index` : Add index of playlist for title.***
- ***Default will get all download links for media.***
- ***All the example in Usage.***
 
## ***All URL Supported***
- ***url media***
  ```
  https://zingmp3.vn/video-clip/.../<id>.html
  https://zingmp3.vn/bai-hat/.../<id>.html
  https://zingmp3.vn/playlist/.../<id>.html
  https://zingmp3.vn/album/.../<id>.html
  https://zingmp3.vn/embed/.../<id>.html
  https://zingmp3.vn/the-loai-video/<slug>/<id>.html
  https://zingmp3.vn/the-loai-album/<slug>/<id>.html
  ```
- ***url artist's profile type 1***
  ```
  https://zingmp3.vn/nghe-si/<name_artist>/video
  https://zingmp3.vn/nghe-si/<name_artist>/playlist
  https://zingmp3.vn/nghe-si/<name_artist>/bai-hat
  https://zingmp3.vn/nghe-si/<name_artist>/album
  ```
- ***url artist's profile type 2***
  ```
  https://zingmp3.vn/<name_artist>/bai-hat
  https://zingmp3.vn/<name_artist>/playlist
  https://zingmp3.vn/<name_artist>/video
  https://zingmp3.vn/<name_artist>/album
  ```
- ***url #ZINGCHART***
  ```
  https://zingmp3.vn/zing-chart/bai-hat.html
  https://zingmp3.vn/zing-chart/video.html
  https://zingmp3.vn/zing-chart-tuan/bai-hat-Viet-Nam/<id>.html
  https://zingmp3.vn/zing-chart-tuan/video-US-UK/<id>.html
  ```
- ***url new release***
  ```
  https://zingmp3.vn/moi-phat-hanh
  ```

## ***Usage***

- ***Install module***
  ```
  pip install -r requirements.txt
  ```

- ***Run***
  ```
  python zingmp3.py https://zingmp3.vn/bai-hat/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html
  ```

- ***Download and save media file***

  ```
  python zingmp3.py -s https://zingmp3.vn/bai-hat/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html
  ```

- ***Save info media***
    ```
    python zingmp3.py -i https://zingmp3.vn/bai-hat/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html
    ```