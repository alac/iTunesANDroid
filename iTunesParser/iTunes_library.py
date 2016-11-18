class iTunesLibrary:
    def __init__(
        self,
        tracks_by_id,
        playlists,
        music_folder
        ):
        self.tracks_by_id = tracks_by_id
        self.playlists = playlists
        self.music_folder = music_folder


    def song_locations_for_playlist(self, playlist):
        locations = []
        for track_id in playlist.track_ids:
            track = self.tracks_by_id.get(track_id, None)

            if not track:
                print "Missing track_id:", track_id
                continue

            locations.append(track.location)
        return locations


class iTunesPlaylist:
    def __init__(
        self,
        name,
        track_ids
        ):
        self.name = name
        self.track_ids = track_ids

class iTunesTrack:
    def __init__(
        self,
        title,
        album,
        artist,
        album_artist,
        location
        ):
        self.title = title
        self.album = album
        self.artist = artist
        self.album_artist = album_artist
        self.location = location