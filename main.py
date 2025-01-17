import asyncio
import logging
import os
import sys
from idlelib.window import add_windows_to_menu

from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
import multiprocessing
from os import getenv

from aiogram.fsm.state import StatesGroup
from aiohttp.web_routedef import delete
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, callback_data
from aiogram.types import Message
from buttons.button import StartBTN, contactBTN, priceBTN, statusBTN
from buttons.inline import documentsBTN, acceptBTN, AcceptCallback
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from pyexpat.errors import messages
from start_up.start_up_btn import start_up_btn

load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")

ADMINS = 1509198141

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

class User(StatesGroup):
    full_name = State()
    technology = State()
    contact = State()
    city = State()
    price = State()
    price_total = State()
    status = State()
    time = State()
    dream = State()



if not TOKEN:
    print("Error: BOT_TOKEN is not set in environment variables.")
    sys.exit(1)
# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"""Assalomu alaykum, {html.bold(message.from_user.username)}!
UstozShogird kanallining rasmiy botiga xush kelibsiz!\n
/help yordam buyrugi orqali nimalarga qodir ekanligimni bilib oling!""", reply_markup=StartBTN)




@dp.message(lambda message: message.text == "Sherik kerak")
async def sherik_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"""Sherik topish uchun ariza berish!\n
Hozir sizga bir necha savollar beriladi.
Har biriga javob bering.
Oxirida agar hammasi to'g'ri bo'lsa, {html.bold("Ha")}
Tugmasini bosing va arizangiz Adminga yuboriladi.""")
    await message.answer("Ism Familliyangizni kiriting!")
    await state.set_state(User.full_name)
    # data = await state.get_data()


@dp.message(User.full_name)
async def full_name_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(full_name=message.text)
    await message.answer(f"""📚 Texnologiya:

Talab qilinadigan texnologiyalarni kiriting?
Texnologiya nomlarini vergul bilan ajrating. Masalan, 

Java, C++, C#""")
    await state.set_state(User.technology)


@dp.message(User.technology)
async def technology_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(technology=message.text)
    await message.answer(f"""📞 Aloqa: 

Bog`lanish uchun raqamingizni kiriting!""", reply_markup=contactBTN)
    await state.set_state(User.contact)


@dp.message(User.contact)
async def contact_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(contact=message.contact.phone_number)
    await message.answer(f"""🌐 Hudud: 

Qaysi hududdansiz?
Viloyat nomi, Toshkent shahar yoki Respublikani kiriting""")
    await state.set_state(User.city)

@dp.message(User.city)
async def city_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await message.answer(f"""💰 Narxi:

Tolov qilasizmi yoki Tekinmi?
Kerak bo`lsa, Summani kiriting""")
    await state.set_state(User.price_total)


@dp.message(User.price_total)
async def price_total_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(price_total=message.text)
    await message.answer(f"""👨🏻‍💻 Kasbi: 

Ishlaysizmi yoki o`qiysizmi?
Masalan, Talaba""", reply_markup=statusBTN)
    await state.set_state(User.status)


@dp.message(User.status)
async def status_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(status=message.text)
    await message.answer(f"""🕰 Murojaat qilish vaqti: 

Qaysi vaqtda murojaat qilish mumkin?
Masalan, 9:00 - 18:00""")
    await state.set_state(User.time)


@dp.message(User.time)
async def time_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(time=message.text)
    await message.answer(f"""🔎 Maqsad: 

Maqsadingizni qisqacha yozib bering.""")

    await state.set_state(User.dream)

from aiogram import types
from aiogram.fsm.context import FSMContext

@dp.message(User.dream)
async def dream_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(dream=message.text)
    data = await state.get_data()

    # Foydalanuvchiga tekshirish uchun xabar yuborish
    await message.bot.send_message(
        chat_id=message.from_user.id,
        text=f"""
Sherik kerak:

🏅 Sherik: <b>{data.get('full_name')}</b>
🆔 User id: {message.from_user.id}
📚 Texnologiya: <i>{data.get('technology')}</i> 
🇺🇿 Telegram: @{message.from_user.username or 'Username mavjud emas'} 
📞 Aloqa: +{data.get('contact')} 
🌐 Hudud: {data.get('city')} 
💰 Narxi: {data.get('price_total')}$ 
👨🏻‍💻 Kasbi: {data.get('status')} 
🕰 Murojaat qilish vaqti: {data.get('time')} 
🔎 Maqsad: {data.get('dream')} 
        """,
        parse_mode="HTML"
    )

    msg = await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=documentsBTN)


