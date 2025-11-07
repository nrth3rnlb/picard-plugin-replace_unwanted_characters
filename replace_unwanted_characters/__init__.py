# -*- coding: utf-8 -*-

from picard import config, log
from picard import metadata
from picard.script import register_script_function
from picard.ui.options import register_options_page

from .options import DEFAULT_TAGS, DEFAULT_CHAR_MAPPING, ReplaceUnwantedCharactersOptionsPage

__version__ = '1.1.0'

PLUGIN_NAME = "Replace Unwanted Characters"
PLUGIN_AUTHOR = "nrth3rnlb"
PLUGIN_VERSION = __version__
PLUGIN_API_VERSIONS = ["2.7", "2.8"]
PLUGIN_LICENSE = "GPL-2.0"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-2.0.html"
PLUGIN_DESCRIPTION = '''
    The "Replace Unwanted Characters" Plugin replaces unwanted characters in tags.
    Also add $replace_unwanted() function for Tagger.

    The plugin is based on an idea and the implementation in the "Replace Forbidden Symbols" plugin by Alex Rustler
    <alex_rustler@rambler.ru>
'''

def get_config_settings():
    """Load settings from config: returns (filter_tags, default_table, per_tag_tables)"""

    try:
        filter_tags = config.setting["replace_unwanted_characters_filter_tags"]
    except KeyError:
        filter_tags = DEFAULT_TAGS

    try:
        default_table = config.setting["replace_unwanted_characters_char_table"]
    except KeyError:
        default_table = DEFAULT_CHAR_MAPPING

    try:
        per_tag_tables = config.setting["replace_unwanted_characters_per_tag_tables"]
    except KeyError:
        per_tag_tables = {}

    return filter_tags, default_table, per_tag_tables

def _replace_with_table(value, table):
    """Apply a mapping table to a tag value list"""

    def sanitize_char(c):
        return table.get(c, c)

    return ["".join(sanitize_char(ch) for ch in item) for item in value]

def replace_unwanted_characters(tagger, metadata, *args):
    filter_tags, default_table, per_tag_tables = get_config_settings()

    for name, value in metadata.rawitems():
        if name not in filter_tags:
            continue

        entry = per_tag_tables.get(name)
        # default: apply full default_table
        if entry is None:
            table = default_table
        else:
            # support both legacy list form and new dict form
            if isinstance(entry, dict):
                active = entry.get("active", True)
                keys_list = entry.get("keys", [])
            else:
                # legacy list -> active by default
                active = True
                keys_list = entry

            if not active:
                # skip applying any replacements for this tag
                continue

            # build a per-tag mapping from default_table filtered to selected keys
            table = {k: v for k, v in default_table.items() if k in set(keys_list)}

        metadata[name] = _replace_with_table(value, table)

def script_replace_unwanted(parser, value):
    # Tagger function: use configured default mapping
    try:
        default_table = config.setting["replace_unwanted_characters_char_table"]
    except KeyError:
        default_table = DEFAULT_CHAR_MAPPING

    if isinstance(value, list):
        return _replace_with_table(value, default_table)
    else:
        # single string
        return "".join(default_table.get(ch, ch) for ch in value)


log.debug(PLUGIN_NAME + ": registration" )

register_options_page(ReplaceUnwantedCharactersOptionsPage)

metadata.register_track_metadata_processor(replace_unwanted_characters)
metadata.register_album_metadata_processor(replace_unwanted_characters)

register_script_function(script_replace_unwanted, name="replace_unwanted")
