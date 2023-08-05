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


import os
import string
import secrets
from pyppeteer import launch

DOWNLOAD_FOLDER = os.getcwd()


defaultOptions = {
    "backgroundColor": "rgba(171, 184, 195, 1)",
    "code": "",
    "dropShadow": True,
    "dropShadowBlurRadius": "68px",
    "dropShadowOffsetY": "20px",
    "exportSize": "2x",
    "fontFamily": "Hack",
    "firstLineNumber": 1,
    "fontSize": "14px",
    "language": "auto",
    "lineNumbers": False,
    "paddingHorizontal": "56px",
    "paddingVertical": "56px",
    "squaredImage": False,
    "theme": "seti",
    "watermark": False,
    "widthAdjustment": True,
    "windowControls": True,
    "windowTheme": None,
}

optionToQueryParam = {
    "backgroundColor": "bg",
    "code": "code",
    "dropShadow": "ds",
    "dropShadowBlurRadius": "dsblur",
    "dropShadowOffsetY": "dsyoff",
    "exportSize": "es",
    "fontFamily": "fm",
    "firstLineNumber": "fl",
    "fontSize": "fs",
    "language": "l",
    "lineNumbers": "ln",
    "paddingHorizontal": "ph",
    "paddingVertical": "pv",
    "squaredImage": "si",
    "theme": "t",
    "watermark": "wm",
    "widthAdjustment": "wa",
    "windowControls": "wc",
    "windowTheme": "wt",
}

ignoredOptions = [
    # Can't pass these as URL (So no support now)
    "backgroundImage",
    "backgroundImageSelection",
    "backgroundMode",
    "squaredImage",
    "hiddenCharacters",
    "name",
    "lineHeight",
    "loading",
    "icon",
    "isVisible",
    "selectedLines",
]


def validateBody(body_: dict):
    validatedBody = {}
    if not body_['code']:
        raise Exception("Code is required for creating carbon")

    for option in body_:
        if option in ignoredOptions:
            print(f"Unsupported option: {option} found. Ignoring!")
            continue
        if not (option in defaultOptions):
            print(f"Unexpected option: {option} found. Ignoring!")
            continue
        validatedBody[option] = body_[option]
    return validatedBody


def createURLString(validatedBody):
    base_url = "https://carbon.now.sh/"
    first = True
    url = ""
    try:
        if validatedBody['backgroundColor'].startswith('#') or checkHex(validatedBody['backgroundColor'].upper()):
            validatedBody['backgroundColor'] = hex2rgb(
                validatedBody['backgroundColor'])
        for f in ["fontFamily", "language", "theme", "windowTheme"]:
            if validatedBody[f]:
                validatedBody[f] = validatedBody[f].lower()
    except KeyError:
        pass
    for option in validatedBody:
        if first:
            first = False
            url = base_url + \
                f"?{optionToQueryParam[option]}={validatedBody[option]}"
        else:
            url = url + \
                f"&{optionToQueryParam[option]}={validatedBody[option]}"
    return url


def hex2rgb(h):
    h = h.lstrip('#')
    return 'rgb'+str(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))


def checkHex(s):
    for ch in s:
        if (ch < '0' or ch > '9') and (ch < 'A' or ch > 'F'):
            return False
    return True


async def make_carbon(url, path, chromium: str = None):
    browser = await launch(
        executablePath=chromium,
        defaultViewPort=None,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    try:
        page = await browser.newPage()
        await page._client.send('Page.setDownloadBehavior', {
            'behavior': 'allow',
            'downloadPath': DOWNLOAD_FOLDER
        })
        await page.goto(url, timeout=100000)
        element = await page.querySelector("#export-container  .container-bg")
        try:
            await element.screenshot({'path': path})
        except ValueError as e:
            if "Unsupported screenshot mime type" in str(e):
                path = path + ".png"
                await element.screenshot({'path': path})
            else:
                raise
    finally:
        await browser.close()
    return path


def random_file_name():
    letters = string.ascii_lowercase + string.digits
    random = ''.join(secrets.choice(letters) for _ in range(6))
    return f'carbon-{random}.png'
