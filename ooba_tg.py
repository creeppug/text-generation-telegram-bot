import os
import json
from aiogram import Bot, Dispatcher
from httpx import AsyncClient
import asyncio
from aiogram.types import Message
from variables import BOT_TOKEN, URL
from handlers import common, user_chatting
from googletrans import Translator

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
translator = Translator()


headers = {
    "Content-Type": "application/json"
}


async def neuro_chat(message: Message,user_id,character):
    history = []
    if os.path.exists(f"C:/Users/user/Desktop/neuro/ooba_tg_bot/data/{user_id}_{character}_history.json"):
           with open(f"C:/Users/user/Desktop/neuro/ooba_tg_bot/data/{user_id}_{character}_history.json", "r") as history_file:
                  history = json.load(history_file)
    print(history)
    print(message)
    translate_from_ru = translator.translate(f"{message}", dest="en")
    print(translate_from_ru)
    history.append({"role": "user", "content": translate_from_ru.text})
    data =  {
        "messages": history,
        "mode": "chat-instruct",
        "character": f"{character}",
        "max_tokens": 250,
        "temperature": 0.5,
        "top_p": 0.9,
        "seed": -1
    }
    print(data)
    async with AsyncClient() as httpx_client:
        try:
            r = await httpx_client.post(URL, headers=headers, json=data, timeout=None)
            assistant_message = r.json()['choices'][0]['message']['content']
            with open(f"C:/Users/user/Desktop/neuro/ooba_tg_bot/data/{user_id}_{character}_response_data.json", "w") as json_file:
                        json.dump(r.json(), json_file)
            history.append({"role": "assistant", "content": assistant_message})
            with open(f"C:/Users/user/Desktop/neuro/ooba_tg_bot/data/{user_id}_{character}_history.json", "w") as history_file:
                        json.dump(history, history_file)
            print(assistant_message)
            assistant_message_translated_from_en = translator.translate(f"{assistant_message}", dest="ru")
            return assistant_message_translated_from_en.text
        except Exception as e:
              print(e)
        finally:
              await httpx_client.close()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(common.router)
    dp.include_router(user_chatting.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())