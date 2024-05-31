import telebot
from telebot import types, custom_filters
from telebot.handler_backends import State, StatesGroup
from settings import site, search
from site_API.SEARCH_V3 import request as req_1
from site_API.PROPERTIES_LIST import request as req_2
from site_API.REVIEWS_GET_SUMMARY import request as req_3
from telebot.storage import StateMemoryStorage
import re
from database.common.models import HistorySearch, HistorySummary
from datetime import datetime
import tg_API.utils.markups as mk


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(site.token, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))


class Filter(StatesGroup):
    choose = State()
    city = State()
    city_confirm = State()
    dates = State()
    price = State()
    people = State()
    people_adults = State()
    people_children = State()
    searching = State()
    summary = State()


@bot.message_handler(commands=['check'], state='*')
def choose_city(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.send_message(message.chat.id, text="Date in {}\nDate out {}\nmin_price:{}\nmax_price: {}\ncity"
                                               " id: {}\n Adults quantity: {}\nChildren: {}\nsummary id:{}".format(
            data["checkInDate"], data["checkOutDate"], data["price"]["min"], data["price"]["max"], data['regionId'],
            data['adults'], data['children'], data['id_for_summary']), reply_markup=mk.markup_main)
        bot.set_state(message.from_user.id, Filter.choose, message.chat.id)


@bot.message_handler(commands=['help'], state='*')
def send_welcome(message):
    bot.send_message(message.chat.id, text='Type /start to start interacting with bot.\n'
                                           'Type /check to watch your search settings.\n')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
    bot.send_message(message.chat.id,
                     text="Hello, {0.first_name}! Im test bot for searching hotels!"
                          "Please type place where you want to go, after chose dates of your vocation"
                          " prises for room and quantity of people and we will find good"
                          " place for you!".format(message.from_user), reply_markup=mk.markup_main)


@bot.message_handler(state=Filter.choose)
def choose_city(message):
    if message.text == "Choose city":
        bot.send_message(message.chat.id, text='Enter city name.', reply_markup=mk.poor_markup)
        bot.set_state(message.from_user.id, Filter.city, message.chat.id)
    elif message.text == "Choose dates":
        bot.send_message(message.chat.id, text='Enter dates of in and out in format DD-MM-YYYY DD-MM-YYYY.',
                         reply_markup=mk.poor_markup)
        bot.set_state(message.from_user.id, Filter.dates, message.chat.id)
    elif message.text == "Modify people quantity":
        bot.send_message(message.chat.id, text='Enter quantity of adults and kids.',reply_markup=mk.people_markup)
        bot.set_state(message.from_user.id, Filter.people, message.chat.id)
    elif message.text == "Choose prices":
        bot.send_message(message.chat.id, text='Type minimum and maximum price like ''100 200''.',reply_markup=mk.poor_markup)
        bot.set_state(message.from_user.id, Filter.price, message.chat.id)
    elif message.text == "Search":
        with (bot.retrieve_data(message.from_user.id, message.chat.id) as data):
            if data['regionId'] and data["checkInDate"] and data["checkOutDate"] and data['adults'] and data["price"]['min'] and data["price"]['max']:
                HistorySearch.create(tg_id=message.from_user.id, search_settings=data)
                bot.set_state(message.from_user.id, Filter.searching, message.chat.id)
                data['site_response'] = req_2(
                    data['regionId'], data["checkInDate"]['day'], data["checkInDate"]['month'],
                    data["checkInDate"]['year'], data["checkOutDate"]['day'], data["checkOutDate"]['month'],
                    data["checkOutDate"]['year'], data['adults'], data['children'], data["price"]["min"],
                    data["price"]['max'])
                result_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for i_item in data['site_response']:
                    btn = types.KeyboardButton('{}'.format(i_item['name']))
                    result_markup.add(btn)
                result_markup.add(mk.btn_cancel)
                bot.send_message(message.chat.id, text='We have got next hotels',
                                 reply_markup=result_markup)
            else:
                bot.send_message(message.chat.id, text='You didnt fill all fields required for search',
                                 reply_markup=mk.markup_main)


@bot.message_handler(state=Filter.city)
def choose_city_2(message):
    if message.text != 'Cancel':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        response = req_1(message.text)
        i = 0
        for i_elem in response:
            if i_elem["type"] == "CITY":
                search.id_map[i_elem['regionNames']['fullName']] = i_elem["gaiaId"]
                i += 1
                i_btn = types.InlineKeyboardButton(i_elem['regionNames']['fullName'],
                                                   callback_data=i_elem["regionNames"]["fullName"])
                markup.add(i_btn)
        markup.add(mk.btn_cancel)
        if i > 0:
            bot.send_message(message.chat.id,
                             text="Please confirm your city choice.", reply_markup=markup)
            bot.set_state(message.from_user.id, Filter.city_confirm, message.chat.id)
        else:
            bot.send_message(message.chat.id, text="There is no match to your request, try this command again.")
    else:
        bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
        bot.send_message(message.chat.id, text='You are back at search settings..Choose other option to modify'
                                               ' or start your search!', reply_markup=mk.markup_main)


@bot.message_handler(state=Filter.city_confirm)
def confirm_city(message):
    if message.text != 'Cancel':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['regionId'] = search.id_map[message.text]
        search.id_map.clear()
        bot.send_message(message.chat.id, text='City chosen successfully!.Choose other option to modify'
                                               ' or start your search!', reply_markup=mk.markup_main)
        bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
    else:
        bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
        bot.send_message(message.chat.id, text='You are back at search settings..Choose other option to modify'
                                               ' or start your search!', reply_markup=mk.markup_main)


@bot.message_handler(state=Filter.dates)
def choose_date(message):
    if message.text != 'Cancel':
        result = re.findall(r'\d{1,2}-\d{1,2}-\d\d\d\d \d{1,2}-\d{1,2}-\d\d\d\d', message.text)
        if result:
            dates = message.text.split(' ')
            try:
                date_times = [datetime.strptime(date, '%d-%m-%Y') for date in dates]
                if date_times[0] <= date_times[1]:
                    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                        data["checkInDate"] = {
                            "day": date_times[0].day,
                            "month":date_times[0].month,
                            "year": date_times[0].year
                        }
                        data["checkOutDate"] = {
                            "day": date_times[1].day,
                            "month": date_times[1].month,
                            "year": date_times[1].year
                        }
                    bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
                    bot.send_message(message.chat.id, text='Dates set successfully! Choose other option to modify or '
                                                           'start your search!', reply_markup=mk.markup_main)
                else:
                    raise ValueError
            except ValueError:
                bot.send_message(message.chat.id, text='Incorrect date given, repeat enter please. '
                                                       'First date should be earlier than second')
        else:
            bot.send_message(message.chat.id, text='You wrote something wrong')
    else:
        bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
        bot.send_message(message.chat.id, text='You are back at search settings..Choose other option to modify'
                                               ' or start your search!', reply_markup=mk.markup_main)


@bot.message_handler(state=Filter.price)
def choose_price(message):
    if message.text != 'Cancel':
        result = re.findall(r'\d+ \d+', message.text)
        if result:
            if message.text.split(' ')[0] > message.text.split(' ')[1]:
                bot.send_message(message.chat.id, text='Prises are incorrect, first should be smalled than second.')
            else:
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    data["price"] = {
                        "max": message.text.split(' ')[0],
                        "min": message.text.split(' ')[1]
                    }
                bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
                bot.send_message(message.chat.id, text='Prices set successfully! Choose other option to modify or '
                                                       'start your search!', reply_markup=mk.markup_main)
        else:
            bot.send_message(message.chat.id, text='Format to enter price is ''min_price max_price''')
    else:
        bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
        bot.send_message(message.chat.id, text='You are back at search settings..Choose other option to modify'
                                               ' or start your search!', reply_markup=mk.markup_main)


@bot.message_handler(state=Filter.people)
def modify_people(message):
    if message.text != 'Cancel':
        if message.text == 'Adults':
            bot.send_message(message.chat.id, text='Enter quantity of adults.', reply_markup=mk.adult_markup)
            bot.set_state(message.from_user.id, Filter.people_adults, message.chat.id)
        elif message.text == 'Children':
            bot.send_message(message.chat.id, text='Enter ages of children, split with space.', reply_markup=mk.poor_markup)
            bot.set_state(message.from_user.id, Filter.people_children, message.chat.id)
    else:
        bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
        bot.send_message(message.chat.id, text='You are back at search settings..Choose other option to modify'
                                               ' or start your search!', reply_markup=mk.markup_main)


@bot.message_handler(state=Filter.people_adults)
def modify_adults(message):
    if message.text != 'Cancel':
        if 0 < int(message.text) < 10:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data["adults"] = int(message.text)
                data["children"] = []
            bot.send_message(message.chat.id, text='Quantity of adults saved successfully! Change persons settings'
                                                   ' or press Cancel to other settings and search.',
                             reply_markup=mk.people_markup)
            bot.set_state(message.from_user.id, Filter.people, message.chat.id)
        else:
            bot.send_message(message.chat.id, text='You too many persons or wrong symbol. Please try again',
                             reply_markup=mk.poor_markup)
    else:
        bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
        bot.send_message(message.chat.id, text='You are back at search settings..Choose other option to modify'
                                               ' or start your search!', reply_markup=mk.markup_main)


@bot.message_handler(state=Filter.people_children)
def modify_child(message):
    if message.text != 'Cancel':
        result = re.findall(r'\d{1,2}', message.text)
        if result:
            search.children.clear()
            result_row = message.text.split(' ')
            for i_item in result_row[-1::-1]:
                if int(i_item) >= 16:
                    result_row.remove(i_item)
                else:
                    search.children.append({"age": int(i_item)})
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data["children"] = search.children
            bot.send_message(message.chat.id, text='Quantity of children saved successfully! Children ages set:'
                                                   ' {} Change persons settings or'
                                                   ' press Cancel to other settings and search.'.format(result_row),
                             reply_markup=mk.people_markup)
            bot.set_state(message.from_user.id, Filter.people, message.chat.id)
        else:
            bot.send_message(message.chat.id, text='You entered something wrong, please repeat.',
                             reply_markup=mk.poor_markup)
    else:
        bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
        bot.send_message(message.chat.id, text='You are back at search settings..Choose other option to modify'
                                               ' or start your search!', reply_markup=mk.markup_main)


@bot.message_handler(state=Filter.searching)
def modify_adults(message):
    if message.text != 'Cancel':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            for i_item in data['site_response']:
                if i_item['name'] == message.text:
                    summary_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn = types.KeyboardButton("Get summary")
                    summary_markup.add(btn).add(mk.btn_cancel)
                    data['id_for_summary'] = i_item['id']
                    bot.set_state(message.from_user.id, Filter.summary, message.chat.id)
                    bot.send_photo(message.chat.id, photo=i_item["propertyImage"], reply_markup=summary_markup)
    else:
        bot.set_state(message.from_user.id, Filter.choose, message.chat.id)
        bot.send_message(message.chat.id, text='You are back at search settings..Choose other option to modify'
                                               ' or start your search!', reply_markup=mk.markup_main)


@bot.message_handler(state=Filter.summary)
def modify_adults(message):
    if message.text != 'Cancel':
        if message.text == 'Get summary':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                link = 'https://www.hotels.com/h{}.Hotel-Information'.format(data['id_for_summary'])
                HistorySummary.create(
                    tg_id=message.from_user.id,
                    summary_id=data['id_for_summary'],
                    hotel_link=link)
                answer = req_3(data['id_for_summary'])
                result_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for i_item in data['site_response']:
                    btn = types.KeyboardButton('{}'.format(i_item['name']))
                    result_markup.add(btn)
                result_markup.add(mk.btn_cancel)
                bot.send_message(message.chat.id, text=answer, reply_markup=result_markup)
                bot.set_state(message.from_user.id, Filter.searching, message.chat.id)
    else:
        bot.set_state(message.from_user.id, Filter.searching, message.chat.id)
        result_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            for i_item in data['site_response']:
                btn = types.KeyboardButton('{}'.format(i_item['name']))
                result_markup.add(btn)
            result_markup.add(mk.btn_cancel)
            bot.send_message(message.chat.id, text='You are back at search settings..Choose other option to modify'
                                                   ' or start your search!', reply_markup=result_markup)