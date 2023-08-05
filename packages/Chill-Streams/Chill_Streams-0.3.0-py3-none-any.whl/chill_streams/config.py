import argparse

from .version import CSAbout


def vlc_parse_args():
    parser = argparse.ArgumentParser(description=str(CSAbout()))
    parser.add_argument(
        "station",
        help="Index or (partial) name of station to play",
        nargs="?",  # make this arg optional
    )
    parser.add_argument(
        "-f", "--first-match",
        help="Choose first partial station name match",
        action="store_true"
    )
    parser.add_argument(
        "-l", "--loop",
        help="Loop mode: Return to station menu when player terminates (q to quit completely)",
        action="store_true"
    )
    parser.add_argument(
        "--gui",
        help="Disable ncurses interface, run VLC in GUI mode",
        action="store_true",
    )
    parser.add_argument(
        "--write-shell-script",
        help="Write a shell script that sets up environment and executes vlc-radio",
        action="store_true"
    )
    parser.add_argument(
        "--version",
        help="Print version string and exit",
        action='version',
        version=str(CSAbout())
    )
    parser.add_argument(
        # just print the bare version string
        "--bare-version",
        help=argparse.SUPPRESS,
        action='version',
        version=CSAbout().version
    )

    parsed = parser.parse_args()
    return parsed
