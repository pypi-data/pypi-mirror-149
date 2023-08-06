import asyncio
import logging
import os
from typing import Callable, Optional

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import NetworkError

from .session_cache import OpenSessions, get_prompt, UserSession, CompleteFlowException
from .localisation import ServiceVocabulary, FormatException, TranslateException
from .google_sheets import DB_AS_GoogleSheet
from .utils import Singleton

logger = logging.getLogger(os.path.split(__file__)[-1])


@Singleton
class _service:
    network_retry = 10
    counter = 0

    def __init__(self, token):
        self._token = token
        self._bot: Optional[Bot] = None
        self._dp = None
        self._on_startup = None
        self.skip_updates = True

    def set_on_startup(self, callback: Callable):
        self._on_startup = callback

    @property
    def bot(self):
        if not self._bot:
            self._bot = Bot(token=self._token)
        return self._bot

    @property
    def dp(self):
        if not self._dp:
            self._dp = Dispatcher(self.bot)
        return self._dp

    @staticmethod
    def register_on_startup(*callbacks):
        async def on_startup(_):
            for callback in callbacks:
                asyncio.create_task(callback)
                logger.info(f"Callback '{callback.__name__}' registered")
            # asyncio.create_task(background_expired_sessions_handler(OpenSessions.expired_queue))
            logger.info("Bot started online service")

        return on_startup

    def start(self, **kwargs):
        while True:
            try:
                self.register_on_startup(*kwargs.get('start_up', []))
                executor.start_polling(self.dp, skip_updates=self.skip_updates, on_startup=self._on_startup)
            except NetworkError as e:
                if self.counter > self.network_retry:
                    raise
                logging.warning(f"Cannot restart service for {self.counter} times; {e}")
                self.counter += 1
            finally:
                pass

    def stop(self):
        self.dp.stop_polling()


Service: _service = _service(os.getenv('TOKEN'))


async def cancel_registration(message: types.Message):
    logger.debug(f"cancel_registration -> {message.from_user.full_name}: {message.text}")
    if message.from_user.id in OpenSessions.keys():
        logger.info(f"Restart session for {message.from_user.id}")
        del OpenSessions[message.from_user.id]
        await message.reply(get_prompt('flows', 'cancel', 0, 'language', message.from_user.language_code,
                                       message=message), parse_mode='html')
    else:
        await message.reply("Registration wasn't started yet", parse_mode='html')


async def register_handler(message: types.Message):
    logger.debug(f"register_handler -> {message.from_user.full_name}: {message.text}")
    if message.from_user.id in OpenSessions.keys():
        logger.info(f"Restart session for {message.from_user.id}")
        await Service.bot.send_message(message.from_user.id, "Session restarted")
        del OpenSessions[message.from_user.id]
    logger.info(f'New user -> {message.from_user.id}: {message.from_user.language_code}')
    user_name = message.from_user.username if message.from_user.username else ''
    OpenSessions[message.from_user.id] = UserSession(message.from_user.id, user_name,
                                                     message.from_user.language_code)
    OpenSessions[message.from_user.id].set_flow('register')
    await message.reply(OpenSessions[message.from_user.id].get_prompt(message), parse_mode='html')


async def role_handler(message: types.Message):
    logger.debug(f"role_handler -> {message.from_user.full_name}: {message.text}")
    if message.from_user.id in OpenSessions.keys():
        command = message.get_command(True)
        OpenSessions[message.from_user.id].set_item(command)
        OpenSessions[message.from_user.id].move_to_next()
        await message.answer(OpenSessions[message.from_user.id].get_prompt(message))
    else:
        await message.reply("Registration wasn't started yet", parse_mode='html')


async def all_handler(message: types.Message):
    logger.debug(f"all_handler -> {message.from_user.full_name}: {message.text}")
    if message.from_user.is_bot:
        await message.reply("Please enter from Group")
        return
    user_id = message.from_user.id
    if user_id not in OpenSessions.keys():
        prompt = "{}".format(ServiceVocabulary.get_path('welcome_banner', 'text', message.from_user.language_code))

        welcome_picture = os.path.normpath(ServiceVocabulary.get('welcome_banner', {}).get('picture', ''))
        if welcome_picture:
            with open(os.path.normpath(os.path.join('images', 'welcome_banner.jpg')), 'rb') as photo_stream:
                await Service.bot.send_photo(message.chat.id, photo=photo_stream, caption=prompt, parse_mode='html')
        else:
            await message.reply(prompt, parse_mode='html')
        return
    try:
        OpenSessions[user_id].set_item(f"{message.text}")
        OpenSessions[user_id].move_to_next()
        await message.answer(OpenSessions[user_id].get_prompt(message))
    except CompleteFlowException:
        msg = "User {} registered:\n\t{}".format(
            message.from_user.full_name,
            '\n\t'.join(f"{k}: {v}" for k, v in OpenSessions[message.from_user.id].as_dict().items())
        )
        logger.info(msg)
        result = OpenSessions[message.from_user.id].as_dict()
        DB.set_person(**result)
        del OpenSessions[message.from_user.id]
        await message.reply(get_prompt('flows', 'complete', 0, 'language', message.from_user.language_code,
                                       message=message), parse_mode='html')
        # for admin in ServiceConfiguration.get('administrators', []):
        #     await Service.bot.send_message(admin.get('id'), f"Thanks, your registration completed\n{msg}")
    except (TranslateException, FormatException) as e:
        await message.reply(f"Wrong data inserted: {e}")


# async def chat_join_handler(chat_member: types.ChatJoinRequest):
#     await Service.bot.send_message(chat_member.from_user.id, "Hi, i'm your bot")


def handlers_register(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, commands=['cancel'])
    dp.register_message_handler(register_handler, commands=['register'])
    dp.register_message_handler(role_handler, commands=['Volunteer', 'Candidate'])
    dp.register_message_handler(all_handler)
    # dp.register_chat_join_request_handler(chat_join_handler)


__all__ = [
    'Service',
    'handlers_register'
]
