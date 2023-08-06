#!/usr/bin/python3

"""
scan a music directory to find concerts near a specified location
"""

from .version import __version__
from .cli import parse_args
from .scan import scan_dir
from .concerts import bit
from .output import output_wrapper


def main():
    """Main function."""
    args = parse_args()
    raw_artists = scan_dir(args.directory, args.cache)
    concerts_list = bit(raw_artists, args)
    output_wrapper(concerts_list, args.output)


if __name__ == "__main__":
    main()
