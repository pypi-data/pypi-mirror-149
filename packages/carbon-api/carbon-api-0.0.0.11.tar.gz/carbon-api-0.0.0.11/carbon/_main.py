# Carbon - Create beautiful carbon code images using python or terminal
# Copyright (C) 2022 Stark Bots <https://github.com/StarkBotsIndustries>
#
# This file is part of Carbon.
#
# Carbon is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Carbon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Carbon. If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
import os
from carbon import _utils
from urllib.parse import quote


def boolean(value: bool | str) -> str:
    if value and (not isinstance(value, str) or not value.lower() == "false"):
        value = "true"
    else:
        value = "false"
    return value


class Carbon:
    def __init__(
        self,
        downloads_dir: str = os.getcwd(),
        *,
        colour: str = "rgba(171, 184, 195, 1)",  # Hex or rgba color
        shadow: bool = True,  # Turn on/off shadow
        shadow_blur_radius: str = "68px",
        shadow_offset_y: str = "20px",
        export_size: str = "2x",  # resolution of exported image, e.g. 1x, 3x
        font_size: str = "14px",
        font_family: str = "Hack",  # font family, e.g. JetBrains Mono, Fira Code.
        first_line_number: int = 1,
        language: str = "auto",  # programing language for properly highlighting
        line_numbers: bool = False,  # turn on/off, line number
        horizontal_padding: str = "56px",
        vertical_padding: str = "56px",
        theme: str = "seti",  # code theme
        watermark: bool = False,  # turn on/off watermark
        width_adjustment: bool = True,  # turn on/off width adjustment
        window_controls: bool = True,  # turn on/off window controls
        window_theme=None,  # "none",
        chromium_path: str = None
    ):
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        self.downloads_dir = downloads_dir if downloads_dir.endswith("/") else downloads_dir + "/"
        self.colour = colour
        self.shadow = shadow
        self.shadow_blur_radius = shadow_blur_radius
        self.shadow_offset_y = shadow_offset_y
        self.export_size = export_size
        self.font_size = font_size
        self.font_family = font_family
        self.first_line_number = first_line_number
        self.language = language
        self.line_numbers = line_numbers
        self.horizontal_padding = horizontal_padding
        self.vertical_padding = vertical_padding
        self.theme = theme
        self.watermark = watermark
        self.width_adjustment = width_adjustment
        self.window_controls = window_controls
        self.window_theme = window_theme
        self.chromium_path = chromium_path

    async def create(
        self,
        code: str,
        *,
        colour: str = None,
        shadow: bool = None,
        shadow_blur_radius: str = None,
        shadow_offset_y: str = None,
        export_size: str = None,
        font_size: str = None,
        font_family: str = None,
        first_line_number: int = None,
        language: str = None,
        line_numbers: bool = None,
        horizontal_padding: str = None,
        vertical_padding: str = None,
        theme: str = None,
        watermark: bool = None,
        width_adjustment: bool = None,
        window_controls: bool = None,
        window_theme=None,
        downloads_dir: str = None,
        file: str = None,
    ):
        if not colour:
            colour = self.colour
        if not shadow:
            shadow = self.shadow
        if not shadow_blur_radius:
            shadow_blur_radius = self.shadow_blur_radius
        if not shadow_offset_y:
            shadow_offset_y = self.shadow_offset_y
        if not export_size:
            export_size = self.export_size
        if not font_size:
            font_size = self.font_size
        if not font_family:
            font_family = self.font_family
        if not first_line_number:
            first_line_number = self.first_line_number
        if not language:
            language = self.language
        if not line_numbers:
            line_numbers = self.line_numbers
        if not horizontal_padding:
            horizontal_padding = self.horizontal_padding
        if not vertical_padding:
            vertical_padding = self.vertical_padding
        if not theme:
            theme = self.theme
        if not watermark:
            watermark = self.watermark
        if not colour:
            colour = self.colour
        if not width_adjustment:
            width_adjustment = self.width_adjustment
        if not window_controls:
            window_controls = self.window_controls
        if not downloads_dir:
            downloads_dir = self.downloads_dir
        if not file:
            file = _utils.random_file_name()
        shadow = boolean(shadow)
        line_numbers = boolean(line_numbers)
        watermark = boolean(watermark)
        width_adjustment = boolean(width_adjustment)
        window_controls = boolean(window_controls)
        data = {
            "code": quote(code.encode("utf-8")),
            "backgroundColor":	colour,
            "dropShadow": shadow,
            "dropShadowBlurRadius":	shadow_blur_radius,
            "dropShadowOffsetY": shadow_offset_y,
            "exportSize": export_size,
            "fontSize": font_size,
            "fontFamily": font_family,
            "firstLineNumber": first_line_number,
            "language": language,
            "lineNumbers": line_numbers,
            "paddingHorizontal": horizontal_padding,
            "paddingVertical": vertical_padding,
            "theme": theme,
            "watermark": watermark,
            "widthAdjustment": width_adjustment,
            "windowControls": window_controls,
            "windowTheme": window_theme,
        }
        carbonURL = _utils.createURLString(data)
        path = downloads_dir + file
        await _utils.make_carbon(carbonURL, path, chromium=self.chromium_path)
        return path
