# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]
import asyncio
import urllib.parse
import logging
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
            f"<b>#New_User_Joined\n\n᚛›Name :- <a href='tg://user?id={m.from_user.id}'>{m..first_name}</a>\n᚛› ID :- <code>{m.from_user.id}</code>\n᚛› From Bot :- <a href=https://t.me/File_to_Link_Star_Bot><b>File to Link Star Bots</b></a></b>"
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
                text="""<i><b>Join Our Bot Channel to Use Me</b> 🔐</i>""",
                reply_markup=InlineKeyboardMarkup(
                    [[ InlineKeyboardButton("Join Now 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}") ]]
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
        file_name = get_media_file_name(m)
        file_size = humanbytes(get_media_file_size(m))
        file_caption = m.caption
        stream_link = "https://{}:{}/{}/{}".format(Var.FQDN, Var.PORT, log_msg.id, file_name)
        watch_link = "https://{}:{}/Watch/{}/{}".format(Var.FQDN, Var.PORT, log_msg.id, file_name)
        short_link = "https://{}:{}/{}/{}".format(Var.FQDN, Var.PORT, file_hash, log_msg.id)

        msg_text ="""
<b><i>Your Link is Generated... ⚡</i>\n
📁 File Name :- {}\n
📦 File Size :- {}\n
🔠 File Captain :- {}\n
📥 Download Link :- {}\n
🖥 Watch Link :- {}\n
🔗 Shortened Link :- {}\n
❗ Note :- This Link is Permanent and Won't Gets Expired 🚫\n
©️ <a href=https://t.me/Star_Bots_Tamil><b></b>Star Bots Tamil</a></b></b>"""

        await log_msg.reply_text(text=f"<b>Request By :- [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**ID :- <code>{m.from_user.id}</code>\n📥 Download Link :- {stream_link}", disable_web_page_preview=True, parse_mode=ParseMode.HTML, quote=True)
        await m.reply_text(
            text=msg_text.format(file_name, file_size, file_caption, stream_link, watch_link, short_link),
            parse_mode=ParseMode.HTML, 
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ 📥", url=stream_link)]]),
            quote=True
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode=ParseMode.HTML)

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
            text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** https://t.me/{(await bot.get_me()).username}?start=Moksh_b658_{str(log_msg.message_id)}",
            # text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** https://t.me/FxStreamBot?start=Moksh_b658_{str(log_msg.message_id)}",
            quote=True,
            parse_mode=ParseMode.HTML
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.message_id,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📥", url=f"https://t.me/{(await bot.get_me()).username}?start=Moksh_b658_{str(log_msg.message_id)}")]])
            # [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📥", url=f"https://t.me/direct_link_generator_658_bot?start=Moksh_b658_{str(log_msg.message_id)}")]])
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(w.x)}s from {broadcast.chat.title}\n\n**Cʜᴀɴɴᴇʟ ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True, parse_mode=ParseMode.HTML)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`", disable_web_page_preview=True, parse_mode=ParseMode.HTML)
        print(f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\nEʀʀᴏʀ: {e}")
