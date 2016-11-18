import os
import plistlib
import urllib
from iTunes_library import iTunesTrack, iTunesPlaylist, iTunesLibrary

# Windows
import codecs
codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)


class iTunesXMLKeys:
    app_version = "Application Version"
    date = "Date"
    features = "Features"
    library_id = "Library Persistent ID"
    major_version = "Major Version"
    minor_version = "Minor Version"
    music_folder = "Music Folder"
    playlists = "Playlists"
    show_content_ratings = "Show Content Ratings"
    tracks = "Tracks"


class PlaylistXMLKeys:
    name = "Name"
    all_items = "All Items"
    persistent_id = 'Playlist Persistent ID'
    items = "Playlist Items"
    visible = "Visible"
    master = "Master"
    playlist_id = "Playlist ID"
    playlist_items = "Playlist Items"
    distinguished_kind = "Distinguished Kind"
    smart_info = "Smart Info"


class PlaylistItemXMLKeys:
    track_id = "Track ID"


class TrackXMLKeys:
    album = "Album"
    persistent_id = "Persistent ID"
    # int
    track_number = "Track Number"
    album_artist = "Album Artist"
    track_type = "Track Type"
    # int
    file_folder_count = "File Folder Count"
    sort_artist = "Sort Artist"
    # int
    duration_ms = "Total Time"
    artist = "Artist"
    # int
    track_count = "Track Count"
    # int
    bit_rate = "Bit Rate"
    kind = "Kind"
    title = "Name"
    # int
    sample_rate = "Sample Rate"
    sort_album_artist = "Sort Album Artist"
    # int
    track_id = "Track ID"
    artwork_count = "Artwork Count"
    location = "Location"
    # datetime
    date_modified = "Date Modified"
    library_folder_count = "Library Folder Count"
    year = "Year"
    # datetime
    date_added = "Date Added"
    size_bytes = "Size"


def playlist_from_xml_obj(xml_obj):
    name = xml_obj[PlaylistXMLKeys.name]

    playlist_items = xml_obj.get(PlaylistXMLKeys.playlist_items, None)

    track_ids = []
    for item in playlist_items:
        track_ids.append(int(item[PlaylistItemXMLKeys.track_id]))
    return iTunesPlaylist(name, track_ids)


def track_from_xml_obj(xml_obj):
    path = xml_obj.get(TrackXMLKeys.location, "")
    unicode_path = urllib.unquote(path).decode('utf8')
    fixed_path = unicode_path.replace("file://localhost/","")

    return iTunesTrack(
        xml_obj.get(TrackXMLKeys.title, ""),
        xml_obj.get(TrackXMLKeys.album, ""),
        xml_obj.get(TrackXMLKeys.artist, ""),
        xml_obj.get(TrackXMLKeys.album_artist, ""),
        fixed_path,
        )


def library_from_xml(xml_path):
    xml_obj = plistlib.readPlist(xml_path)

    # Map of track_id_no -> {song properties}
    track_xml_objs_dict = xml_obj[iTunesXMLKeys.tracks]
    tracks_by_id = {}
    for k in track_xml_objs_dict:
        tracks_by_id[int(k)] = track_from_xml_obj(track_xml_objs_dict[k])

    def user_playlist(pl):
        if PlaylistXMLKeys.playlist_items not in pl:
            return False
        if PlaylistXMLKeys.distinguished_kind in pl:
            return False
        if PlaylistXMLKeys.visible in pl:
            return False
        if PlaylistXMLKeys.smart_info in pl:
            return False
        return True

    # List of {playlist properties}
    playlist_xml_objs = xml_obj[iTunesXMLKeys.playlists]
    playlists = [playlist_from_xml_obj(x) for x in playlist_xml_objs if user_playlist(x)]

    music_folder = xml_obj[iTunesXMLKeys.music_folder]

    return iTunesLibrary(
        tracks_by_id,
        playlists,
        music_folder
        )
