from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, Message
from aiogram.types import CallbackQuery
from ooba_tg import neuro_chat
from sql import new_chat_history,select_from_character_list,select_from_chat_history, select_from_chat_history_command, close_chat
import datetime

router = Router()


class UserChatting(StatesGroup):
    UserChat = State()

class DelHistory(StatesGroup):
    DeleteHistory = State()


async def chat_start(message: Message,callback: CallbackQuery, state: FSMContext,character):
    await message.answer(text="Поздоровайтесь!")
    await state.set_state(UserChatting.UserChat)
    await state.update_data(UserChat=character)
    current_datetime = datetime.datetime.now()
    if await select_from_chat_history(callback.from_user.id,f"{callback.from_user.id}_{character}_history.json") is None:
        await new_chat_history(callback.from_user.id,callback.from_user.username,character,f"{callback.from_user.id}_{character}_history.json",current_datetime)

@router.message(Command("history"))
async def get_chat_history(message: Message):
    history_list = await select_from_chat_history_command(message.from_user.id)
    history_len = len(history_list)
    if history_len == 0:
        await message.answer(text = "Истории чатов нет")
    else:
        for i in range(history_len):
            await message.answer(text = f"Персонаж: {history_list[i][3]}\nДата начала чата: {history_list[i][5]}\nДата конца чата: {history_list[i][6]}")

@router.message(Command("get_characters"))
async def character_menu(message: Message, state: FSMContext):
    character_data = await state.get_data()
    if character_data is not None:
        await state.set_data({})
        await state.clear()
    character_list = await select_from_character_list()
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=f"{character_list[0][0]}",callback_data="character1"))
    builder.add(InlineKeyboardButton(text=f"{character_list[1][0]}",callback_data="character2"))
    await message.answer(text= "Выберите персонажа для общения с ним", reply_markup=builder.as_markup())

@router.callback_query(F.data == "character1")
async def get_character1(callback: CallbackQuery, state: FSMContext):
    character = 'Assistant'
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Очистить диалог",callback_data=f"close_chat1"))
    await callback.message.edit_text("Начат чат с персонажем 1\nДля выхода из чата введите команду /cancel",reply_markup=builder.as_markup())
    await chat_start(callback.message,callback,state,character)
    await callback.answer()

@router.callback_query(F.data == "character2")
async def get_character1(callback: CallbackQuery, state: FSMContext):
    character = 'Example'
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Очистить диалог",callback_data=f"close_chat2"))
    await callback.message.edit_text("Начат чат с персонажем 2\nДля выхода из чата введите команду /cancel",reply_markup=builder.as_markup())
    await chat_start(callback.message,callback,state,character)
    await callback.answer()

@router.message(StateFilter(UserChatting.UserChat))
async def chat_continue(message: Message, state: FSMContext):
    character_data = await state.get_data()
    await message.answer(text= f"{character_data['UserChat']}: {await neuro_chat(message.text,message.from_user.id,character_data['UserChat'])}")

@router.callback_query(F.data == "close_chat1")
async def close_chat1(callback: CallbackQuery, state: FSMContext):
    character = 'Assistant'
    current_datetime = datetime.datetime.now()
    text = await close_chat(callback.from_user.id,f"{callback.from_user.id}_{character}_history.json",current_datetime)
    await callback.message.edit_text(text= text)
    await callback.answer()

@router.callback_query(F.data == "close_chat2")
async def close_chat2(callback: CallbackQuery, state: FSMContext):
    character = 'Example'
    current_datetime = datetime.datetime.now()
    text = await close_chat(callback.from_user.id,f"{callback.from_user.id}_{character}_history.json",current_datetime)
    await callback.message.edit_text(text= text)
    await callback.answer()