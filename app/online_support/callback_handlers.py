import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message, Voice
from aiogram.filters import Filter
from database.users import return_phone_number_or_none, delete_phone_number
from database.help_request import add_thread, return_user_by_thread_id, return_user_by_user_id
from aiogram.fsm.context import FSMContext

from app.online_support.states import UserHelp
import app.online_support.keyboards as kb


OnlineSupportCallbackRouter = Router()


@OnlineSupportCallbackRouter.callback_query(F.data == 'start_conversation')
async def start_conv(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer('')
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    await state.set_state(UserHelp.user_message)
    await callback.message.answer('Отправьте ваш вопрос и администратор в скором времени на него ответит!')
    return


@OnlineSupportCallbackRouter.message(UserHelp.user_message)
async def send_help(message: Message, state: FSMContext) -> None:
    await state.update_data(user_id = str(message.from_user.id))
    await state.update_data(first_message = str(message.from_user.id))
    await state.update_data(date = message.date)
    data = await state.get_data()
    try:
        thread_id =(await return_user_by_user_id(user_id=str(message.from_user.id)))[1]
        await message.bot.send_message(text = message.text, chat_id = '-1002437414181', message_thread_id = thread_id)
    except:
        topic = await message.bot.create_forum_topic(chat_id = '-1002437414181', name = f'{message.from_user.id} - {message.from_user.username}')
        await state.update_data(thread_id = topic.message_thread_id)
        data = await state.get_data()
        await add_thread(data = data)
        await message.bot.send_message(text = f'Новое обращение от пользователя @{message.from_user.username}\n\n{message.text}', chat_id = '-1002437414181', message_thread_id = topic.message_thread_id)
    await message.answer('Ваше обращение усппешно отправлено! Скоро администраторы вам ответят! Вы можете пользоваться ботом в ожидании ответа!', reply_markup = kb.use_bot_while_waiting)
    await state.clear()
    return


@OnlineSupportCallbackRouter.message(F.photo)
async def send_photo(message: Message) -> None:
    group = [photo.file_id for photo in message.photo]
    if message.chat.is_forum:
        if message.chat.id == '-1002183209044' and message.message_thread_id == 1:
            return
        else:
            try:
                user_chat_id = (await return_user_by_thread_id(thread_id=message.message_thread_id))[0]
                await message.bot.send_photo(photo = f'{group[0]}', caption = message.caption, chat_id = user_chat_id)
            except: pass
    else: 
        user_chat_id = (await return_user_by_user_id(user_id = str(message.from_user.id)))
        if user_chat_id:
            await message.bot.send_photo(chat_id = '-1002437414181', message_thread_id = user_chat_id[1], photo = f'{group[0]}', caption = message.caption)
        else: 
            await message.answer('Ваш чат с администратором неактивен! Активируйте чат с помощью /start_conversation')
    return


@OnlineSupportCallbackRouter.message(F.video)
async def send_video(message: Message) -> None:
    video = message.video.file_id
    if message.chat.is_forum:
        if message.chat.id == '-1002183209044' and message.message_thread_id == 1:
            return
        else:
            try:
                user_chat_id = (await return_user_by_thread_id(thread_id = message.message_thread_id))[0]
                await message.bot.send_video(video=f'{video}', caption = message.caption, chat_id = user_chat_id)
            except: pass
    else: 
        user_chat_id = (await return_user_by_user_id(user_id = str(message.from_user.id)))
        if user_chat_id:
            await message.bot.send_video(chat_id = '-1002437414181', message_thread_id = user_chat_id[1], video = f'{video}', caption = message.caption)
        else: 
            await message.answer('Ваш чат с администратором неактивен! Активируйте чат с помощью /start_conversation')
    return


@OnlineSupportCallbackRouter.message()
async def help_message(message: Message):
    if message.chat.is_forum:
        if message.chat.id == '-1002437414181' and message.message_thread_id == 1:
            return
        else: 
            try:
                user_chat_id = (await return_user_by_thread_id(thread_id=message.message_thread_id))[0]
                await message.bot.send_message(chat_id = user_chat_id, text = message.text)
            except: pass
    else:
        user_chat_id = (await return_user_by_user_id(user_id = str(message.from_user.id)))
        if user_chat_id:
            try:
                await message.bot.send_message(chat_id = '-1002437414181', message_thread_id = user_chat_id[1], text = message.text)
            except: await message.answer('Ваш чат с администратором неактивен! Активируйте чат с помощью /start_conversation')
        else: 
            await message.answer('Ваш чат с администратором неактивен! Активируйте чат с помощью /start_conversation')
    return