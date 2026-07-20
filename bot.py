import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

import config
from utils import get_product_info
from logger import amzn_bot_logger


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="⭐️ Hello there! \nI am an Amazon advertising bot, designed to assist you in managing your Amazon advertising campaigns efficiently. \n\n",
    )


async def amazon_url_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    message = update.effective_message
    chat = update.effective_chat

    if message is None or message.text is None or chat is None:
        amzn_bot_logger.warning(
            "Received a text update without an accessible message or chat."
        )
        return

    URL = message.text
    text = message.text

    amzn_bot_logger.info("A new request came...")
    amzn_bot_logger.info(f"Chat ID -> {chat.id}")
    amzn_bot_logger.info(f"Message -> {text}")

    try:
        url, image_url, name, price, discount_price, percentage = get_product_info(text)
        if price == 0.0:
            price = "controlla il prezzo sulla pagina del prodotto."
        else:
            price = f"{float(price):.2f}"
        emoji = random.choice(
            ["🔥", "⏰", "🚨", "🌋", "👻", "🤡", "👾", "🤖", "👽", "⚠️"]
        )
        text = f"{emoji} <b> {name[:40]}..."
        discounted_price_text = str(price).replace(".", ",")
        if discount_price == 0.0:
            original_price_text = discounted_price_text
        else:
            original_price_text = f"{float(price) + float(discount_price):.2f}".replace(
                ".", ","
            )
        text += f"\n\n💰 {discounted_price_text}€ </b>invece di <b>{original_price_text}€ </b>"
        if discount_price == 0.0:
            text += "\n"
            text += random.choice(
                [
                    "☘️ un ottimo prodotto",
                    "🐺 item gagliardo",
                    "😆 merita anche senza sconto",
                    "🤔 e se..",
                    "🧙‍♂️ quasi magico",
                    "👽 extraterrestre",
                    "👾 superlativo",
                    "🙌 da mani alzate",
                    "👀 sotto osservazione",
                    "🥷 mitico come un ninja",
                    "🧞‍♂️ gagliardo come il genio",
                ]
            )
        else:
            discount_price = f"{float(discount_price):.2f}"
            text += f"\n✂️ <i>risparmi {str(discount_price).replace('.', ',')}€ ({int(percentage)}%) </i>"

        text += f"""\n\n<a href="{url}">➡️ Offerta Amazon</a>"""

        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="🚀 Scopri l'offerta", url=url)]]
        )

        await context.bot.send_photo(
            chat_id=chat.id,
            photo=image_url,
            caption=text,
            reply_markup=button,
            parse_mode="HTML",
        )
        await context.bot.send_photo(
            chat_id=config.CHANNEL_ID,
            photo=image_url,
            caption=text,
            reply_markup=button,
            parse_mode="HTML",
        )
    except Exception as e:
        amzn_bot_logger.error(e)
        await context.bot.send_message(
            chat_id=chat.id, text=f"The URL -> {URL} is invalid, please check the URL."
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    amzn_bot_logger.exception(
        "Unhandled exception in update processing", exc_info=context.error
    )

    if isinstance(update, Update) and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="We are facing an issue, please try after sometime.",
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), amazon_url_handler)
    )
    application.add_error_handler(error_handler)

    application.run_polling(timeout=20)
