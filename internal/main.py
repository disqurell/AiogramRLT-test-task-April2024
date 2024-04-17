from config.settings import bot
from api.v1.handlers import router as v1_router


async def main():
    bot.run()
    dp = bot.get_dp()
    bot_obj = bot.get_bot()

    dp.include_routers(v1_router)

    await dp.start_polling(bot_obj)
