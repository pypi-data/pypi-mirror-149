#!/usr/bin/python3

"""
songkick API provider
"""

import musicbrainzngs

from metalfinder.version import __version__

musicbrainzngs.set_useragent("metalfinder", __version__, "https://gitlab.com/baldurmen/metalfinder")


def mb_artist_id(raw_artists):
    """Match an artist list to their MusicBrainz ID"""
    mb_ids = []
    for artist in raw_artists:
        mbid = musicbrainzngs.search_artists(artist=artist,limit=1)
        if mbid['artist-count'] != 0:
            mb_ids.append(mbid['artist-list'][0]['id'])
    return mb_ids
