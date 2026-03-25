import os
import re

import aiofiles
import aiohttp
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from ytSearch import VideosSearch

from AnonXMusic import app
from config import YOUTUBE_IMG_URL

# ============================================================
#  👇 Apne 5 image URLs yahan daal do
# ============================================================
BACKGROUND_IMAGES = [
    "https://files.catbox.moe/nlumcw.jpg",
    "https://files.catbox.moe/rhyyq7.jpg",
    "https://files.catbox.moe/4wyd3q.jpg",
    "https://files.catbox.moe/po9tcz.jpg",
    "https://files.catbox.moe/em3egx.jpg",
]
# ============================================================

# Sequential counter — har call pe next image use hogi
_bg_index = 0


def get_next_bg_url():
    global _bg_index
    url = BACKGROUND_IMAGES[_bg_index % len(BACKGROUND_IMAGES)]
    _bg_index += 1
    return url


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def circle(img):
    h, w = img.size
    a = Image.new('L', [h, w], 0)
    b = ImageDraw.Draw(a)
    b.pieslice([(0, 0), (h, w)], 0, 360, fill=255, outline="white")
    c = np.array(img)
    d = np.array(a)
    e = np.dstack((c, d))
    return Image.fromarray(e)


def clear(text):
    words = text.split(" ")
    title = ""
    for i in words:
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()


async def get_thumb(videoid, user_id):
    if os.path.isfile(f"cache/{videoid}_{user_id}.png"):
        return f"cache/{videoid}_{user_id}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        # ── Sequential background image download ──
        bg_url = get_next_bg_url()
        bg_cache_path = f"cache/bg_{videoid}_{user_id}.png"

        async with aiohttp.ClientSession() as session:
            async with session.get(bg_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(bg_cache_path, mode="wb") as f:
                        await f.write(await resp.read())

        # ── Background process ──
        bg_image = Image.open(bg_cache_path)
        background = changeImageSize(1280, 720, bg_image).convert("RGBA")

        # Slight blur + darken for readability
        background = background.filter(filter=ImageFilter.BoxBlur(6))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.55)

        # ── Text overlay ──
        draw = ImageDraw.Draw(background)
        arial = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 30)
        font  = ImageFont.truetype("AnonXMusic/assets/font.ttf", 30)

        draw.text((1110, 8), unidecode(app.name), fill="white", font=arial)
        draw.text(
            (55, 560),
            f"{channel} | {views[:23]}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (57, 600),
            clear(title),
            (255, 255, 255),
            font=font,
        )
        draw.line(
            [(55, 660), (1220, 660)],
            fill="white",
            width=5,
            joint="curve",
        )
        draw.ellipse(
            [(918, 648), (942, 672)],
            outline="white",
            fill="white",
            width=15,
        )
        draw.text(
            (36, 685),
            "00:00",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (1185, 685),
            f"{duration[:23]}",
            (255, 255, 255),
            font=arial,
        )

        # ── Cleanup & save ──
        try:
            os.remove(bg_cache_path)
        except:
            pass

        background.save(f"cache/{videoid}_{user_id}.png")
        return f"cache/{videoid}_{user_id}.png"

    except Exception:
        return YOUTUBE_IMG_URL
        
