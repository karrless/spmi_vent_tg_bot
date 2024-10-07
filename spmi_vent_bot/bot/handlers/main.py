from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from spmi_vent_bot.bot.templates import render_template

router = Router()

@router.message(Command("start"))
async def start_command_handler(msg: Message):
    await msg.answer(text=render_template('start.html', username=msg.from_user.username, id=msg.from_user.id))
