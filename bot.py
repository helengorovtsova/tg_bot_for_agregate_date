import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import load_config, Config
from handlers import user_handlers
from keyboards.keyboards import set_main_menu
logger = logging.getLogger(__name__)

async def main():

    # logging setup
    logging.basicConfig(
        level=logging.INFO, 
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )

    logging.info('Starting bot')



    config: Config = load_config()

    bot = Bot(token=config.bot.token, parse_mode='HTML')
    dp = Dispatcher()

    # setting the main menu
    await set_main_menu(bot)

    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())