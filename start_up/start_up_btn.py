from aiogram import Dispatcher, types

async def start_up_btn(bot):
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description='Botni ishga tushirish'),
            types.BotCommand(command="help", description='Bot haqida'),
            types.BotCommand(command="exit", description='Botni to\'xtarish')
        ]
    )

    await bot.send_message(chat_id=1509198141, text="Assalomu alaykum Bot ishga tushirildi!")