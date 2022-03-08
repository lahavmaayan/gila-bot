import os

import telegram
from telethon import types
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler

# QUESTIONS = ["First", "second", "third"]
# LAST_QUESTION = None

selected = []

DATABASE_URL = os.environ['DATABASE_URL']

telegram_bot_token = "5235401334:AAFC3AOzKzR_pK6dPHLRMQhkGOwi8YLbWm0"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    chat_id = update.effective_chat.id
    # TODO: change the text
    # context.bot.send_message(chat_id=chat_id, text="Hello there. My name is Gila! I'm your bot :)")
    context.bot.send_message(
        update.chat_id,
        file=types.InputMediaPoll(
            poll=types.Poll(
                id=1,
                question="This is a test poll",
                answers=[types.PollAnswer('Option 1', b'1'), types.PollAnswer('Option 2', b'2'), types.PollAnswer('Option 3', b'3')],
                multiple_choice=True
            )))

# def _fetch_question():
#     if LAST_QUESTION is None:
#         LAST_QUESTION = 0
#         return


# obtain the information of the word provided and format before presenting.
def get_word_info(update, context):
    chat_id = update.effective_chat.id
    # current_question = QUESTIONS[0]

    message = f"Word: hello\n\nOrigin: Gila\n"
    global selected
    selected += {update.message.text}

    update.message.reply_text(f"This was the reply: {update.message.text}, {chat_id}")




# run the start function when the user invokes the /start command
dispatcher.add_handler(CommandHandler("start", start))

# invoke the get_word_info function when the user sends a message
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, get_word_info))
updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path=telegram_bot_token,
                      webhook_url='https://gila-the-bot.herokuapp.com/' + telegram_bot_token)