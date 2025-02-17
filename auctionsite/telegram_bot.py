#Creator t.me/@unotuno
#Number:
#Date: 11.11.2024

import asyncio
import os
from datetime import datetime, timezone
import requests
import django
from aiogram.filters import Command
from aiogram.types import message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputFile
from django.conf import settings
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import FSInputFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auctionsite.settings')
if not settings.configured:
    django.setup()

from auctionapp.models import Lot, AdminProfile

BOT_TOKEN = ''
CHANNEL_ID = ''


bot = Bot(BOT_TOKEN)
dp = Dispatcher()
router = Router()


@router.message(Command('send'))
async def send_data_to_channel(message: types.Message)->None:
    """Отправляет информацию о лотах в Telegram-канал сообщением в виде photo>caption photo>buttons."""
    try:
        response = requests.get('http://127.0.0.1:8000/active_lots')
        lots = response.json()
        try:
            for lot in lots:
                path_img = lot['images']
                img = path_img[13:]
                with open(img, 'rb') as file:
                    file_img = FSInputFile(img)
                message_text = f"Название: {lot['name_lot']}\n"
                message_text += f"Продавец: {lot['link_seller']}\n"
                message_text += f"Адрес: {lot['address']}\n"
                message_text += f"Описание: {lot['description']}\n"
                message_text += f"Дата окончания лота: {lot['end_date_auction']}\n"
                message_text += f"Цена: {lot['start_price']}\n"
                message_text += f"Следующая ставка: .\n"
                message_text += f"Лидирует: .\n"
                keyboard = [[InlineKeyboardButton(text='info', callback_data=f'info{lot['id']}')],
                            [InlineKeyboardButton(text='time', callback_data=f'time{lot['id']}')],
                            [InlineKeyboardButton(text='Открыть лот', url=f't.me/boteski_bot?start={lot['id']}',
                                                  callback_data=f'{lot['id']}')]]
                kb = InlineKeyboardMarkup(inline_keyboard=keyboard)
                await bot.send_photo(CHANNEL_ID, photo=file_img, caption=message_text, reply_markup=kb)
        except Exception as e:
            print(f'Нет возможности создать карточку лота {e}')
        print(f"Сообщение отправлено в канал {CHANNEL_ID}")
    except Exception as e:
        print(f"Ошибка при получении данных о лотах: {e}")


@router.message(Command('start'))
async def choose_lot( call:CallbackQuery)->None:
    '''Создаёт новое сообщение с карточкой лота когда юзер выбрал лот'''
    id_lot = call.text.split(' ')[1]
    try:
        response = requests.get(f'http://127.0.0.1:8000/lot/{id_lot}')
        lot_in_choice = response.json()
        for lot in lot_in_choice:
            path_img = lot['images']
            img = path_img[13:]
            with open(img, 'rb') as file:
                file_img = FSInputFile(img)
            message_text = f"Название: {lot['name_lot']}\n"
            message_text += f"Продавец: {lot['link_seller']}\n"
            message_text += f"Адрес: {lot['address']}\n"
            message_text += f"Описание: {lot['description']}\n"
            message_text += f"Дата окончания лота: {lot['end_date_auction']}\n"
            message_text += f"Цена: {lot['start_price']}\n"
            message_text += f"Следующая ставка: .\n"
            message_text += f"Лидирует: .\n"
            keyboard = [ [InlineKeyboardButton(text='info',callback_data=f'info{lot['id']}')],
                         [InlineKeyboardButton(text='time',callback_data=f'time{lot['id']}')],
                         [InlineKeyboardButton(text='Сделать ставку',callback_data=f'bid{lot['id']}')],
                         [InlineKeyboardButton(text='Настроить ставку',callback_data='auto_bid')],
                         [InlineKeyboardButton(text='Скачать документ',callback_data=f'doc{lot['id']}')],
                         ]
            kb = InlineKeyboardMarkup(inline_keyboard=keyboard)
            await bot.send_photo(call.chat.id, photo=file_img, caption=message_text, reply_markup=kb)
    except Exception as e:
        print('Нет возможности создать карточку лота')

@router.message(Command('balance'))
async def up_balace(message: types.Message)->None:
    '''Пополняет баланс'''
    try:
        chat_user = await bot.get_chat_member(CHANNEL_ID, user_id=message.from_user.id)
        if chat_user.status in ['administrator', 'creator']:
            info_balance = message.text.split(' ')
            name_user = info_balance[1]
            money = info_balance[2]
            params = {'name_user': name_user,
                      'balance': money}
            response = requests.post('http://127.0.0.1:8000/balance_up', params=params)
        else:
            await bot.send_message(message.chat.id, text='Проверь правильность ввода команды по примеру'
                                                         '/balance Oleg 150, или ты не админ')
    except Exception as e:
        print(f'Ошибка {e}')


