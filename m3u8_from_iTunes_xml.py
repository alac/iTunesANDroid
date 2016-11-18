"""
m3u8_from_iTunes_xml.py xml_path output_folder
"""

import argparse, os
from iTunesParser import iTunes_xml_parser, iTunes_library

#support unicode on windows; also need `chcp 65001` in terminal...
import codecs
codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

import json
def pretty_print(d):
    print json.dumps(d, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Create m3u8 playlist files from an iTunesXML."""
        )
    parser.add_argument(
        'xml_path',
        action='store',
        type=unicode,
        help="Path of the iTunes library xml."
        )
    parser.add_argument(
        'output_folder',
        action='store',
        type=unicode,
        help="Path of the iTunes library xml."
        )

    args = parser.parse_args()
    print "arguments"
    pretty_print(vars(args))

    xml_path = args.xml_path
    output_folder = args.output_folder

    if not os.path.exists(xml_path):
        raise ValueError("Invalid xml_path: %r" % (xml_path))

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if not os.path.isdir(output_folder):
        raise ValueError("Output folder is not a folder: %r" % (output_folder))

    library = iTunes_xml_parser.library_from_xml(xml_path)

    for playlist in library.playlists:
        print "Processing playlist...", playlist.name
        locations = library.song_locations_for_playlist(playlist)

        for location in locations:
            if not os.path.exists(location):
                print "Missing file:", location

        m3u8_file = os.path.join(output_folder, playlist.name + ".m3u8")

        with codecs.open(m3u8_file, "w", "utf-8") as temp:
            for location in locations:
                rel_path = os.path.relpath(location, output_folder)
                temp.write(rel_path + "\n")
