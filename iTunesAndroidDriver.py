"""
iTunesAndroidDriver.py

One-way script for syncing iTunes music + playlists to an Android device.

Plan:
- scrape the iTunes XML -> m3u8 playlists
- use adb sync to sync music + m3u8 playlist files
"""

# Windows
import codecs
codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

import os, subprocess, time, sys

class ProcessTimer:
    def __init__(self):
        pass

    def start(self, message):
        self.start_ts = time.time()
        self.message = message
        print "<<<<", self.message, " starting"
        return self

    def finish(self):
        self.end_ts = time.time()
        print ">>>>", self.message, " | ", (self.end_ts - self.start_ts)
        return self

    def run(self, message, params):
        self.start(message)
        process = subprocess.Popen(
            params,
            shell=True
        )
        process.wait()
        self.finish()

class Locations:
    iTunes_root_folder = "C:\Users\Alan\Dropbox\iTunes 3"
    iTunes_music_folder = os.path.join(iTunes_root_folder, "iTunes Media", "Music")
    iTunes_m3u8_Folder = os.path.join(iTunes_root_folder, "iTunes Media", "Playlists")
    iTunes_library_xml = os.path.join(iTunes_root_folder, "iTunes Library.xml")
    android_playlist_folder = "sdcard/Playlists"
    android_music_folder = "sdcard/Music"

if __name__ == "__main__":
    overall_timer = ProcessTimer()
    overall_timer.start("iTunesAndroidDriver")
    timer = ProcessTimer()

    if sys.platform == 'win32':
        if sys.stdout.encoding != 'cp65001':
            os.system("chcp 65001")

    timer.run(
        "iTunesXML -> m3u8 playlists",
        [
        'python',
        'm3u8_from_iTunes_xml.py',
        Locations.iTunes_library_xml,
        Locations.iTunes_m3u8_Folder,
        ]
    )

    timer.run(
        "playlists -> android",
        [
        'py',
        '-3',
        "adb-sync\\adb-sync",
        Locations.iTunes_m3u8_Folder,
        Locations.android_playlist_folder,
        ]
    )

    timer.run(
        "music -> android",
        [
        'py',
        '-3',
        "adb-sync\\adb-sync",
        "-d",
        Locations.iTunes_music_folder,
        Locations.android_music_folder,
        ]
    )

    overall_timer.finish()