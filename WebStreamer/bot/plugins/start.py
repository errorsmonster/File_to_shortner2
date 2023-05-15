# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery
from WebStreamer.vars import Var 
from WebStreamer.bot import StreamBot
OWNER_ID = Var.OWNER_ID

STAR_BUTTONS = [
            [
                InlineKeyboardButton('👨🏻‍💻 Creator', user_id=OWNER_ID)
            ],
            [
                InlineKeyboardButton('🤖 Bot Channel', url='https://t.me/Star_Bots_Tamil'),                        
                InlineKeyboardButton('👥 Support Group', url='https://t.me/Star_Bots_Tamil_Support')
            ]
        ]

@StreamBot.on_message(filters.command(["start"]) & filters.private)
async def start(_, m: Message):
    reply_markup = InlineKeyboardMarkup(STAR_BUTTONS)
    mention = m.from_user.mention(style="md")
    if Var.ALLOWED_USERS and not ((str(m.from_user.id) in Var.ALLOWED_USERS) or (m.from_user.username in Var.ALLOWED_USERS)):
        return await m.reply(
            "<b>You are not in the allowed list of users who can use me. \
            Check <a href='https://github.com/EverythingSuckz/TG-FileStreamBot#optional-vars'>this link</a> for more info.</b>",
            disable_web_page_preview=True, quote=True
        )
    await m.reply_text(
            text="<b>Hi 👋🏻 {} ♥️,  Send me a File 📂 to get an Instant Stream link.</b>".format(
                mention
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
