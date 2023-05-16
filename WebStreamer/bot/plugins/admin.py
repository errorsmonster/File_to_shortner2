import os
import aiohttp
import time
import string
import random
import asyncio
import aiofiles
import datetime
from WebStreamer.utils.broadcast import send_msg
from WebStreamer.utils.database import Database
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from pyshorteners import Shortener
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.handlers import MessageHandler
from pyrogram import filters, Client, enums
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)
broadcast_ids = {}


@StreamBot.on_message(filters.command("stats") & filters.private & filters.user(Var.OWNER_ID))
async def sts(c: Client, m: Message):
    total_users = await db.total_users_count()
    await m.reply_text(text=f"<b>Total Users in Database :-</b> <code>{total_users}</code>", parse_mode=ParseMode.HTML, quote=True)


@StreamBot.on_message(filters.command("broadcast") & filters.private & filters.user(Var.OWNER_ID) & filters.reply)
async def broadcast_(c, m):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    out = await m.reply_text(
        text=f"<b>Broadcast Initiated! You will be Notified With Log File When all the Users are Notified.</b>"
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(
        total=total_users,
        current=done,
        failed=failed,
        success=success
    )
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(
                user_id=int(user['id']),
                message=broadcast_msg
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(
                        current=done,
                        failed=failed,
                        success=success
                    )
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await m.reply_text(
            text=f"<b>broadcast Completed in <code>{completed_in}</code>\n\nTotal Users 📊 :- {total_users}\nTotal Done ✅ :- {done}\nSuccessfully Sended Users :- {success}\nFailed Users :- {failed}</b>",
            quote=True
        )
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=f"<b>broadcast Completed in <code>{completed_in}</code>\n\nTotal Users 📊 :- {total_users}\nTotal Done ✅ :- {done}\nSuccessfully Sended Users :- {success}\nFailed Users :- {failed}</b>",
            quote=True
        )
    os.remove('broadcast.txt')
    
BITLY_API = os.environ.get("BITLY_API", "aa2132168583d283fb288625d9352f2c5835512a")
CUTTLY_API = os.environ.get("CUTTLY_API", "bd3a3ab946d7598ee459331dac9e9568e3d66")
EZ4SHORT_API = os.environ.get("EZ4SHORT_API", "e41618d805b3c4256dfa99abde6ef11fc7629c47")
TINYURL_API = os.environ.get("TINYURL_API", "iRkhyhlmfJ07cFVsFV0NpvX6dOWZIwPglbq8jQDuSBMqAEk5Y81BX04ejVQk")
DROPLINK_API = os.environ.get("DROPLINK_API", "1d85e33efc4969b36e0f6c0a017aaaefd8accccc")
TNSHORT_API = os.environ.get("TNSHORT_API", "d03a53149bf186ac74d58ff80d916f7a79ae5745")

reply_markup = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🎥 Movie Updates', url='https://t.me/Star_Moviess_Tamil')
        ],
        [
        InlineKeyboardButton('🤖 Bot Channel', url=f"https://t.me/Star_Bots_Tamil"),
        ],
        [
        InlineKeyboardButton('⚡ Request', user_id=OWNER_ID),
        ],
        [
        InlineKeyboardButton('🚫 Close', callback_data='close_data')
        ]]
    )

@Client.on_message(filters.command(["short"]) & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    message = await update.reply_text(
        text="**Analysing Your Link...**",
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )
    link = update.matches[0].group(0)
    shorten_urls = await short(link)
    await message.edit_text(
        text=shorten_urls,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@Client.on_inline_query(filters.regex(r'https?://[^\s]+'))
async def inline_short(bot, update):
    link = update.matches[0].group(0),
    shorten_urls = await short(link)
    answers = [
        InlineQueryResultArticle(
            title="Short Links",
            description=update.query,
            input_message_content=InputTextMessageContent(
                message_text=shorten_urls,
                disable_web_page_preview=True
            ),
            reply_to_message_id=message.id
        )
    ]
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )

async def short(link):
    shorten_urls = "**--Shortened URLs--**\n"
    
    # Bit.ly Shortener
    if BITLY_API:
        try:
            s = Shortener(api_key=BITLY_API)
            url = s.bitly.short(link)
            shorten_urls += f"\n**Bit.ly :- {url}**\n"
        except Exception as error:
            print(f"Bit.ly Error :- {error}")
        
    # Clck.ru Shortener
    try:
        s = Shortener()
        url = s.clckru.short(link)
        shorten_urls += f"\n**Clck.ru :- {url}**\n"
    except Exception as error:
        print(f"Click.ru Error :- {error}")
    
    # Cutt.ly Shortener
    if CUTTLY_API:
        try:
            s = Shortener(api_key=CUTTLY_API)
            url = s.cuttly.short(link)
            shorten_urls += f"\n**Cutt.ly :- {url}**\n"
        except Exception as error:
            print(f"Cutt.ly Error :- {error}")
    
    # Da.gd Shortener
    try:
        s = Shortener()
        url = s.dagd.short(link)
        shorten_urls += f"\n**Da.gd :- {url}**\n"
    except Exception as error:
        print(f"Da.gd Error :- {error}")
    
    # Is.gd Shortener
    try:
        s = Shortener()
        url = s.isgd.short(link)
        shorten_urls += f"\n**Is.gd :- {url}**\n"
    except Exception as error:
        print(f"Is.gd Error :- {error}")
    
    # Osdb.link Shortener
    try:
        s = Shortener()
        url = s.osdb.short(link)
        shorten_urls += f"\n**Osdb.link :- {url}**\n"
    except Exception as error:
        print(f"Osdb.link Error :- {error}")
                
    # Droplink.co Shortener
    try:
        api_url = "https://droplink.co/api" 
        params = {'api': DROPLINK_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**DropLink.co :- {url}**\n"
    except Exception as error:
        print(f"Droplink.co Error :- {error}")

    # TNShort.net Shortener
    try:
        api_url = "https://tnshort.net/api" 
        params = {'api': TNSHORT_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**TNShort.net :- {url}**\n"
    except Exception as error:
        print(f"TNShort.net Error :- {error}")

    # TinyURL.com Shortener
    try:
        s = Shortener(api_key=TINYURL_API)
        url = s.tinyurl.short(link)
        shorten_urls += f"\n**TinyURL.com :- {url}**\n"
    except Exception as error:
        print(f"TinyURL.com Error :- {error}")
    
    # Ez4short.com Shortener
    try:
        api_url = "https://ez4short.com/api" 
        params = {'api': EZ4SHORT_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**Ez4short.com :- {url}**\n"
    except Exception as error:
        print(f"Ez4short.com Error :- {error}")

   
    # Send the text
    try:
        shorten_urls += ""
        return shorten_urls
    except Exception as error:
        return error    
