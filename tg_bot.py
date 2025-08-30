import telebot
from bs4 import BeautifulSoup
from telebot import types
import random
import bs4
import requests
import os

from telebot.asyncio_helper import send_message

bot = telebot.TeleBot('8327117191:AAGytn-Wf-qq7JU1I-3gIws-k5uSNkkMUok')

# id канала фанфики от спарсика "id": -1003085885462,
# id чата канала фанфики от спарсика"id": -1002995302819,
# id канала "id": -1003085885462,
# мой личный Yanikundr chat_id = 1277591715

@bot.message_handler(commands=['start'])
def startBot(message):
  first_mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>, привет!\n Я Спарсик, создаю красивые посты по фанфикам. Отправь мне ссылку на работу."
  markup = types.InlineKeyboardMarkup()

  bot.send_message(message.from_user.id, first_mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def TextBot(message = 0):
    if message:
        site = message.text
    else:
        site = 'https://author.today/work/415098'
        site = 'https://author.today/work/476181'

    data_fic = 0

    if site.__contains__('ficbook.net'):
        post = "Это ссылка на фикбук"
    elif site.__contains__('author.today'):
        post = "Это ссылка на AuthorToday"
        data_fic = getDataByToday()
    else:
        post = 'Я такой сайт пока не знаю('

    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'ru,en;q=0.9',
        'Content-Type': 'text/html; charset=utf-8',
        'refere': f'{site}',

    }

    resp = requests.get(site, headers=headers, timeout=3)
    # resp = requests.get(site)

    if data_fic:
        parse = bs4.BeautifulSoup(resp.text, 'lxml')

        data_post = getDataPost(parse, data_fic)

        print(data_post)

        post = create_post(data_post)

    send_ful_post(post)

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message = 0):
    try:
        if message:
            chat_id = message.from_user.id
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            with open(src, 'rb') as read_file:
                index = read_file.read()
        else:
            chat_id = 1277591715
            # src = 'чудо.html'
            src = 'чммсч.html'
            with open(src, 'rb') as read_file:
                index = read_file.read()

        parse = BeautifulSoup(index, 'lxml')

        os.remove(src)

        data_post = {}
        data_fic = 0

        data_post['href'] = parse.find("meta", property="og:url")['content']
        if  data_post['href'].__contains__('ficbook'):
            data_fic = getDataByFicbook()
        elif data_post['href'].__contains__('author.today'):
            data_fic = getDataByToday()
        else:
            post = 'Я такой сайт пока не знаю('

        if data_fic:
            data_post = getDataPost(parse, data_fic)
            post = create_post(data_post)

    except Exception as e:
        bot.reply_to(message, e)
        post = "Непредвиденная ошибка"


    send_ful_post(post)


@bot.callback_query_handler(func=lambda call: call.data == 'send1234')
def forward_to_the_channel(call):
    message = call.message
    post = message.html_text
    # канал
    chat_id = -1003085885462
    # чат
    # chat_id = -1002995302819
    markup = types.InlineKeyboardMarkup()
    bot.send_message(chat_id, post, parse_mode='html', reply_markup=markup)

    # Изменить сообдение
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, parse_mode='html', message_id=message_id, text=post)

def getDataByFicbook():

    data_fic = {
       'name' : ['h1', 'class', 'heading'],
       'href' : ['meta', 'property', 'og:url'],
       'creators.worker' : {'selector' : '.creator-info .text-muted'},
       'creators.name' : {'selector' : 'a.creator-username'},
       'creators.href' : {'selector' : 'a.creator-username'},
       'description' : {'selector' : 'div.js-public-beta-description'},
       'direction' : {'selector' : 'div.badge-with-icon.direction .badge-text'},
       'rating' : {'selector' : '[class*=badge-rating] .badge-text'},
       'tags' : {'selector' : '.tags a', 'array': '1'},
       'dop_desc.name' : {'selector' : '.description .mb-10 strong'},  # Размер Фэндом сборник
       'dop_desc.text' : {'selector' : '.description .mb-10 div'},
       # 'size' : {'selector' : '.description .mb-10:nth-child(3) div'},
        'site': {'selector': 'meta[name="application-name"]'},
    }

    return data_fic

def getDataByToday():
    data_fic = {
        'name' : {'selector' : 'h1'},
        'href' : {'selector' : '.work-details .btn-read-work'},
        'creators.name': {'selector': '.book-authors span a, .card-author a'},
        'creators.href': {'selector': '.book-authors span a, .card-author a'},
        'description': {'selector': '.card-description .rich-content:nth-child(1)'},
        'tags': {'selector': '.tags > a, .work-tags a', 'array': '1'},
        'genres': {'selector': '.book-genres, .work-stats a', 'array': '1'},
        'status': {'selector': '.book-meta-panel .label, .work-stats label.label'},
        'size': {'selector': '.work-stats .work-stat + div'},
        'rating': {'selector': '.book-stats .label-adult-only'},
        'site': {'selector': 'meta[name="application-name"]'},
    }

    return data_fic