# Confirmation handler (Userdan tasdiq olish uchun)
@dp.callback_query(lambda call: call.data in ["confirm_yes", "confirm_no"])
async def documents_handler(call: CallbackQuery, state: FSMContext) -> None:
    if call.data == "confirm_yes":
        data = await state.get_data()
        print(data)
        user_id = call.from_user.id  # Foydalanuvchi ID

        # Adminlarga ma'lumot yuborish
        await call.bot.send_message(
            chat_id=ADMINS,
            text=f"""
<b>{call.from_user.full_name}</b> dan ma'lumot:\n
Sherik kerak:

🆔 User id: {user_id}
🏅 Sherik: <b>{data.get('full_name')}</b> 
📚 Texnologiya: <i>{data.get('technology')}</i> 
🇺🇿 Telegram: @{call.from_user.username or 'Username mavjud emas'} 
📞 Aloqa: +{data.get('contact')} 
🌐 Hudud: {data.get('city')} 
💰 Narxi: {data.get('price_total')} 
👨🏻‍💻 Kasbi: {data.get('status')} 
🕰 Murojaat qilish vaqti: {data.get('price')} 
🔎 Maqsad: {data.get('dream')}
            """,
            parse_mode="HTML",
            reply_markup=acceptBTN(user_id)  # Foydalanuvchi IDni yuboring
        )
        await call.answer("Ma'lumot yuborildi.")
        await state.clear()
    elif call.data == "confirm_no":
        await call.message.answer("Ma'lumotlaringizni boshidan kiriting!", reply_markup=StartBTN)
        await call.answer()
        await state.clear()
    await call.message.delete()
# Admin tasdiqlash/inkor qilish handleri
@dp.callback_query(lambda call: call.data.startswith("accept_Yes") or call.data.startswith("accept_No"))
async def accept_handler(call: CallbackQuery, state: FSMContext) -> None:
    try:
        # Callback data dan foydalanuvchi ID ni ajratib olish
        callback_data = call.data.split(":")
        action = callback_data[0]  # "accept_Yes" yoki "accept_No"
        user_id = int(callback_data[1])  # Foydalanuvchi ID

        # Ma'lumotlarni state'dan olish (data ni admin tasdiqlash vaqtida saqlab qo'ygan bo'lishingiz kerak)
        data = await state.get_data()
        print(data)  # Ma'lumotlarni tekshirish uchun chiqarish

        # Inline tugmalarni o'chirib yuborish
        await call.message.edit_reply_markup()  # Tugmalarni o'chirish

        # Qaysi tugma bosilganini bildiruvchi matnni yuborish
        if action == "accept_Yes":
            # Foydalanuvchiga tasdiqlangan ma'lumotlarni yuborish
            await call.bot.send_message(
                chat_id=user_id,
                text=f"""
<b>Sherik kerak</b> Bo'yicha arizangiz qabul qilindi!✅

Ma'lumotlaringiz qabul qilindi!✅""",
                parse_mode="HTML",
                reply_markup=StartBTN,
            )
            # Adminlarga qabul qildik deb bildirish
            updated_text = call.message.text + "\n\nSiz <b>qabul qildingiz</b> ✅"
            await call.message.edit_text(updated_text, parse_mode="HTML")
        elif action == "accept_No":
            # Foydalanuvchiga rad etilganligini yuborish
            await call.bot.send_message(
                chat_id=user_id,
                text="Ma'lumotlaringiz rad etildi. Iltimos, qaytadan urinib ko'ring!",
                reply_markup=StartBTN,
            )
            # Adminlarga rad etilganligini bildirish
            updated_text = call.message.text + "\n\nSiz <b>rad etdiniz</b> ❌"
            await call.message.edit_text(updated_text, parse_mode="HTML")

        await call.answer("Javob yuborildi.")
    except (IndexError, ValueError):
        await call.answer("Callback ma'lumotlarida xatolik yuz berdi.", show_alert=True)
        await state.clear()







async def main() -> None:
    # Use the updated Bot initializer with DefaultBotProperties


    await start_up_btn(bot)

    # Ensure handlers are included
    # dp.include_router(dp)

    # Start polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())