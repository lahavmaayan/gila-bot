import os

import psycopg2
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from SQL_QUERIES import INSERT_DEFAULT_LAST_QUESTION, GET_QUESTION_BY_CHAT_ID, UPDATE_LAST_QUESTION, INSERT_ANSWER, \
    GET_LAST_QUESTION_ID, UPDATE_USER_NAME

FIRST_QUESTION = """
Hello there, my name is Gila, I’m your Bot-pal in these uncertain times of menopausal and peri menopausal phases.
Unsure what you’re going through? I’m here for you
Before we start, please tell me your name :)
"""

DATABASE_URL = os.environ['DATABASE_URL']
telegram_bot_token = "5235401334:AAFC3AOzKzR_pK6dPHLRMQhkGOwi8YLbWm0"

LAST_QUESTION_ID = 7

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    conn, cur = create_connection()
    chat_id = update.effective_chat.id

    sql_query = INSERT_DEFAULT_LAST_QUESTION.format(CHAT_ID=chat_id)
    cur.execute(sql_query)
    conn.commit()
    close_connection(conn, cur)

    context.bot.send_message(chat_id=chat_id, text=FIRST_QUESTION)


def conversation(update, context):
    conn, cur = create_connection()
    chat_id = update.effective_chat.id
    parsed_user_response = _parse_response(update.message.text)

    last_question = _get_last_question_id(chat_id, cur)
    should_skip_insert_answer = False
    if last_question == 0:
        _save_name_handler(context, chat_id, parsed_user_response, cur)
        should_skip_insert_answer = True
    if last_question == LAST_QUESTION_ID:
        return handle_matching(chat_id, conn, cur, update)

    send_next_question(chat_id, cur, update)

    update_db(chat_id, conn, cur, parsed_user_response, context, should_skip_insert_answer)

    close_connection(conn, cur)


def _save_name_handler(context, chat_id, parsed_user_response, cur):
    update_name = UPDATE_USER_NAME.format(NAME=parsed_user_response[0], CHAT_ID=chat_id)
    cur.execute(update_name)

    context.bot.send_message(chat_id=chat_id, text=f"Nice to meet you {parsed_user_response[0]}! :)")


def _get_last_question_id(chat_id, cur):
    last_question_id = GET_LAST_QUESTION_ID.format(CHAT_ID=chat_id)
    cur.execute(last_question_id)
    res = cur.fetchone()[0]
    return res


def handle_matching(chat_id, conn, cur, update):
    update.message.reply_text("Matching!")
    close_connection(conn, cur)


def update_db(chat_id, conn, cur, user_response, context, should_skip_insert_answer):
    # This function insert the user's answers + update the last question id in the state.
    if not should_skip_insert_answer:
        for res in user_response:
            update_query = INSERT_ANSWER.format(CHAT_ID=chat_id, ANSWER_DISPLAY_ID=int(res.strip()))
            cur.execute(update_query)

    query = UPDATE_LAST_QUESTION.format(CHAT_ID=chat_id)
    cur.execute(query)
    conn.commit()


def send_next_question(chat_id, cur, update):
    # This function send the parsed response

    select_query = GET_QUESTION_BY_CHAT_ID.format(CHAT_ID=chat_id)
    cur.execute(select_query)
    results = cur.fetchall()
    answers = []
    question = None
    for row in results:
        if question is None:
            question = row[0]
        answers.append(row[1])

    response = _prepare_response(question, answers)
    update.message.reply_text(response)


def _parse_response(message):
    return message.split(",")


def _prepare_response(question, answers):
    response = f"{question}\n"
    for index, answer in enumerate(answers):
        response += f"{index+1}. {answer}\n"
    response += "\nPlease write down the number corresponding to your answer. If you pick 2 or more - write your " \
                "answers like this: 1,2,3\n "
    return response


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