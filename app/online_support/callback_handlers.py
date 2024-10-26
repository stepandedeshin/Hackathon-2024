from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.online_support.keyboards as kb
from app.online_support.states import UserHelp
from database.help_request import (add_thread, return_user_by_thread_id,
                                   return_user_by_user_id)
from database.users import return_phone_number_or_none

OnlineSupportCallbackRouter = Router()


@OnlineSupportCallbackRouter.callback_query(F.data == 'start_conversation')
async def start_conv(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    Starts conversation state by callback_data (by pressing the inline button)
    Only authorized by phone users can use an online support

    returns None
    '''
    phone_number = await return_phone_number_or_none(user_id=str(callback.from_user.id))
    await callback.answer('')
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    if phone_number:
        await state.set_state(UserHelp.user_message)
        await callback.message.answer('Отправьте ваш вопрос и администратор в скором времени на него ответит!')
    else:
        await callback.message.answer('Вы не авторизованы! Чтобы обратиться в онлайн поддержку необходимо привязать свой номер телефона!', reply_markup = kb.auth_to_use_online_support)
    return


@OnlineSupportCallbackRouter.message(UserHelp.user_message)
async def send_help(message: Message, state: FSMContext) -> None:
    '''
    Sending user's help request to new topic if topic not exists and adding thread to database

    in case of topic exists just sending a message without creating topic and adding thread_id

    returns None
    '''
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
    '''
    Sending user's photo to existing topic

    in case of topic not exists asking to create one by using "/start_conversation"

    returns None
    '''
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
    '''
    Sending user's video to existing topic

    in case of topic not exists asking to create one by using "/start_conversation"

    returns None
    '''
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
    '''
    Handle EVERY message that is not handled by other routers
    If message sent in admin chat in topic passes
    If message sent not in admin chat but in topic sens a message to user (admin answer)

    If message sent not in topics
    Sending user's message to existing topic

    in case of user topic not exists asking to create one by using "/start_conversation"

    returns None
    '''
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