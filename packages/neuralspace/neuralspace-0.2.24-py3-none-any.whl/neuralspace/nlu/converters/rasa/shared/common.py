from typing import Match, Text

from neuralspace.nlu.converters.rasa.util import (
    ESCAPE,
    ESCAPE_DCT,
    GROUP_COMPLETE_MATCH,
    UNESCAPE,
    UNESCAPE_DCT,
)


def encode_string(s: Text) -> Text:
    """Return an encoded python string."""

    def replace(match: Match) -> Text:
        return ESCAPE_DCT[match.group(GROUP_COMPLETE_MATCH)]

    return ESCAPE.sub(replace, s)


def decode_string(s: Text) -> Text:
    """Return a decoded python string."""

    def replace(match: Match) -> Text:
        return UNESCAPE_DCT[match.group(GROUP_COMPLETE_MATCH)]

    return UNESCAPE.sub(replace, s)
