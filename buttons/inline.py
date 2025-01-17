from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData

# Define callback data structure
class AcceptCallback(CallbackData, prefix="accept"):
    action: str



documentsBTN = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="HA", callback_data="confirm_yes"),
            InlineKeyboardButton(text="YO'Q", callback_data="confirm_no"),
        ]
    ]
)


# acceptBTN = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton[
#                 text="Qabul qilish", callback_data=("yes")
#             ]
#             InlineKeyboardButton(
#                 text="Qabul qilmaslik", callback_data=("no")
#             ),
#         ]
#     ]
# )

# Qabul qilish va rad etish tugmalari
def acceptBTN(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Qabul qilish",
                    callback_data=f"accept_Yes:{user_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Rad etish",
                    callback_data=f"accept_No:{user_id}"
                )
            ]
        ]
    )
