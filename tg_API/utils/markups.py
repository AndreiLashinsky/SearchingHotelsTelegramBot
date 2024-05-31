from telebot import types


def do_main_markup():
    markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Choose city")
    btn2 = types.KeyboardButton("Choose dates")
    btn3 = types.KeyboardButton("Modify people quantity")
    btn4 = types.KeyboardButton("Choose prices")
    markup_main.add(btn1).add(btn2).add(btn3).add(btn4)
    return markup_main


markup_main = do_main_markup()
btn_cancel = types.KeyboardButton('Cancel')
btn_search = types.KeyboardButton('Search')
poor_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
poor_markup.add(btn_cancel)
markup_main.add(btn_search)

people_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_adults = types.KeyboardButton('Adults')
btn_child = types.KeyboardButton('Children')
people_markup.add(btn_adults).add(btn_child).add(btn_cancel)

adult_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
for i_num in range(6):
    btn = types.KeyboardButton('{}'.format(i_num + 1))
    adult_markup.add(btn)
adult_markup.add(btn_cancel)