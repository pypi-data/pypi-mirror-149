#!/usr/bin/python3

"""
scan a music directory and output a list of artists
"""

import os
import pickle

import mutagen


def has_changed(song_cache, fullpath):
    """Query song cache to know if file has changed (or is new) since last run.
    If that is the case, add it to the cache"""
    # TODO: files that have been deleted are not currently handled
    file_has_changed = False
    mtime = os.stat(fullpath).st_mtime
    if (fullpath not in song_cache) or (fullpath in song_cache and
                                        song_cache[fullpath] != mtime):
        file_has_changed = True
        song_cache[fullpath] = mtime
    return song_cache, file_has_changed


def write_song_cache(song_cache, cache_dir):
    """Write song cache file to disk"""
    song_cache_file = os.path.join(cache_dir, 'song_cache')
    with open(song_cache_file, 'wb') as _cache:
        pickle.dump(song_cache, _cache)


def get_song_cache(cache_dir):
    """Get the song cache if it exists"""
    song_cache = {}
    song_cache_file = os.path.join(cache_dir, 'song_cache')
    if os.path.isfile(song_cache_file):
        with open(song_cache_file, 'rb') as _cache:
            song_cache = pickle.load(_cache)
    return song_cache


def write_artist_cache(raw_artists, cache_dir):
    """Write artist cache file to disk"""
    artist_cache_file = os.path.join(cache_dir, 'artist_cache')
    with open(artist_cache_file, 'w+', encoding='utf-8') as _cache:
        _cache.write('\n'.join(raw_artists))


def get_artist_cache(cache_dir):
    """Get the artist cache if it exists"""
    raw_artists = []
    artist_cache_file = os.path.join(cache_dir, 'artist_cache')
    if os.path.isfile(artist_cache_file):
        with open(artist_cache_file, 'r', encoding='utf-8') as _cache:
            raw_artists = _cache.read().splitlines()
    return raw_artists


def scan_dir(music_dir, cache_dir):
    """Scan a directory and output a list of artists"""
    raw_artists = get_artist_cache(cache_dir)
    song_cache = get_song_cache(cache_dir)
    for dirname, _, filenames in os.walk(music_dir, topdown=False):
        for song in filenames:
            fullpath = os.path.abspath(os.path.join(dirname, song))
            if song.endswith(('.flac', '.mp3', '.ogg')):
                song_cache, file_has_changed = has_changed(song_cache, fullpath)
                if file_has_changed:
                    # TODO: fix this try-except? IIRC, mutagen crashed on my
                    # full music collection and I didn't wanted to debug it at
                    # the time.
                    try:
                        artist = mutagen.File(fullpath)["artist"]
                        raw_artists.append(''.join(artist))  # list to string
                    except:  # pylint: disable=W0702
                        pass
    raw_artists = set(raw_artists)
    write_song_cache(song_cache, cache_dir)
    write_artist_cache(raw_artists, cache_dir)
    return raw_artists
