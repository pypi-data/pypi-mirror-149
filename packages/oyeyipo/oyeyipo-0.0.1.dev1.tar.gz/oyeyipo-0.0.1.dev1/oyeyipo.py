#!/usr/env/bin python
"""
Simple bio package for Oyeyipo Olawale <oyeyipoos@gmail.com>
"""
import sys
from collections import namedtuple


__version__ = "0.0.1dev1"

fname = "Olawale"
lname = "Oyeyipo"
full_name = "%s %s" % (fname, lname)
tel = ["+2348090539375", "+2349038831715"]

_Rec = namedtuple("Socials", "stackoverflow github linkedin")

socials = _Rec(
    stackoverflow="https://stackoverflow.com/users/7024331/oyeyipo",
    github="https://github.com/oyeyipo",
    linkedin="https://www.linkedin.com/in/oyeyipowale/",
)


def cli():
    phonenumbers = "--phone" in sys.argv
    if phonenumbers:
        print(*tel, sep="\n")


if __name__ == "__main__":
    cli()
