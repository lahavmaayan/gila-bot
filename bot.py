import os

import psycopg2
import telegram
from telethon import types
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from SQL_QUERIES import INSERT_DEFAULT_LAST_QUESTION, GET_QUESTION_BY_CHAT_ID

FIRST_QUESTION = """
Hello there,  my name is Gila! I'm your bot :)
How are you doing today?
Please choose the number corresponding to your response: 
1. Great
2. Fine
3. So so
4. Not very well
5. Horrible
"""

DATABASE_URL = os.environ['DATABASE_URL']
telegram_bot_token = "5235401334:AAFC3AOzKzR_pK6dPHLRMQhkGOwi8YLbWm0"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


# set up the introductory statement for the bot when the /start command is invoked
def start(update, context):
    con, cur = create_connection()
    try:
        chat_id = update.effective_chat.id
        # insert into first last question
        sql_query = INSERT_DEFAULT_LAST_QUESTION.format(CHAT_ID=int(chat_id))
        context.bot.send_message(chat_id=chat_id, text=sql_query)
        cur.execute(sql_query)
        context.bot.send_message(chat_id=chat_id, text=FIRST_QUESTION)
    finally:
        close_connection(con, cur)


def conversation(update, context):
    con, cur = create_connection()
    try:
        chat_id = update.effective_chat.id
        response = _parse_response(update.message.text)

        # Get next question

        # Verify not the last question

        # Update in the DB



        select_query = GET_QUESTION_BY_CHAT_ID.format(CHAT_ID=chat_id)
        question = cur.fetchone()[0]

    except:
        update.message.reply_text(f"An error occurred, sorry")
    finally:
        close_connection(con, cur)

    update.message.reply_text(f"This was the reply: {update.message.text}, {chat_id}")


def _parse_response(message):
    return message.split(",")


def create_connection():
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    return con, cur


def close_connection(con, cur):
    cur.close()
    con.close()




# run the start function when the user invokes the /start command
dispatcher.add_handler(CommandHandler("start", start))

# invoke the get_word_info function when the user sends a message
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, conversation))
updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path=telegram_bot_token,
                      webhook_url='https://gila-the-bot.herokuapp.com/' + telegram_bot_token)