# Replace Unwanted Characters (Picard plugin)

Replace Unwanted Characters is a MusicBrainz Picard plugin that replaces characters often problematic in filenames or filesystems (for example `/`, `*`, `?`, `"` , `.`) with visually similar Unicode alternatives.

## Features

- Replace specified characters in configurable tags (default: `album`, `artist`, `title`, `albumartist`, `releasetype`, `label`).
- Configurable default character mapping table.
- Per-tag mappings: enable either the default mapping or a custom selection for each tag.
- Tagger script function: `$replace_unwanted()` for use in Picard scripts.

## Installation

1. Copy the plugin folder into Picard's plugin directory (typically `~/.config/musicbrainz-picard/plugins` on Linux).
2. Restart Picard.
3. Enable the plugin in Picard's Plugins settings.

## Usage

- The plugin automatically processes track and album metadata and replaces configured characters for the enabled tags.
- It is possible to configure a separate assignment for each tag.
- In scripts or tagger rules you can use `$replace_unwanted(<tagname>)` to apply the replacement to a specific tag.
- Configure the plugin settings via Picard's Plugins settings to customize which tags to process and the character mappings.

## Configuration

Open Picard \> Options \> Plugins \> Replace Unwanted Characters (or the plugin's Options page):

- **Affected Tags**: add or remove tags that should be taken into account.
- **Default Replacements**: Define your own replacement rules or use the default.
- **Per-Tag Mappings**: choose whether a tag uses the default mappings or allow only certain mappings for the tag.

## Default character mapping

The plugin ships with a sensible default mapping, e.g.:
- `:` -> `∶`
- `/` -> `⁄`
- `*` -> `∗`
- `?` -> `？`
- `"` -> `″`
- `\` -> `⧵`
- `.` -> `․`
- `|` -> `ǀ`
- `<` -> `‹`
- `>` -> `›`

## Development

Project layout:
- `replace_unwanted_characters/__init__.py` — plugin implementation
- `replace_unwanted_characters/replace_unwanted_characters_config.ui` — Qt UI for options