from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery
from WebStreamer.vars import Var 
from WebStreamer.bot import StreamBot
from pyrogram.enums.parse_mode import ParseMode
import aiofiles
from WebStreamer.handlers.broadcast import broadcast
from WebStreamer.handlers.database import Database
from WebStreamer.handlers.check_user import handle_user_status
LOG_CHANNEL = Var.LOG_CHANNEL
AUTH_USERS = Var.AUTH_USERS
DB_URL = Var.DB_URL
DB_NAME = Var.DB_NAME
OWNER_ID = Var.OWNER_ID
OWNER_ID = Var.OWNER_ID
db = Database(DB_URL, DB_NAME)

STAR_BUTTONS = [
            [
                InlineKeyboardButton('👨🏻‍💻 Creator', user_id=OWNER_ID)
            ],
            [
                InlineKeyboardButton('🤖 Bot Channel', url='https://t.me/Star_Bots_Tamil'),                        
                InlineKeyboardButton('👥 Support Group', url='https://t.me/Star_Bots_Tamil_Support')
            ]
        ]

@StreamBot.on_message(filters.private)
async def _(bot, cmd):
    await handle_user_status(bot, cmd)

    chat_id = cmd.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"**#New_User :- \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n ID :- {message.from_user.id} Started @{BOT_USERNAME} !!**",
            )
        else:
            logging.info(f"New User :- Name :- {message.from_user.first_name} ID :- {message.from_user.id}")


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


@StreamBot.on_message(filters.private & filters.command("broadcast"))
async def broadcast_handler_open(_, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if m.reply_to_message is None:
        await m.reply(REPLY_ERROR, quote=True)
    else:
        await broadcast(m, db)

@StreamBot.on_message(filters.private & filters.command("stats"))
async def sts(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    await m.reply_text(
        text=f"**Total Users in Database 📂 :- {await db.total_users_count()}**",
        quote=True
    )            

@StreamBot.on_message(filters.private & filters.command("ban"))
async def ban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban 🛑 any user from the bot 🤖.\n\nUsage:\n\n`/ban_user user_id ban_duration ban_reason`\n\nEg: `/ban_user 1234567 28 You misused me.`\n This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = " ".join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."

        try:
            await c.send_message(
                user_id,
                f"You are Banned 🚫 to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin 🤠**",
            )
            ban_log_text += "\n\nUser notified successfully!"
        except BaseException:
            traceback.print_exc()
            ban_log_text += (
                f"\n\n ⚠️ User notification failed! ⚠️ \n\n`{traceback.format_exc()}`"
            )
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(ban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )
            
@StreamBot.on_message(filters.private & filters.command("unban"))
async def unban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban 😃 any user.\n\nUsage:\n\n`/unban_user user_id`\n\nEg: `/unban_user 1234567`\n This will unban user with id `1234567`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user 🤪 {user_id}"

        try:
            await c.send_message(user_id, f"Your ban was lifted!")
            unban_log_text += "\n\n✅ User notified successfully! ✅"
        except BaseException:
            traceback.print_exc()
            unban_log_text += (
                f"\n\n⚠️ User notification failed! ⚠️\n\n`{traceback.format_exc()}`"
            )
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(unban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"⚠️ Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True,
        )
@StreamBot.on_message(filters.private & filters.command("banned"))
async def _banned_usrs(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ""
    async for banned_user in all_banned_users:
        user_id = banned_user["id"]
        ban_duration = banned_user["ban_status"]["ban_duration"]
        banned_on = banned_user["ban_status"]["banned_on"]
        ban_reason = banned_user["ban_status"]["ban_reason"]
        banned_usr_count += 1
        text += f"> **User_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, **Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s) 🤭: `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open("banned-users.txt", "w") as f:
            f.write(reply_text)
        await m.reply_document("banned-users.txt", True)
        os.remove("banned-users.txt")
        return
    await m.reply_text(reply_text, True)
           
            
