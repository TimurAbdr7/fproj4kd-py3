import telebot
from telebot import types

TOKEN = "TOKEN"
bot = telebot.TeleBot(TOKEN)


waiting_for_photo = set()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("Как оформить заказ?")
    btn2 = types.KeyboardButton("Как узнать статус заказа?")
    btn3 = types.KeyboardButton("Как отменить заказ?")
    btn4 = types.KeyboardButton("Товар пришел поврежденным")
    btn5 = types.KeyboardButton("Связаться с техподдержкой")
    btn6 = types.KeyboardButton("Информация о доставке")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)

    bot.send_message(
        message.chat.id,
        "Здравствуйте! Я бот техподдержки магазина.\nВыберите вопрос:",
        reply_markup=markup
    )


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.chat.id in waiting_for_photo:
        waiting_for_photo.remove(message.chat.id)

        bot.reply_to(
            message,
            "Спасибо за фотографии. Ваша заявка принята. Наш сотрудник свяжется с вами позже."
        )


@bot.message_handler(func=lambda message: True)
def support(message):
    text = message.text.lower()

    if "оформить заказ" in text:
        bot.reply_to(
            message,
            'Для оформления заказа выберите товар, нажмите "Добавить в корзину", затем перейдите в корзину и завершите покупку.'
        )

    elif "статус" in text:
        bot.reply_to(
            message,
            'Статус заказа можно посмотреть в разделе "Мои заказы" в вашем аккаунте.'
        )

    elif "отменить заказ" in text:
        bot.reply_to(
            message,
            'Свяжитесь со службой поддержки как можно скорее. Мы постараемся отменить заказ до отправки.'
        )

    elif "поврежден" in text:
        waiting_for_photo.add(message.chat.id)

        bot.reply_to(
            message,
            "Пожалуйста, отправьте фотографию поврежденного товара."
        )

    elif "техподдерж" in text:
        bot.reply_to(
            message,
            'Связаться с техподдержкой можно по телефону на сайте или через этот чат-бот.'
        )

    elif "доставк" in text:
        bot.reply_to(
            message,
            'Информация о доставке доступна на странице оформления заказа.'
        )

    elif "оплата" in text or "сайт" in text:
        bot.reply_to(
            message,
            "Ваш запрос передан программистам."
        )

    elif "товар" in text or "заказ" in text:
        bot.reply_to(
            message,
            "Ваш запрос передан в отдел продаж."
        )

    else:
        bot.reply_to(
            message,
            "Не удалось найти ответ. Ваш запрос передан специалисту."
        )


bot.infinity_polling()