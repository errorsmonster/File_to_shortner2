# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery
from WebStreamer.vars import Var 
from WebStreamer.bot import StreamBot
from pyrogram.enums.parse_mode import ParseMode
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
            
@StreamBot.on_message(filters.command(["help"]) & filters.private & filters.incoming)
async def help(client, message):
    reply_markup = InlineKeyboardMarkup(STAR_BUTTONS)
    mention = message.from_user.mention
    if Var.ALLOWED_USERS and not ((str(message.from_user.id) in Var.ALLOWED_USERS) or (message.from_user.username in Var.ALLOWED_USERS)):
        return await message.reply(
            "<b>You are not in the allowed list of users who can use me. \
            Check <a href='https://github.com/EverythingSuckz/TG-FileStreamBot#optional-vars'>this link</a> for more info.</b>",
            disable_web_page_preview=True, quote=True
        )
    await message.reply_text(
            text="<b>Hi 👋🏻 {} ♥️,  Send me a File 📂 to get an Instant Stream link.</b>".format(
                mention
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

@StreamBot.on_message(filters.command(["about"]) & filters.private & filters.incoming)
async def about(client, message):
    mention = message.from_user.mention
    reply_markup = InlineKeyboardMarkup(STAR_BUTTONS)
    if Var.ALLOWED_USERS and not ((str(message.from_user.id) in Var.ALLOWED_USERS) or (message.from_user.username in Var.ALLOWED_USERS)):
        return await message.reply(
            "<b>You are not in the allowed list of users who can use me. \
            Check <a href='https://github.com/EverythingSuckz/TG-FileStreamBot#optional-vars'>this link</a> for more info.</b>",
            disable_web_page_preview=True, quote=True
        )
    await message.reply_text(
            text="<b>Hi 👋🏻 {} ♥️,  Send me a File 📂 to get an Instant Stream link.</b>".format(
                mention
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
            
REPLY_ERROR = """<b>Use This Command as a Reply to any Telegram Message Without any Spaces.</b>"""


@StreamBot.on_message(filters.private & filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler_open(_, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if m.reply_to_message is None:
        await m.reply(REPLY_ERROR, quote=True)
    else:
        await broadcast(m, db)

@StreamBot.on_message(filters.private & filters.command("stats") & filters.user(OWNER_ID))
async def sts(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    await m.reply_text(
        text=f"**Total Users in Database 📂 :- {await db.total_users_count()}**",
        quote=True
    )            
