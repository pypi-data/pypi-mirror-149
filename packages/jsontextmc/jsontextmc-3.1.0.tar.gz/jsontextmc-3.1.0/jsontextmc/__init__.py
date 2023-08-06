#!/usr/bin/env python3
# coding=utf-8
# encoding=utf-8
# pylint: disable=W0311
"""Minecraft uses two main systems for formatting text.

The Legacy format uses section symbols and hexadecimal color coding,
while the JSON format uses key-value pairs to color individual parts of text.

JSONTextMC is a module for translating legacy messages to and from JSON-formatted text.
Output is not valid JSON by itself, it must be translated into JSON with :func:`json.loads`.

Strict modes and inheritance of various JSON elements can be controlled.

Legacy -> JSON::

    >>> import jsontextmc
    >>> jsontextmc.to_json("\xa7cRed! \xa7lAnd bold!")
    [{'text': 'Red! ', 'color': 'red'}, {'text': 'And bold!', 'color': 'red', 'bold': True}]
    >>> jsontextmc.to_json("\xa7cRed! \xa7lAnd bold!", inherit_parent=False)
    [{'text': 'Red! ', 'color': 'red'}, {'text': 'And bold!', 'bold': True}]
    >>> jsontextmc.to_json("\xa7l\xa7cBold before red, not anymore", strict=True)
    {'text': 'Bold before red, not anymore', 'color': 'red'}
    >>> jsontextmc.to_json("Simple plain text")
    'Simple plain text'
    >>> jsontextmc.to_json("\xa7x12bcdeHex codes work too")
    {'text': 'Hex codes work too', 'color': '#12bcde'}

JSON -> Legacy::

    >>> import jsontextmc
    >>> jsontextmc.from_json(
    ...   [{'text': 'Red! ', 'color': 'red'}, {'text': 'And bold!', 'bold': True}]
    ... )
    '§cRed! §lAnd bold!'
    >>> jsontextmc.from_json('Simple plain text')
    'Simple plain text'
"""

from __future__ import annotations

import re

__version__: str = "3.1.0"


def tokenize(sectioned: str, separator: str = "\xa7") -> list[str]:
    """
    Split text based on separator.

    Text is searched for the separator and split with the Minecraft color code in front of it.

    :param sectioned: Text to split
    :param separator: The separator to split on
    :return: Split list of tokenized codes
    """
    return re.split(
        fr"(?P<r>{separator}[x#][0-9a-f]{{6}}|{separator}[0-9a-frk-o])",
        sectioned,
        flags=re.IGNORECASE | re.UNICODE,
    )


COLORS: dict[str:str] = {
    "0": "black",
    "1": "dark_blue",
    "2": "dark_green",
    "3": "dark_aqua",
    "4": "dark_red",
    "5": "dark_purple",
    "6": "gold",
    "7": "gray",
    "8": "dark_gray",
    "9": "blue",
    "a": "green",
    "b": "aqua",
    "c": "red",
    "d": "light_purple",
    "e": "yellow",
    "f": "white",
    "r": "reset",
}

COLORS_REVERSED: dict[str:str] = {v: k for k, v in COLORS.items()}

FORMATS: dict[str:str] = {
    "k": "obfuscated",
    "l": "bold",
    "m": "strikethrough",
    "n": "underlined",
    "o": "italic",
}

FORMATS_REVERSED: dict[str:str] = {v: k for k, v in FORMATS.items()}

ACCEPTED_FORMATS: str = "0123456789abcdefklmnorx#ABCDEFKLMNORX"


def to_json(
    text: str,
    separator: str = "\xa7",
    strict: bool = False,
    inherit_parent: bool = True,
) -> dict | list | str:
    """
    Translate Minecraft color-coded text into a modern JSON format.

    * Standalone text will be returned as-is.
    * Text components with one element will be returned themselves, outside a list.
    * For all other cases, each element is appended to a list and returned.

    If ``strict`` is true, then formatting codes are not allowed to be declared before color codes.
    If a formatting code appears before any color is applied, it will be ignored and discarded.

    If ``inherit_parent`` is false, formatting from the previous element will not carry over into
    the next one, and so any codes defined before will be reset. The reset code works identically.

    :param text: The text to translate into raw JSON text.
    :param separator: Character to identify color codes by. Natively, it is §, but others may use &
    :param strict: If true, formatting codes will be cleared if they are before a color code.
    :param inherit_parent: If true, formatting from previous element will be not be copied ahead.
    :return: List, string, or dictionary of a valid JSON component. Use json to transfer into JSON.
    """
    exported: list = []
    settings: dict = {"color": None, "format": []}
    for part in [x for x in tokenize(text, separator) if x]:
        # Tokens are guarenteed to have valid codes
        # if part is a valid color code (has section sign *and* a valid code after)
        if len(part) == 2 or len(part) == 8:
            # If part is a hex code and valid
            if (
                len(part) == 8
                and part[1] in "x#X"
                and all(c in "0123456789abcdefABCDEF" for c in part[2:8])
            ):
                # Hashtag + 6 digits in hexadecimal color code
                settings["color"] = f"#{part[2:8].lower()}"
            elif part[1] in "rR":
                # Reset code
                settings = {"color": "reset", "format": []}

            elif part[1] in "0123456789abcdefABCDEF":
                # If part is a color code
                settings["color"] = COLORS[part[1].lower()]
            elif part[1] in "klmnoKLMNO":
                # Else, part must be a format code
                if not (strict and not settings["color"]):
                    # If strict and no color is set before a format
                    settings["format"].append(FORMATS[part[1].lower()])

        else:
            # If a setting is present
            if settings["color"] or settings["format"]:
                temp: dict = {"text": part}
                if settings["color"]:
                    temp["color"] = settings["color"]
                if settings["format"]:
                    for option in settings["format"]:
                        temp[option] = True
                exported.append(temp)
            else:
                # No formatting
                exported.append(part)
            if not inherit_parent:
                settings = {"color": None, "format": []}
    if len(exported) == 1:
        return exported[0]
    return exported


def from_json(text: dict | list | str, separator: str = "\xa7") -> str:
    """
    Translate modern JSON text into legacy section-sign text.

    .. note::
        Any extra elements such as clickables, translations, or actions **will be discarded**.
        Only ``"text"``, ``"color"``, and the formatting code booleans are dealt with.

    :param text: JSON component text to transform.
    :param separator: Character to use as color code marking.
    :return: String of legacy-coded text.
    """
    exported: str = ""
    if isinstance(text, (dict, list)):
        if isinstance(text, dict):
            text: list = [text]
        for entry in text:
            if len(entry.keys()) >= 2 and "text" in entry:
                if "color" in entry:
                    exported += separator + COLORS_REVERSED[entry["color"].lower()]
                for option in FORMATS_REVERSED.keys():
                    if option in entry:
                        exported += separator + FORMATS_REVERSED[option]
            if "text" in entry:
                exported += entry["text"]
    elif isinstance(text, str):
        return text
    return exported
