#!/usr/bin/env python3

from click import command


@command()
def suggest_five():
    print("suggest_five")
    print("------------\n")
    print("Suggested word: CRANE")