@router.message(Command('delete'))
async def channel_post_handler(message: types.Message)->None:
    '''Деактивирует(удаляет) лот если команду ввёл админ или создатель  канала '''
    user_id = message.from_user.id
    name_lot = message.text[8:]
    try:
        chat_user = await bot.get_chat_member(CHANNEL_ID, user_id=user_id)
        if chat_user.status in ['administrator', 'creator']:
            params = {'name_lot': name_lot}
            response = requests.post('http://127.0.0.1:8000/delete', params=params)
            a = response.json()
    except Exception as e:
        print (f'Error: {e}')
        await bot.send_message(message.chat.id, text='Вероятнее всего вы не являетесь админом или создателем канала,'
                                                     ' чтобы иметь права на удаление лотов. Если же вы являетесь таковым '
                                                     'проверьте правильность ввода имени лота после команды /delete')
@router.callback_query()
async def choose_lot(call:CallbackQuery):
    '''Колбэки'''
    data = call.data
    if data.startswith('time'):
        #Отлавливает кнопку TIME
        id_lot = data[4:]
        try:
            response = requests.get(f'http://127.0.0.1:8000/lot/{id_lot}')
            req_data = response.json()
        except Exception as e:
            print(f'Ошибка {e}')
        lot_time = datetime.fromisoformat(req_data[0]['end_date_auction'])
        time_to_end = lot_time - datetime.now(tz=timezone.utc)
        await call.answer(f'До конца аукциона осталось:\n {time_to_end}', show_alert=True)
    elif data.startswith('bid'):
        #Отлавливает кнопку СДЕЛАТЬ СТАВКУ
        # вставить проверку если пользователь уже делал ставку на лот
        data_caption = {}
        for line in call.message.caption.splitlines():
            key, value = line.split(": ")
            data_caption[key] = value
        user_name = call.from_user.username
        id_lot = data[3:]
        try:
            response = requests.get(f'http://127.0.0.1:8000/bid/{id_lot}')
            admin_data = response.json()
            response = requests.get(f'http://127.0.0.1:8000/lot/{id_lot}')
            lot_data = response.json()
        except Exception as e:
            print(f'К сожалению {e} ')
        bid = float(admin_data[0]['step_bid'])
        price = admin_data[0]['current_price']
        if float(price) == 0:
            new_price = bid + float(lot_data[0]['start_price'])
        else:
            new_price = bid + float(price)
        new_caption = ''
        for k,v in data_caption.items():
            if k == 'Цена':
                v = str(new_price)
            if k == 'Следующая ставка':
                v = str(new_price + bid)
            if k == 'Лидирует':
                v = f'@{user_name}'
            new_caption += f'{k}: {v}\n'
        keyboard = [[InlineKeyboardButton(text='info', callback_data=f'info{id_lot}')],
                    [InlineKeyboardButton(text='time', callback_data='time')],
                    [InlineKeyboardButton(text='Сделать ставку', callback_data=f'bid{id_lot}')],
                    [InlineKeyboardButton(text='Настроить ставку', callback_data='auto_bid')],
                    [InlineKeyboardButton(text='Скачать документ', callback_data=f'doc{id_lot}')],
                    ]
        kb = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                       caption=f"{new_caption}", reply_markup=kb
                                       )
        try:
            params = {'new_price': new_price,
                      'user_name_bid': user_name}
            response = requests.post(f'http://127.0.0.1:8000/save_price/{id_lot}', params=params)
        except Exception as e:
            print(f'Ошибка {e}')
    elif data.startswith('info'):
        #Отлавливает кнопку INFO
        id_lot = data[4:]
        response = requests.get(f'http://127.0.0.1:8000/bid/{id_lot}')
        admin_data = response.json()
        info_rule = admin_data[0]['rules']
        await call.answer( f'{info_rule}', show_alert=True)
    elif data.startswith('doc'):
        #Отлавливает кнопку скачать документы
        id_lot = data[3:]
        keyboard = [[InlineKeyboardButton(text='Исторический', callback_data=f'hist_{id_lot}')],
                    [InlineKeyboardButton(text='Ювелирный', callback_data=f'jewe_{id_lot}')],
                    [InlineKeyboardButton(text='Стандартный', callback_data=f'stan_{id_lot}')]
        ]
        kb = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await bot.send_message(chat_id=call.message.chat.id,  reply_markup=kb,text='Выберите тип документа')
    elif data[4] == '_':
        #Отлавливает колбэк конкретного типа документа
        id_lot = call.data[5:]
        user_name = call.from_user.username
        params = {
            'type': data[:4],
            'user_name': user_name
        }
        response = requests.post(f'http://127.0.0.1:8000/document/{id_lot}', params=params)
        data_response = response.json()
        file_name = data_response['file_name']
        try:
            path = f'document/{file_name}'
            with open(path, 'rb') as file:
                await bot.send_document(chat_id=call.message.chat.id, document=FSInputFile(filename=f'{file}', path=path))
        except Exception as e:
            print(f'Ошибка отправки документа {e}')

async def main():
    """Запускает бота."""
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



