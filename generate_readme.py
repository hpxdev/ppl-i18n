#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime
import json
import sys

header = f"""[//]: # "This file is automatically generated by {os.path.basename(__file__)}"
# ppl-i18n
This repository contains the translated strings for the game [PewPew Live](https://pewpew.live).
## Contributing
Any contribution helps, even if it's only a few words or phrases.
(but please only contribute to languages you can speak; no Google Translate)

For information on how to submit changes on GitHub, take a look at this [guide](https://docs.github.com/en/free-pro-team@latest/github/managing-files-in-a-repository/editing-files-in-another-users-repository).

If you contribute a significant amount, I'll put you in the credits!

A few tips for contributing:
* Keep the `%s` as they later get replaced by some other text.
* The text fragments that look like `#ffffffff` encode colors. Keep them!
* Try to have the translations be approximately the same length as the English text.
* Don't hesitate the reword the text to better fit the language.
* In order to reduce merge conflicts, avoid working on a single pull request for multiple days. It's better if you create one pull request per day.
## Adding new languages
If you want to add support for a new language, create a GitHub Issue so that we can discuss
the feasibility.
## Status
"""

# Change CWD to the script's own director.
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Notes about metadata.json (can't put comments in json!):
#  * the order in which the languages are is:
#    - sort-of latin-based languages first, in alphabetical order
#    - followed by the other real languages, in alphabetical order
#    - the fun languages, in alphabetical order
#    (then get sorted from most uncompleted to fully completed)
#  * language code are (when possible) in ISO 639-2
#    https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
#  * There is no code for the chinese variants
metadata_source_file_path = "metadata.json"

with open(metadata_source_file_path, "r", encoding="utf8") as f:
    langs = json.load(f)

lang_files_dir = "translations/"
lang_stats = {}

# Generate the stats
for lang in langs:
    print("parsing " + lang["english_name"])
    lang_code = lang["code"]
    lang_file = lang_files_dir + lang_code + ".po"
    message_count = 0.0
    missing_translations = 0.0
    with open(lang_file, "r", encoding="utf8") as f:
        for line in f:
            if line.startswith("msgstr"):
                message_count += 1
            if line == 'msgstr ""\n':
                missing_translations += 1
    lang_stats[lang_code] = {"total": message_count, "missing": missing_translations}

# Write the README
readme_file = "README.md"
with open(readme_file, "w", encoding="utf8", newline="\r\n") as f:
    f.write(header)

    results = []
    for lang in langs:
        lang_code = lang["code"]
        stats = lang_stats[lang_code]
        percentage = stats["missing"] / stats["total"]
        percentage = int(100 - percentage * 100)
        results.append([lang, percentage])

    results = sorted(
        results, key=lambda x: lang_stats[x[0]["code"]]["missing"], reverse=True
    )
    for lang, percentage in results:
        lang_code = lang["code"]
        lang_name = lang["english_name"]
        flag = lang["emoji_flag"]
        stats = lang_stats[lang_code]
        comment = (
            " ("
            + str(percentage)
            + "% complete; "
            + str(int(stats["missing"]))
            + " remaining)"
        )
        if stats["missing"] == 0:
            comment = " (100% complete! 🎉)"
        lang_link = "[" + lang_name + "](/translations/" + lang_code + ".po)"
        f.write("* " + flag + " " + lang_link + comment + "\n")

    date = datetime.datetime.utcnow()
    date_str = date.strftime("%b %d %Y %H:%M:%S")
    f.write("> Report generated on " + date_str + " UTC")
