import urllib.parse
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.database import Database
from pyrogram import filters, enums
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
OWNER_ID = Var.OWNER_ID

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

START_TEXT = """
<b><i>Hello 👋🏻</i>{},\n
I'm Star Bots Tamil's Official File to Link Bot (Link Generator Bot). Maintained By :- <a href='https://t.me/Star_Bots_Tamil'>Star Bots Tamil</a>. Click on /help to Get More Information.\n
Warning 🚸\n
🔞 Porn Contents Leads to Permanent Ban You. Check "About 😁"</b>"""

HELP_TEXT = """
<b>➠ Send Me Any Type of Documents From Telegram.
➠ I will Provide Permanent Direct Download Link, Watch / Stream Link & Shortened Link !
➠ Add me in Your Channel For Direct Download Link Button
➠ This Permanent Link with Fastest Download Speed.
➠ You Can Short Generated Link.\n
Available Commands\n
● /start - Check if 😊 I'm Alive
● /help - How to Use❓
● /about - to Know About Me 😌
● /short - Use This Command with Bot Generated Link 🔗 to Get Shorted Links 🔗\n
Warning ⚠️\n
🔞 Porn Contents Leads to Permanent Ban You.</b>"""

ABOUT_TEXT = """
<b><i>🤖 My Name :- <a href=https://t.me/File_to_Link_Star_Bot><b>File to Link Star Bots</b></a>\n
🧑🏻‍💻 Developer :- <a href=https://t.me/TG_Karthik><b>Karthik</b></a>\n
📝 Language :- Python3\n
📚 Framework :- Pyrogram\n
📡 Hosted on :- VPS\n
🎥 Movie Updates :- <a href=https://t.me/Star_Moviess_Tamil><b></b>Star Movies Tamil</a>\n
🤖 Bot Channel :- <a href=https://t.me/Star_Bots_Tamil><b></b>Star Bots Tamil</a></b></i>"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        [
        InlineKeyboardButton('👨🏻‍✈️ Devloper', user_id=OWNER_ID)
        ], 
        [
        InlineKeyboardButton('🤖 Bot Channel', url=f"https://t.me/Star_Bots_Tamil"),
        InlineKeyboardButton('🎥 Movie Updates', url='https://t.me/Star_Moviess_Tamil')        
        ],        
        InlineKeyboardButton('💁🏻 Help', callback_data='help'),
        InlineKeyboardButton('About 😁', callback_data='about')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        [
        InlineKeyboardButton('👨🏻‍✈️ Devloper', user_id=OWNER_ID)
        ], 
        [
        InlineKeyboardButton('🤖 Bot Channel', url=f"https://t.me/Star_Bots_Tamil"),
        InlineKeyboardButton('🎥 Movie Updates', url='https://t.me/Star_Moviess_Tamil')        
        ],        
        InlineKeyboardButton('About 😁', callback_data='about'),
        InlineKeyboardButton('🏠 Home', callback_data='home')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        [
        InlineKeyboardButton('👨🏻‍✈️ Devloper', user_id=OWNER_ID)
        ], 
        [
        InlineKeyboardButton('🤖 Bot Channel', url=f"https://t.me/Star_Bots_Tamil"),
        InlineKeyboardButton('🎥 Movie Updates', url='https://t.me/Star_Moviess_Tamil')        
        ],        
        InlineKeyboardButton('💁🏻 Help', callback_data='help'),
        InlineKeyboardButton('🏠 Home', callback_data='home')
        ]]
    )

@StreamBot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()

def get_media_file_size(m):
    media = m.video or m.audio or m.document
    if media and media.file_size:
        return media.file_size
    else:
        return None


def get_media_file_name(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)
    else:
        return None


@StreamBot.on_message(filters.command('start') & filters.private)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.LOG_CHANNEL,
            f"<b>#New_User_Joined\n\n᚛›Name :- <a href='tg://user?id={m.from_user.id}'>{m..first_name}</a>\n᚛› ID :- <code>{m.from_user.id}</code>\n᚛› From Bot :- <a href=https://t.me/File_to_Link_Star_Bot><b>File to Link Star Bots</b></a></b>"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="<b>Sorry <a href='tg://user?id={m.from_user.id}>{m..first_name}</a>,\nYou're Banned 🚫 To Use Me❓.\n\n Contact Developer <a href='https://t.me/Star_Bots_Tamil_Support'>Star Bots Tamil Support</a> They will Help You.</b>",
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i><b>Join Our Bot Channel to Use Me</b> 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Join Now 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]]
                    ),
                    parse_mode=ParseMode.HTML
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<b>Something Wrong❗\nYou're Not Added Admin to Update Channel.\n\n👥 Support :- <a href=https://t.me/Star_Bots_Tamil_Support><b>Star Bots Tamil Support</b></a></b>",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text=START_TEXT.format(m.from_user.mention),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
              )                                                                         
                                                                                       
                                                                            
    else:
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="<b>Sorry <a href='tg://user?id={m.from_user.id}>{m..first_name}</a>,\nYou're Banned 🚫 To Use Me❓.\n\n Contact Developer <a href='https://t.me/Star_Bots_Tamil_Support'>Star Bots Tamil Support</a> They will Help You.</b>",
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<b>Please Join Our Updates Channel to Use Me❗\n\nDue To Overload, Only Channel Subscribers Can Use to Me❗.</b>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                          InlineKeyboardButton("🤖 Join Our Bot Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")],
                         [InlineKeyboardButton("🔄 Refresh / Try Again", url=f"https://t.me/{(await b.get_me()).username}?start=Star_Bots_Tamil_{usr_cmd}")
                        
                        ]]
                    ),
                    parse_mode=ParseMode.HTML
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<b>Something Wrong❗\nYou're Not Added Admin to Update Channel.\n\n👥 Support :- <a href=https://t.me/Star_Bots_Tamil_Support><b>Star Bots Tamil Support</b></a></b>",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))
        file_name = get_media_file_name(get_msg)
        file_size = humanbytes(get_media_file_size(get_msg))
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


        await m.reply_text(
            text=msg_text.format(file_name, file_size, file_caption, stream_link, watch_link, short_link),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ 📥", url=stream_link)]])
        )



@StreamBot.on_message(filters.private & filters.command(["about"]))
async def start(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )


@StreamBot.on_message(filters.command('help') & filters.private)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"<b>#New_User_Joined\n\n᚛›Name :- <a href='tg://user?id={m.from_user.id}'>{m..first_name}</a>\n᚛› ID :- <code>{m.from_user.id}</code>\n᚛› From Bot :- <a href=https://t.me/File_to_Link_Star_Bot><b>File to Link Star Bots</b></a></b>"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="<b>Sorry <a href='tg://user?id={m.from_user.id}>{m..first_name}</a>,\nYou're Banned 🚫 To Use Me❓.\n\n Contact Developer <a href='https://t.me/Star_Bots_Tamil_Support'>Star Bots Tamil Support</a> They will Help You.</b>",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>Please Join Our Updates Channel to Use Me❗\n\nDue To Overload, Only Channel Subscribers Can Use to Me❗.</b>",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("🤖 Join Our Bot Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]]
                ),
                parse_mode=ParseMode.HTML
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>Something Wrong❗\nYou're Not Added Admin to Update Channel.\n\n👥 Support :- <a href=https://t.me/Star_Bots_Tamil_Support><b>Star Bots Tamil Support</b></a></b>",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text=HELP_TEXT,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS
        )
