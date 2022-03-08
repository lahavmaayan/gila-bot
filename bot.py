import os

import psycopg2
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


def start(update, context):
    conn, cur = create_connection()
    chat_id = update.effective_chat.id
    # insert into first last question
    # sql_query = INSERT_DEFAULT_LAST_QUESTION.format(CHAT_ID=chat_id)
    select_query = f"SELECT question FROM public.questions where id = (SELECT last_question_id+1 from public.state where chat_id = {chat_id})"
    context.bot.send_message(chat_id=chat_id, text=select_query)
    cur.execute(select_query)
    res = cur.fetchone()[0]
    context.bot.send_message(chat_id=chat_id, text=res)

    close_connection(conn, cur)

    context.bot.send_message(chat_id=chat_id, text=FIRST_QUESTION)


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
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    return conn, cur


def close_connection(conn, cur):
    cur.close()
    conn.close()




# run the start function when the user invokes the /start command
dispatcher.add_handler(CommandHandler("start", start))

# invoke the get_word_info function when the user sends a message
# that is not a command.
dispatcher.add_handler(MessageHandler(Filters.text, conversation))
updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path=telegram_bot_token,
                      webhook_url='https://gila-the-bot.herokuapp.com/' + telegram_bot_token)