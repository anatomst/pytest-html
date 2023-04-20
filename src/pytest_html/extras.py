# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from enum import Enum


class Format(Enum):
    HTML = "html"
    IMAGE = "image"
    JSON = "json"
    TEXT = "text"
    URL = "url"
    VIDEO = "video"


def extra(content, format_type: Format, name=None, mime_type=None, extension=None):
    return {
        "name": name,
        "format_type": format_type.value,
        "content": content,
        "mime_type": mime_type,
        "extension": extension,
    }


def html(content):
    return extra(content, Format.HTML)


def image(content, name="Image", mime_type="image/png", extension="png"):
    return extra(content, Format.IMAGE, name, mime_type, extension)


def png(content, name="Image"):
    return image(content, name, mime_type="image/png", extension="png")


def jpg(content, name="Image"):
    return image(content, name, mime_type="image/jpeg", extension="jpg")


def svg(content, name="Image"):
    return image(content, name, mime_type="image/svg+xml", extension="svg")


def json(content, name="JSON"):
    return extra(content, Format.JSON, name, "application/json", "json")


def text(content, name="Text"):
    return extra(content, Format.TEXT, name, "text/plain", "txt")


def url(content, name="URL"):
    return extra(content, Format.URL, name)


def video(content, name="Video", mime_type="video/mp4", extension="mp4"):
    return extra(content, Format.VIDEO, name, mime_type, extension)


def mp4(content, name="Video"):
    return video(content, name)
