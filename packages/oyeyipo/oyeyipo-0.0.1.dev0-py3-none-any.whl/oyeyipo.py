#!/usr/env/bin python
"""
Simple bio package for Oyeyipo Olawale <oyeyipoos@gmail.com>
"""
from collections import namedtuple

__version__ = "0.0.1dev0"

fname = "Olawale"
lname = "Oyeyipo"
full_name = "%s %s" % (fname, lname)

_Rec = namedtuple("Socials", "stackoverflow github linkedin")

socials = _Rec(
    stackoverflow="https://stackoverflow.com/users/7024331/oyeyipo",
    github="https://github.com/oyeyipo",
    linkedin="https://www.linkedin.com/in/oyeyipowale/",
)
