# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]
import os
import aiohttp
import asyncio
import urllib.parse
import logging
import aiohttp
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.handlers import MessageHandler
from pyshorteners import Shortener
from pyrogram import filters, errors, Client, enums
from WebStreamer.vars import Var
from urllib.parse import quote_plus
from WebStreamer.utils.database import Database
from WebStreamer.bot import StreamBot, logger
from WebStreamer.utils import get_hash, get_name
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums.parse_mode import ParseMode
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.file_properties import get_name, get_media_file_size
from pyrogram.errors import FloodWait, UserNotParticipant
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


def get_media_file_name(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)
    else:
        return None

@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)
async def private_receive_handler(c: Client, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.LOG_CHANNEL,
            f"<b>#New_User_Joined\n\n᚛›Name :- <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>\n᚛› ID :- <code>{m.from_user.id}</code>\n᚛› From Bot :- <a href=https://t.me/File_to_Link_Star_Bot><b>File to Link Star Bots</b></a></b>"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="<b>Sorry <a href='tg://user?id={m.from_user.id}>{m..first_name}</a>,\nYou're Banned 🚫 To Use Me❓.\n\n Contact Developer <a href='https://t.me/Star_Bots_Tamil_Support'>Star Bots Tamil Support</a> They will Help You.</b>",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<b>Please Join Our Updates Channel to Use Me❗\n\nDue To Overload, Only Channel Subscribers Can Use to Me❗.</b>""",
                reply_markup=InlineKeyboardMarkup(
                    [[ InlineKeyboardButton("🤖 Join Our Bot Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}") ]]
                ),
                parse_mode=ParseMode.HTML
            )
            return
        except Exception:
            await c.send_message(
                chat_id=m.chat.id,
                text="<b>Something Wrong❗\nYou're Not Added Admin to Update Channel.\n\n👥 Support :- <a href=https://t.me/Star_Bots_Tamil_Support><b>Star Bots Tamil Support</b></a></b>",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True)
            return
    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        file_hash = get_hash(log_msg, Var.HASH_LENGTH)
        link = m.matches[0].group(0),
        file_name = get_media_file_name(m)
        file_size = humanbytes(get_media_file_size(m))
        file_caption = m.caption
        stream_link = "https://{}:{}/{}/{}".format(Var.FQDN, Var.PORT, log_msg.id, file_name)
        watch_link = "https://{}:{}/Watch/{}/{}".format(Var.FQDN, Var.PORT, log_msg.id, file_name)
        short_link = "https://{}:{}/{}/{}".format(Var.FQDN, Var.PORT, file_hash, log_msg.id)
        shorten_urls = await short(link)

        msg_text ="""
<b><i>Your Link is Generated... ⚡</i>\n
📁 File Name :- {}\n
📦 File Size :- {}\n
🔠 File Captain :- {}\n
📥 Download Link :- {}\n
🖥 Watch Link :- {}\n
🔗 Shortened Link :- {}\n
{}\n
❗ Note :- This Link is Permanent and Won't Gets Expired 🚫\n
©️ <a href=https://t.me/Star_Bots_Tamil><b></b>Star Bots Tamil</a></b></b>"""

        await log_msg.reply_text(text=f"<b>Request By :- <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>\nID :- <code>{m.from_user.id}</code>\n📥 Download Link :- {stream_link}", disable_web_page_preview=True, parse_mode=ParseMode.HTML, quote=True)
        await m.reply_text(
            text=msg_text.format(file_name, file_size, file_caption, stream_link, watch_link, short_link),
            parse_mode=ParseMode.HTML, 
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📥 Download Link", url=stream_link)], [InlineKeyboardButton("🖥 Watch Link", url=watch_link)], [InlineKeyboardButton("🔗 Shortened Link", url=short_link)], [InlineKeyboardButton("🔥 Update Channel", url="https://t.me/Star_Bots_Tamil")]]),
            quote=True
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"<b>Got FloodWait of {str(e.x)}s from <a href=tg://user?id={m.from_user.id}>{m.from_user.first_name}</a>\n\nUser ID :- <code>{str(m.from_user.id)}</code></b>", disable_web_page_preview=True, parse_mode=ParseMode.HTML)

@StreamBot.on_message(
    filters.channel
    & (
        filters.document
        | filters.video
    ),
    group=4,
)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = "https://{}:{}/{}".format(Var.FQDN, Var.PORT, log_msg.id)

        await log_msg.reply_text(
            text=f"<b>Channel Name :- <code>{broadcast.chat.title}</code>\nChannel ID :- <code>{broadcast.chat.id}</code>\nRequest URL :- https://t.me/{(await bot.get_me()).username}?start=Star_Bots_Tamil_{str(log_msg.message_id)}</b>",
            # text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** https://t.me/FxStreamBot?start=Moksh_b658_{str(log_msg.message_id)}",
            quote=True,
            parse_mode=ParseMode.HTML
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.message_id,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📥 Download Link", url=f"https://t.me/{(await bot.get_me()).username}?start=Star_Bots_Tamil_{str(log_msg.message_id)}")]])
            # [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📥", url=f"https://t.me/direct_link_generator_658_bot?start=Moksh_b658_{str(log_msg.message_id)}")]])
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"<b>Got FloodWait of {str(w.x)}s From {broadcast.chat.title}\n\nChannel ID :-</b> <code>{str(broadcast.chat.id)}</code>",
                             disable_web_page_preview=True, parse_mode=ParseMode.HTML)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"<b>#Error_Trackback :-</b> <code>{e}</code>", disable_web_page_preview=True, parse_mode=ParseMode.HTML)
        print(f"Can't Edit Broadcast Message!\nError :- {e}")

TNSHORT_API = os.environ.get("TNSHORT_API", "d03a53149bf186ac74d58ff80d916f7a79ae5745")    
                
async def short(link):
    shorten_urls = "**--Shortened URL--**\n"

    # TNShort.net Shortener
    try:
        api_url = "https://tnlink.in/api" 
        params = {'api': TNSHORT_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"**TNShort.net :- {url}**"
    except Exception as error:
        print(f"TNLink.in Error :- {error}")
                
    # Send the text
    try:
        shorten_urls += ""
        return shorten_urls
    except Exception as error:
        return error            
            
