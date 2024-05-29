from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, URLInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Добро пожаловать!", reply_markup=kb.main)


@router.message(F.text == "Каталог")
async def catalog(message: Message):
    await message.answer(
        "Выберите категорию товара", reply_markup=await kb.categories()
    )


@router.callback_query(F.data.startswith("category_"))
async def category(callback: CallbackQuery):
    await callback.answer("Вы выбрали категорию")
    await callback.message.answer(
        "Выберите товар по категории",
        reply_markup=await kb.items(callback.data.split("_")[1]),
    )


@router.callback_query(F.data.startswith("item_"))
async def item(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split("_")[1])
    await callback.answer("Вы выбрали товар")
    await callback.message.answer(
        f"Название: {item_data.name}\nОписание: {item_data.descriprion}\nЦена: {item_data.price}$",
        reply_markup=await kb.items(callback.data.split("_")[1]),
    )

@router.message(F.text == "Контакты")
async def contact(message: Message):
    await message.answer('@mukrop1')

@router.message(F.text == "О нас")
async def about_us(callback: CallbackQuery):
    await callback.answer(text='Всё чики пуки', show_alert=True)
