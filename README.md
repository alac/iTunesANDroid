iTunesANDroid
=================

Purpose
-----------------
- Export iTunes playlists to an Android device as m3u8 playlist files (usable with Poweramp).
- Sync only new or changed audio files to an Android device.

Requirements
-----------------
- Windows
- Python 2, Python 3 and the "py" utility (for switching between versions).
- Android Debug Bridge

Setup
-----------------
- Enable Android USB debugging and install `ADB` via the [setup steps here](https://github.com/google/adb-sync#setup).
- Install Python 2, Python 3 and the "py". [Link](https://www.python.org/downloads/windows/)
- Make sure the folders containing `adb` and `py` are available via your path. [Guide](http://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10)


Usage
-----------------
- Edit line 42 of [iTunesAndroidDriver.py](https://github.com/alac/iTunesANDroid/blob/master/iTunesAndroidDriver.py#L42) to be the location of your iTunes folder.
- Run iTunesAndroidDriver.py.
- Wait for it to finish!


Disclaimers
-----------------
- This project uses a heavily modified version of [adb-sync](https://github.com/google/adb-sync), which is under the Apache License.