#!/usr/bin/python3

"""
get concerts data from API provider
"""

from datetime import date

from .api.bandsintown import Client


def query_bit(raw_artists, args):
    """Query Bandsintown for concert list"""
    bit_client = Client(args.bit_appid)
    concerts_list = []
    for artist in raw_artists:
        # TODO: Why are we getting some empty artists?
        if artist != '':
            if args.max_date:
                date_range = str(date.today()) + ',' + args.max_date
                concerts = bit_client.artists_events(artist, date=date_range)
            else:
                concerts = bit_client.artists_events(artist)
            if concerts is not None:
                concerts_list = concerts_list + concerts
    return concerts_list


def filter_location(concerts_list, location):
    """Filter concerts based on location"""
    concerts_list = [concert for concert in concerts_list if
            (concert['venue']['city'] == location)]
    return concerts_list


def bit(raw_artists, args):
    """Wrapper function for Bandsintown provider"""
    concerts_list = query_bit(raw_artists, args)
    concerts_list = filter_location(concerts_list, args.location)
    return concerts_list
