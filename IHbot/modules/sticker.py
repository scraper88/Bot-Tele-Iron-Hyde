import hashlib
import os
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import TelegramError
from telegram import Update, Bot
from telegram.ext import CommandHandler, run_async
from telegram.utils.helpers import escape_markdown

from IHbot import dispatcher
from IHbot.modules.disable import DisableAbleCommandHandler

@run_async
def stickerid(update: Update):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text("Hello " +
                                            "[{}](tg://user?id={})".format(msg.from_user.first_name, msg.from_user.id)
                                            + ", The sticker id you are replying is :\n```" + 
                                            escape_markdown(msg.reply_to_message.sticker.file_id) + "```",
                                            parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text("Hello " + "[{}](tg://user?id={})".format(msg.from_user.first_name,
                                            msg.from_user.id) + ", Please reply to sticker message to get id sticker",
                                            parse_mode=ParseMode.MARKDOWN)

@run_async
def getsticker(bot: Bot, update: Update):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text("Hello " + "[{}](tg://user?id={})".format(msg.from_user.first_name,
                                            msg.from_user.id) + ", Please check the file you requested below."
                                            "\nPlease use this feature wisely!",
                                            parse_mode=ParseMode.MARKDOWN)
        bot.sendChatAction(chat_id, "upload_document")
        file_id = msg.reply_to_message.sticker.file_id
        newFile = bot.get_file(file_id)
        newFile.download('sticker.png')
        bot.send_document(chat_id, document=open('sticker.png', 'rb'))
        os.remove("sticker.png")

    else:
        bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text("Hello " + "[{}](tg://user?id={})".format(msg.from_user.first_name,
                                            msg.from_user.id) + ", Please reply to sticker message to get sticker image",
                                            parse_mode=ParseMode.MARKDOWN)

@run_async
def kang(bot: Bot, update: Update):
    msg = update.effective_message
    user = update.effective_user
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        kang_file = bot.get_file(file_id)
        kang_file.download('kangsticker.png')
        hash = hashlib.sha1(bytearray(user.id)).hexdigest()
        packname = "a" + hash[:20] + "_by_"+bot.username
        if msg.reply_to_message.sticker.emoji:
            sticker_emoji = msg.reply_to_message.sticker.emoji
        else:
            sticker_emoji = "🤔"
        try:
            bot.add_sticker_to_set(user_id=user.id, name=packname,
                                   png_sticker=open('kangsticker.png', 'rb'), emojis=sticker_emoji)
            os.remove("kangsticker.png")
            msg.reply_text("Sticker successfully added to [pack](t.me/addstickers/%s)" % packname,
                           parse_mode=ParseMode.MARKDOWN)
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                msg.reply_text("Use /makepack to create a pack first.")
            print(e)
    else:
        msg.reply_text("Please reply to a sticker for me to kang it.")


@run_async
def makepack(bot: Bot, update: Update):
    msg = update.effective_message
    user = update.effective_user
    name = user.first_name
    name = name[:50]
    hash = hashlib.sha1(bytearray(user.id)).hexdigest()
    packname = "a" + hash[:20] + "_by_"+bot.username
    try:
        success = bot.create_new_sticker_set(user.id, packname, name + "'s kang pack",
                                             png_sticker="https://images.emojiterra.com/google/android-pie/512px/1f914.png",
                                             emojis="🤔")
    except TelegramError as e:
        print(e)
        if e.message == "Sticker set name is already occupied":
            msg.reply_text("Your pack can be found [here](t.me/addstickers/%s)" % packname,
                           parse_mode=ParseMode.MARKDOWN)
        elif e.message == "Peer_id_invalid":
            msg.reply_text("Contact me in PM first.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                text="Start", url="t.me/{}".format(bot.username))]]))
        return

    if success:
        msg.reply_text("Sticker pack successfully created. Get it [here](t.me/addstickers/%s)" % packname,
                       parse_mode=ParseMode.MARKDOWN)
    else:
        msg.reply_text("Failed to create sticker pack. Possibly due to blek mejik.")

__help__ = """
- /stickerid: reply to a sticker to me to tell you its file ID.
- /getsticker: reply to a sticker to me to upload its raw PNG file.
- /makepack: create a sticker pack that's tied to your telegram account (only one can be made at a time)
- /kang: reply to a sticker to add it to the created pack.
"""

__mod_name__ = "Sticker"

STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker)
MAKEPACK_HANDLER = DisableAbleCommandHandler("makepack", makepack)
KANG_HANDLER = DisableAbleCommandHandler("kang", kang)

dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(MAKEPACK_HANDLER)
dispatcher.add_handler(KANG_HANDLER)