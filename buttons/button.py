from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

StartBTN = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Sherik kerak"),KeyboardButton(text="Ish joyi kerak")],
        [KeyboardButton(text="Hodim kerak"), KeyboardButton(text="Ustoz kerak")],
        [KeyboardButton(text="Shogird kerak")]
    ]
)

contactBTN = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Share my contact", request_contact=True)],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

priceBTN = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Tekin!"), KeyboardButton(text="Narx kiritish:")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

statusBTN = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Talabaman"), KeyboardButton(text="Ishlayman")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

adminBTN = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Adminga murojat qilish!")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)