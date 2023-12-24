import logging
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import config
from utils import get_product_info

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="⭐️ Hello there! \nI am an Amazon advertising bot, designed to assist you in managing your Amazon advertising campaigns efficiently. \n\n")


async def amazon_url_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # if not update.effective_chat.id == config.ADMIN_ID:
    #     return await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this bot")

    text = update.message.text
    url, image_url, name, price, discount_price, percentage = get_product_info(
        text)
    price = f"{float(price):.2f}"
    discount_price = f"{float(discount_price):.2f}"

    my_list = ["🔥", "⏰", "🚨", "🌋", "👻", "🤡", "👾", "🤖", "👽", "⚠️"]
    emoji = random.choice(my_list)
    text = f"{emoji} <b> {name[:40]}..."
    text += f"\n\n💰 {str(price).replace('.',',')}€ </b>"
    text += f"\n✂️ <i>risparmi {str(discount_price).replace('.',',')}€ ({percentage}%) </i>"
    text += f"""\n\n<a href="{url}">➡️ Offerta Amazon</a>"""

    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="🚀 Scopri l'offerta", url=url)]])

    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo=image_url, caption=text, reply_markup=button, parse_mode="HTML")
    await context.bot.send_photo(chat_id=config.CHANNEL_ID, photo=image_url,
                                 caption=text, reply_markup=button, parse_mode="HTML")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="We are facing an issue, please try after sometime.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), amazon_url_handler))
    application.add_error_handler(error_handler)

    application.run_polling(timeout=20)
