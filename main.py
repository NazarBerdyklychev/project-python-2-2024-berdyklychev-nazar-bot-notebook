import telebot
from telebot import types
import sqlite3


def init_table() -> None:
    '''создаём базу данных, если не создана'''
    connection = sqlite3.connect('database.sql')
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS notebook (id int auto_increment primary key, user_id int, note_name '
                   'varchar(50), data varchar(500))')
    connection.commit()

    cursor.close()
    connection.close()


init_table()

bot = telebot.TeleBot('7103964871:AAGJ8clv7BRKrf4LUiRhNQH8IHv_qYHdYTM')


@bot.message_handler(commands=['start'])
def start(message) -> None:
    '''/start'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton('Create new note')
    btn2 = types.KeyboardButton('Check the created one')
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, 'What do you want to do', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message) -> None:
    '''работа с отправленым сообщением'''
    user_id = message.from_user.id

    connection = sqlite3.connect('database.sql')
    cursor = connection.cursor()

    cursor.execute('SELECT note_name FROM notebook WHERE user_id = ?', (user_id,))
    note_names = cursor.fetchall()

    cursor.close()
    connection.close()

    if message.text == 'Create new note':
        bot.send_message(message.chat.id, 'Enter the name for the new note')
        bot.register_next_step_handler(message, new_note)

    elif message.text == 'Check the created one':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn = types.KeyboardButton('Go Back')
        markup.add(btn)

        if note_names:
            for ind in range(len(note_names)):
                btn = types.KeyboardButton(note_names[ind][0])
                markup.add(btn)

        bot.send_message(message.chat.id, 'Choose the note or go back', reply_markup=markup)

    elif message.text == 'Go Back':
        start(message)

    elif message.text[:7] == 'Change ' and message.text[-5:] == ' text':
        bot.send_message(message.chat.id, 'Enter the new text')
        bot.register_next_step_handler(message, change_note_text, message.text[7:-5])

    elif note_names and (message.text,) in note_names:
        note_name = message.text

        connection = sqlite3.connect('database.sql')
        cursor = connection.cursor()

        cursor.execute("SELECT data FROM notebook WHERE user_id = ? AND note_name = ?", (user_id, note_name))
        text = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if not text:
            text = 'This note is empty'

        bot.send_message(message.chat.id, text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton(f'Change {note_name} text')
        btn2 = types.KeyboardButton('Go Back')
        markup.add(btn1, btn2)

        bot.send_message(message.chat.id, 'What do you want to do', reply_markup=markup)


def new_note(message) -> None:
    '''создаём новую заметку'''
    user_id = message.from_user.id

    connection = sqlite3.connect('database.sql')
    cursor = connection.cursor()

    cursor.execute('SELECT note_name FROM notebook WHERE user_id = ?', (user_id,))
    note_names = cursor.fetchone()

    note_name = message.text

    if note_names and note_name in note_names:
        cursor.close()
        connection.close()

        bot.send_message(message.chat.id, 'Note with this name already exists')

        start(message)
        return

    cursor.execute("INSERT INTO notebook (user_id, note_name, data) VALUES (?, ?, ?)", (user_id, note_name, ''))
    connection.commit()

    cursor.close()
    connection.close()

    bot.send_message(message.chat.id, 'Done')
    start(message)


def change_note_text(message, note_name) -> None:
    '''редактируем текст заметки'''
    user_id = message.chat.id

    connection = sqlite3.connect('database.sql')
    cursor = connection.cursor()

    cursor.execute("UPDATE notebook SET data = ? WHERE user_id = ? AND note_name = ?", (message.text, user_id, note_name))
    connection.commit()

    cursor.close()
    connection.close()

    bot.send_message(message.chat.id, 'Done')
    start(message)


bot.polling(none_stop=True)
