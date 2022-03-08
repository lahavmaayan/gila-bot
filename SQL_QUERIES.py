GET_QUESTION_BY_CHAT_ID = """
SELECT question, a.answer, a.display_id FROM public.questions q
join answers a on q.id = a.question_id
where q.id = (SELECT last_question_id+1 from public.state where chat_id = {CHAT_ID})
order by a.display_id
"""

UPDATE_LAST_QUESTION = """
UPDATE public.state set last_question_id = (SELECT last_question_id+1 from public.state where chat_id = {CHAT_ID}) 
WHERE chat_id = {CHAT_ID}
"""

INSERT_DEFAULT_LAST_QUESTION = "INSERT INTO public.state (chat_id, last_question_id) VALUES ({CHAT_ID}, 0)"

INSERT_ANSWER = """
INSERT INTO public.users_answers (chat_id, question_id, answer_id)
VALUES
       ({CHAT_ID},
        (select last_question_id from public.state where state.chat_id = {CHAT_ID}),
       (SELECT id from public.answers WHERE question_id = (select last_question_id from public.state where state.chat_id = {CHAT_ID})
       and display_id = {ANSWER_DISPLAY_ID}));
"""

GET_LAST_QUESTION_ID = "SELECT last_question_id FROM public.state where chat_id = {CHAT_ID}"

UPDATE_USER_NAME = "UPDATE public.state SET name = '{NAME}' WHERE chat_id = {CHAT_ID}"

GET_USER_NAME = "SELECT name from public.state where chat_id = {CHAT_ID}"

