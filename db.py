import sqlite3
from os.path import isfile
import openai
from asyncio import Lock
import prompt # has "intro" which has the content for setting up the bot


def connect(db_name):
    """Initializes sqlite3 connection (opens file, creates db if it doesn't exist)"""
    create_db = not isfile(db_name)
    con = sqlite3.connect(db_name)
    if create_db:
        cursor = con.cursor()
        cursor.execute('CREATE TABLE chat (role, content, user_id)')
        cursor.executemany('INSERT INTO chat VALUES (?, ?, ?)', prompt.intro)
        con.commit()
    return con

def format_chat_results(results):
    """Converts sqlite3 results to openai friendly format"""
    return [ {"role": role, "content": content} for role, content, _user_id in results]

# Prevent concurrent access to sqlite DB
sqlite3_lock = Lock()
async def get_reply(db_con, prompt, prompter_id, api_key):
    """Gets reply for user"""
    # Get lock for DB interaction
    await sqlite3_lock.acquire()
    answer = ''
    try:
        cursor = db_con.cursor()
        # Get global history start
        setup = cursor.execute('SELECT * FROM chat WHERE user_id = 0').fetchall()
        msg_history = format_chat_results(setup)
        # Append history of prompt user to msg_history
        user_history = cursor.execute('SELECT * FROM chat WHERE user_id = ?', [prompter_id])
        msg_history = msg_history + format_chat_results(user_history)
        msg_history.append({"role":"user", "content": prompt})
        # Make OpenAI API call
        openai.api_key = api_key
        results = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=msg_history
        )
        answer = results.choices[0].message.content
        # Update DB
        cursor.executemany('INSERT INTO chat VALUES (?, ?, ?)', [("user", prompt, prompter_id), ("assistant", answer, prompter_id)])
        db_con.commit()
    except Exception as err:
        print(f"[SYSTEM] Error occured: \"{err}\"")
    finally:
        sqlite3_lock.release()
    return answer