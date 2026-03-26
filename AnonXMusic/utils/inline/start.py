from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton

import config
from AnonXMusic import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.PRIMARY  # 🔵 Blue
            ),
            InlineKeyboardButton(
                text=_["S_B_2"],
                url=config.SUPPORT_CHAT,
                style=ButtonStyle.SUCCESS  # 🟢 Green
            ),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.PRIMARY
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                callback_data="settings_back_helper",
                style=ButtonStyle.DEFAULT
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_6"],
                user_id=config.OWNER_ID,
                style=ButtonStyle.DANGER  # 🔴 Red
            ),
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=config.SUPPORT_CHANNEL,
                style=ButtonStyle.SUCCESS
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_2"],
                url=config.SUPPORT_CHAT,
                style=ButtonStyle.PRIMARY
            ),
        ],
        [
            InlineKeyboardButton(
                text="˹δᴏᴜʀᴄє ᴄᴏᴅє˼",
                url="https://files.catbox.moe/6jp8hr.mp4",
                style=ButtonStyle.DANGER
            )
        ],
    ]

    return buttons
