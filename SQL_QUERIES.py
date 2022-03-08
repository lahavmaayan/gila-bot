GET_QUESTION_BY_CHAT_ID = """
SELECT public.question FROM public.questions where id = (SELECT last_question_id+1 from public.state where chat_id = {CHAT_ID})
"""

UPDATE_LAST_QUESTION = """
UPDATE public.state set last_question_id = (SELECT last_question_id+1 from public.state where chat_id = {CHAT_ID}) 
WHERE chat_id = {CHAT_ID}
"""

INSERT_DEFAULT_LAST_QUESTION = "INSERT INTO public.state (chat_id, last_question_id) VALUES ({CHAT_ID}, 1)"

INSERT_ANSWER = """
INSERT INTO public.users_answers (chat_id, question_id, answer_id) VALUES ({CHAT_ID}, {QUESTION_ID}, 
(SELECT answer_id from public.answers WHERE question_id = {QUESTION_ID} and display_id = {USER_ANSWER})
"""