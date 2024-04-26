import aiosqlite
import os


#создает запись о регистрации
#registration
async def register_to_bot(id_tg,username_tg,date):
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect('C:/Users/user/Desktop/neuro/ooba_tg_bot/DB/bot_db.db') as db:
        await db.execute('INSERT INTO users (id_tg,username_tg,date) VALUES (?, ?, ?)', 
                        (id_tg,username_tg,date))
        await db.commit()

#создает запись о истории чата
#create new chat history
async def new_chat_history(id_tg,username_tg,character,chat_history,date):
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect('C:/Users/user/Desktop/neuro/ooba_tg_bot/DB/bot_db.db') as db:
        await db.execute('INSERT INTO user_chats (id_tg,username_tg,character,chat_history,date) VALUES (?, ?, ?, ?, ?)', 
                        (id_tg,username_tg,character,chat_history,date))
        await db.commit()

async def select_from_chat_history(id_tg, chat_history):
    async with aiosqlite.connect('C:/Users/user/Desktop/neuro/ooba_tg_bot/DB/bot_db.db') as db:
        cursor = await db.cursor()
        await cursor.execute('SELECT * FROM user_chats WHERE id_tg = ? and chat_history = ?', (id_tg, chat_history,))
        return await cursor.fetchone()

#/history
async def select_from_chat_history_command(id_tg):
    async with aiosqlite.connect('C:/Users/user/Desktop/neuro/ooba_tg_bot/DB/bot_db.db') as db:
        cursor = await db.cursor()
        await cursor.execute('SELECT * FROM user_chats WHERE id_tg = ?', (id_tg,))
        result = await cursor.fetchall()
        return result

#удаление истории чата
#delete chat history
async def close_chat(id_tg,chat_history,date):
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    if os.path.exists(f"C:/Users/user/Desktop/neuro/ooba_tg_bot/data/{chat_history}"):
        async with aiosqlite.connect('C:/Users/user/Desktop/neuro/ooba_tg_bot/DB/bot_db.db') as db:
            cursor = await db.cursor()
            await cursor.execute('UPDATE user_chats SET date_end = ? WHERE  id_tg = ? and chat_history = ?', (date,id_tg,chat_history))
            await db.commit()
            os.remove(f"C:/Users/user/Desktop/neuro/ooba_tg_bot/data/{chat_history}")
            return "Чат очищен"
    else:
        return "Чата нет"

#селект из таблицы с персонажами
#select from characters list
async def select_from_character_list():
    async with aiosqlite.connect('C:/Users/user/Desktop/neuro/ooba_tg_bot/DB/bot_db.db') as db:
        cursor = await db.cursor()
        await cursor.execute(f'SELECT name FROM characters_list')
        select_result = await cursor.fetchall()
        return select_result