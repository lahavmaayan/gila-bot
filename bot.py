import os

import telegram
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler


telegram_bot_token = "5235401334:AAFC3AOzKzR_pK6dPHLRMQhkGOwi8YLbWm0"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    chat_id = update.effective_chat.id
    # TODO: change the text
    context.bot.send_message(chat_id=chat_id, text="Hello there. My name is Gila! I'm your bot :)")


# obtain the information of the word provided and format before presenting.
def get_word_info(update, context):
    chat_id = update.effective_chat.id

    message = f"Word: hello\n\nOrigin: Gila\n"

    update.message.reply_text(f"This was the reply: {update.message.text}")


# run the start function when the user invokes the /start command
dispatcher.add_handler(CommandHandler("start", start))

# invoke the get_word_info function when the user sends a message
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, get_word_info))
updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path=telegram_bot_token,
                      webhook_url='https://gila-the-bot.herokuapp.com/' + telegram_bot_token)