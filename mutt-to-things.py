#!/usr/bin/env python3

import argparse
import email.parser
import subprocess
import sys


def applescript_escape(string):
    """Escape backlsahes and double quotes for applescript"""
    return string.replace('\\', '\\\\').replace('"', '\\"')


def parse_message(raw):
    """Parse an e-mail for useful headers to include in task

    Input: string containing messsage
    Output: (title, note)
        - title: "Mutt: {subject}"
        - note: string for inclusion in task note with list of headers from
                headers_want
    """
    headers_want = ["Message-Id", "Date", "From", "To", "Cc", "Subject"]

    # Transform to lower case for case-insensitive matching and remove newlines
    message = email.parser.HeaderParser().parsestr(raw)
    headers_all = {k.lower(): " ".join(v.splitlines())
                   for k, v in message.items()}

    # List of tuples (header key, header value) rather than dictionary to
    # preserve the order of headers_want
    headers_have = [(h, headers_all[h.lower()]) for h in headers_want
                    if h.lower() in headers_all]

    title = "Mutt: {}".format(headers_all["subject"])
    note = "\n".join(["{k}: {v}".format(k=x[0], v=x[1]) for x in headers_have])
    return (title, note)


def send_to_omnifocus(title, note, quickentry=False):
    """Either create a Things task or pop up the quick entry window"""
    if quickentry:
        scpt = """
            tell application "Things3"
                show quick entry panel with properties {{notes: "{}"}}
            end tell
            """.format(applescript_escape(note))
    else:
        scpt = """
            tell application "Things3"
                set newToDo to make new to do ¬
                    with properties {{name: "{title}", notes: "{note}"}}
            end tell
            """.format(
                title=applescript_escape(title),
                note=applescript_escape(note)
            )

    subprocess.run(["osascript", "-"], input=scpt, text=True)


def main():
    description = ("Parse an e-mail from STDIN and add a task to Things with "
                   "message details in the note")
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-q",
        action="store_true",
        help="Use the quick entry window"
    )
    args = parser.parse_args()

    title, note = parse_message(sys.stdin.read())
    send_to_omnifocus(title=title, note=note, quickentry=args.q)


if __name__ == "__main__":
    main()
