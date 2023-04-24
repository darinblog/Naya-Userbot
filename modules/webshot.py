# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Webshot**

๏ **Perintah:** `webshot` <link>
◉ **Keterangan:** Dapatkan screenshot dari link tersebut

๏ **Perintah:** `image` <berikan teks/balas file>
◉ **Keterangan:** Jadikan sebuah gambar.
"""

import asyncio
import os

from htmlwebshot import WebShot
from PIL import Image, ImageDraw, ImageFont
from . import *

@ayra_cmd(pattern="image( (.*)|$)")
async def f2i(e):
    txt = e.pattern_match.group(1).strip()
    html = None
    if txt:
        html = e.text.split(maxsplit=1)[1]
    elif e.reply_to:
        r = await e.get_reply_message()
        if r.media:
            html = await e.client.download_media(r.media)
        elif r.text:
            html = r.text
    if not html:
        return await eod(e, "`Berikan teks atau balas ke file`")
    html = html.replace("\n", "<br>")
    shot = WebShot(quality=85)
    css = "body {background: white;} p {color: red;}"
    pic = await shot.create_pic_async(html=html, css=css)
    await e.reply(file=pic, force_document=True)
    os.remove(pic)
    if os.path.exists(html):
        os.remove(html)


@ayra_cmd(pattern="webshot(?:\s+(.*))?")
async def webshot(e):
    ajg = await e.eor("`Processing...`")
    try:
        user_link = e.pattern_match.group(1).strip()
        if not user_link:
            await e.eor("`Masukkan URL situs web yang ingin diambil tangkapan layarnya.`")
            return
        full_link = f"https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{user_link}"
        await ajg.delete()
        await e.client.send_file(
            e.chat_id,
            full_link,
            caption=f"**Tangkapan layar halaman** {user_link}",
            force_document=True,
            supports_streaming=False
        )
    except Exception as error:
        await e.eor(f"**Terjadi kesalahan:** `{error}`")
