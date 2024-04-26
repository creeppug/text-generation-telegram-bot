from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from sql import register_to_bot
import datetime


router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_data({})
    await state.clear()
    current_datetime = datetime.datetime.now()
    await register_to_bot(message.from_user.id,message.from_user.username,current_datetime)
    await message.answer(text="С помощью команды /get_characters выберите персонажа для общения\nС помощью команды /history посмотрите историю чата")


@router.message(Command(commands=["cancel"]))
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await state.clear()
    await message.answer(text="Совершен выход из чата")