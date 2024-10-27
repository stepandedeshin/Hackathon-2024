from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import app.main_menu.keyboard as kb
from database.users import return_phone_number_or_none

MainMenuCallbackRouter = Router()


@MainMenuCallbackRouter.callback_query(F.data.startswith('main_menu'))
async def start_message(callback: CallbackQuery, state: FSMContext) -> None: 
    '''
    Get user back to main menu by callback_data (pressing the inline button)

    callback_data may contain parameter "without_deleting" which makes bot to don't remove a message before

    returns None
    '''
    await callback.answer('Меню')
    await callback.message.answer_photo(photo = 'https://imgur.com/Uqf17Mh', caption = f'Приветствуем, @{callback.from_user.username}!\nДобро пожаловать в бота поддержки пользователей!', reply_markup = kb.start_message)
    if not 'without_deleting' in callback.data:
        await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    if 'without_deleting' in callback.data:
        await state.clear()
    return


@MainMenuCallbackRouter.callback_query(F.data == 'gpt_assistant')
async def gpt_assistant_start(callback: CallbackQuery) -> None:
    '''
    Get user to GPT Assistant block by callback_data (pressing the inline button)

    returns None
    '''
    await callback.answer('GPT Ассистент')
    await callback.message.answer('GPT Ассистент поможет вам найти ответ на ваш вопрос, опираясь на документацию', reply_markup = kb.gpt_assistant)
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    return


@MainMenuCallbackRouter.callback_query(F.data == 'faq')
async def show_faq(callback: CallbackQuery) -> None:
    '''
    Get user to FAQ block by callback_data (pressing the inline button)
    FAQ file splits to a few messages and sends part by part which lenght are less than 4096 tokens because of telegram message lenght limit (4096 tokens)

    returns None
    '''
    await callback.answer('')
    faq_questions = open('faq.txt', 'r', encoding='utf-8').read()
    message_limit = 4096 
    parts = [faq_questions[i: i + message_limit] for i in range(0, len(faq_questions), message_limit)]
    for part in parts[0:-1:]:
        await callback.message.answer(part)
    await callback.message.answer(parts[-1], reply_markup = kb.show_faq)
    return 


@MainMenuCallbackRouter.callback_query(F.data == 'help_by_admin')
async def conversation_start(callback: CallbackQuery) -> None:
    '''
    Get user to starts admin conversation state by callback_data (pressing the inline button)
    Only authorized by phone users can use an online support

    returns None
    '''
    await callback.answer('Онлайн поддержка')
    phone_number = await return_phone_number_or_none(user_id = str(callback.from_user.id))
    if phone_number:
        await callback.message.answer('Добро пожаловать в онлайн поддержку! Здесь вы можете запросить помощь у онлайн-администраторов', reply_markup = kb.help_by_admin)
    else:
        await callback.message.answer('Вы не авторизованы! Чтобы обратиться в онлайн поддержку необходимо привязать свой номер телефона!', reply_markup = kb.auth_to_use_online_support)
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    return


@MainMenuCallbackRouter.callback_query(F.data == 'auth')
async def auth_start(callback: CallbackQuery) -> None:
    '''
    Lets user to auth himself by using phone number. Lets user share telegram contact by pressing the button (reply keyboard)
    If phone number already exists in database lets user to edit or delete it

    returns None
    '''
    await callback.answer('Авторизация')
    phone_number = await return_phone_number_or_none(user_id = str(callback.from_user.id))
    if not phone_number:
        await callback.message.answer('Привяжите номер телефона, чтобы пользоваться онлайн поддержкой!', reply_markup = kb.auth)
    else:
        await callback.message.answer(f'Привязанный вами номер телефона: {phone_number}\nЗдесь вы можете его изменить или удалить', reply_markup = kb.auth_edit_or_delete)
    try:
        await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    except: pass
    return