def getDataPost(pars, get_data_fic):
    data_post = {}

    for key, value in get_data_fic.items():
        if key.__contains__('.'):
            keys = key.split('.')
            for k in keys:
                for i in keys:
                    if k not in data_post:
                        data_post[k] = {}

            i = 0

            creators = pars.select(value['selector'])

            for work in creators:
                if i not in data_post[keys[0]]:
                    data_post[keys[0]][i] = {}

                if keys[1] == "href":
                    data_post[keys[0]][i][keys[1]] = work.get("href")
                else:
                    data_post[keys[0]][i][keys[1]] = ' '.join(work.text.replace("\n", "").split())
                i += 1

        else:
            if 'selector' in value:
                creators = pars.select(value['selector'])

                for work in creators:
                    if key == "href":
                        data_post[key] = work.get("href")
                    elif key == 'site':
                        data_post[key] = work.get("content")
                    elif 'array' in value:
                        if key not in data_post:
                            data_post[key] = []
                            tags = []
                        for tag in work:
                            tags.append(tag.text.replace('/', "").replace(":", "").replace(" ", "_"))
                        data_post[key] = tags
                    else:
                        data_post[key] = ' '.join(work.text.replace("\n", "").split())

            else:
                if value[1] == "class":
                    data_post[key] = ' '.join(pars.body.find((value[0], {value[1]: value[2]})).text.replace("\n", "").split())
                elif key == "href":
                    data_post[key] = pars.find("meta", {value[1]: value[2]})['content']

    return data_post

def create_post(data_post):
    style_arr = { 'Джен': '5', 'Гет': '4', 'author.today': '3', 'Перевод': '3', 'Статья' : '0'}
    direct_arr = { 'Джен' : '👾',  'Гет' : '👩‍❤️‍👨',   'Статья' : '🗃️', }
    hust_arr = ['🖤', '💚', '♥️', '💙', '💛', '💜']
    book_arr = ['💻', '📗', '📕', '📘', '📙', '💟' ]
    pen_arr = ['✒️', '🍀️', '🖍️', '🖌️', '✏️', '☂️']
    tag_arr = ['🎮', '🐊️', '🌶️️', '🐋️', '🌻', '👾']
    acc_arr = ['🐈‍⬛️', '🐢', '🐞', '🫏', '🐝', '🍇']
    creat_arr = ['🐦‍⬛', '🦎', '🦀️', '🦕', '🐣', '☔️']
    sites_arr = {'Author.Today' : 'https://author.today', 'Книга Фанфиков': 'https://ficbook.net'}

    style = random.randint(0, 5)

    post = '#спарсик_делится' + "\n\n"

    if not data_post['href'].__contains__('https://'):
        dop = sites_arr[data_post['site']]
    else:
        dop = ''

    post += f"<b>{book_arr[style]} <a href=\"{dop}{data_post['href']}\">{data_post['name']}</a></b>\n\n"

    # создатели
    post += creat_arr[style] + " Создатели: "
    for i in data_post['creators']:
        if not data_post['creators'][i]['href'].__contains__('https://'):
            dop = sites_arr[data_post['site']]
        else:
            dop = ''
        post += f"<a href=\"{dop}{data_post['creators'][i]['href']}\">{data_post['creators'][i]['name']}</a> "

    post += "\n"
    if 'rating' in data_post:
        post += hust_arr[style] + " " + data_post['rating'] + '    '

    if 'direction' in data_post:
        post += direct_arr[data_post['direction']] + " " + data_post['direction'] + "\n"

    if 'dop_desc' in data_post:
        for i in data_post['dop_desc']:
            if data_post['dop_desc'][i]['name'] == 'Фэндом:' or data_post['dop_desc'][i]['name'] == 'Размер:':
                post += hust_arr[style] + " " + data_post['dop_desc'][i]['name'] + " " + data_post['dop_desc'][i]['text'] + "\n"
    post += "\n"

    if 'size' in data_post:
        post += hust_arr[style] + " " + 'Размер:' + " " + data_post['size'] + "\n"
    if 'status' in data_post:
        post += hust_arr[style] + " " + 'Статус:' + " " + "" + data_post['status'] + "\n"
    post += "\n"

    if 'tags' in data_post:
        post +=  tag_arr[style] + " Метки: "
        for tag in data_post['tags']:
            if len(tag) > 0:
                post += "#" + tag + " "
    post += "\n\n"

    if 'description' in data_post:
        post += pen_arr[style] + " Описание: <blockquote>" + data_post['description'] + "</blockquote>\n\n"

    # post += acc_arr[style] + " Наш канал с бесплатной рекламой работ: https://t.me/sparsik_fan\n\n"

    return post

def send_ful_post(post, chat_id = 1277591715):
    # chat_id = 1277591715

    markup = types.InlineKeyboardMarkup()
    # Переслать только для меня
    if chat_id == 1277591715:
        button_save = telebot.types.InlineKeyboardButton(text="Переслать в канал", callback_data='send1234')
        markup.add(button_save)
    # button_change = telebot.types.InlineKeyboardButton(text="Изменить",  callback_data='change_data')

    bot.send_message(chat_id, post, parse_mode='html', reply_markup=markup)

# handle_docs_photo()
# TextBot()

bot.infinity_polling()



# черновичное

# data_post['creators'] = {}

# i = 0
# for creators in pars.find_all('div', {'class': 'creator-info'}):
#     for work in creators.i:
#         data_post['creators'][i] = {}
#         data_post['creators'][i]['worker'] = work.text
#
#     for create in creators.find_all("a", {"class": "creator-username"}):
#         data_post['creators'][i]['name'] = create.text
#         data_post['creators'][i]['href'] = create.get("href")
#
#     i += 1

# i = 0
# for creators in pars.find_all('div', {'class': 'creator-info'}):
#     for work in creators.i:
#         data_post['creators'][i] = {}
#         data_post['creators'][i]['worker'] = work.text
#
#     for create in creators.find_all("a", {"class": "creator-username"}):
#         data_post['creators'][i]['name'] = create.text
#         data_post['creators'][i]['href'] = create.get("href")
#
#     i += 1