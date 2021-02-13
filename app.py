import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher
from telegram import Update, Bot, ReplyKeyboardMarkup, Message
from utils import get_reply, fetch_news, topics_keyboard

# Enable Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "1649580039:AAHavD4FZpNr1L0NLiSgRrnkm9U2USIrmmM"

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello!"


@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "ok"


def start(update: Update, context: CallbackContext):
    fname = update.to_dict()['message']['chat']['first_name']
    reply = "Hi! {}".format(fname)
    update.message.reply_text(reply)


def help(update: Update, context: CallbackContext):
    help_text = "Dude, Don't Worry I'm always here to help you."
    update.message.reply_text(help_text)


def news(update: Update, context: CallbackContext):
    update.message.reply_text(text="Choose a category",
                              reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))


def reply_text(update: Update, context: CallbackContext):
    intent, reply = get_reply(
        update.to_dict()['message']['text'], update.message.chat_id)

    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            update.message.reply_text(article['link'])
    else:
        update.message.reply_text(reply)


def echo_sticker(update: Update, context: CallbackContext):
    reply = update.message.sticker.file_id
    update.message.reply_sticker(reply)


def error(bot, update):
    logger.error("Update {} caused error {}".format(update, update.error))


bot = Bot(TOKEN)
try:
    bot.set_webhook("https://newstoymanbot.herokuapp.com/" + TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot, None)

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_handler(MessageHandler(Filters.text, reply_text))

dp.add_error_handler(error)


if __name__ == "__main__":
    app.run(port=8443)
