from cell_class import Cell
import sqlite3
import re
import db_working
from telegram import Bot
from telegram import Update
from telegram.ext import Filters
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler

from config import TG_TOKEN
from config import TG_API_URL


def do_start(bot: Bot, update: Update):
    if not db_working.is_already_in_bd(update.message.chat_id):
        db_working.user_id_record(update.message.chat_id)
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Привет! Назови своё имя',
        )
        db_working.set_user_scene_id_now(update.message.chat_id, '00')

    else:
        db_working.set_user_scene_id_now(update.message.chat_id, '03')
        bot.send_message(
            chat_id=update.message.chat_id,
            text=db_working.get_cell_text(db_working.get_now_scene_id(update.message.chat_id), update.message.chat_id),
            reply_markup=db_working.get_custom_numeric_keyboard(db_working.get_now_scene_id(update.message.chat_id))
        )


def do_test(bot: Bot, update: Update):
    try:
        pass  # write_cell_text(bot, update, '01')
    except:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Error'
        )


def do_any(bot: Bot, update: Update):
    work_cell = Cell(db_working.get_now_scene_id(update.message.chat_id))
    if work_cell.type == 'name':
        db_working.set_user_name(update.message.chat_id, update.message.text)
        db_working.set_user_scene_id_now(update.message.chat_id, '01')
        bot.send_message(
            chat_id=update.message.chat_id,
            text=db_working.get_cell_text('01', update.message.chat_id)
        )
    elif work_cell.type == 'surname':
        db_working.set_user_surname(update.message.chat_id, update.message.text)
        db_working.set_user_scene_id_now(update.message.chat_id, '03')
        bot.send_message(
            chat_id=update.message.chat_id,
            text=db_working.get_cell_text('03', update.message.chat_id),
            reply_markup=db_working.get_custom_numeric_keyboard('03')
        )
    elif work_cell.type == 'other':
        if len(work_cell.links) > 1:
            try:
                db_working.set_user_scene_id_now(update.message.chat_id, work_cell.links[int(update.message.text) - 1])
                work_cell = Cell(db_working.get_now_scene_id(update.message.chat_id))
                if not len(work_cell.links) < 2:
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text=db_working.get_cell_text(work_cell.id, update.message.chat_id),
                        reply_markup=db_working.get_custom_numeric_keyboard(
                            db_working.get_now_scene_id(update.message.chat_id))
                    )

            except:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='Неверный ввод'
                )
        while len(work_cell.links) == 1:
            if work_cell.type == 'good':
                db_working.update_user_winscene(update.message.chat_id, work_cell.id[:2])
                temp_photo = open(r'media_data/win.jpg', 'rb')
                bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=temp_photo
                )
            if work_cell.type == 'bad':
                temp_photo = open(r'media_data/wasted.jpg', 'rb')
                bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=temp_photo
                )
                temp_photo.close()
            db_working.set_user_scene_id_now(update.message.chat_id, work_cell.links[0])
            bot.send_message(
                chat_id=update.message.chat_id,
                text=db_working.get_cell_text(work_cell.links[0], update.message.chat_id),
                reply_markup=db_working.get_custom_numeric_keyboard(work_cell.links[0])
            )

            work_cell = Cell(work_cell.links[0])
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Неизвестный тип ячейки'
        )


def do_check(bot: Bot, update: Update):
    if str(update.message.chat_id) == '818351859':
        con = sqlite3.connect('main_data_base.db')
        cur = con.cursor()
        users = cur.execute("SELECT * FROM users_id").fetchall()
        cur.close()
        con.commit()
        con.close()
        for user in users:
            message = ''
            if user[3] != None:
                for branch in re.split(' ', user[3]):
                    print(branch)
                    con = sqlite3.connect('main_data_base.db')
                    cur = con.cursor()
                    message = message + '- ' + \
                              cur.execute("SELECT text FROM cells_id WHERE cell_id='{0}'".format(branch)).fetchall()[0][
                                  0] + '\n'
                    cur.close()
                    con.commit()
                    con.close()
            bot.send_message(
                chat_id=update.message.chat_id,
                text='{0} {1}:\n{2}'.format(user[1], user[2], message)
            )


def main():
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL
    )
    updater = Updater(
        bot=bot
    )

    test_handler = CommandHandler('test', do_test)
    start_handler = CommandHandler('start', do_start)
    check_handler = CommandHandler('check', do_check)
    message_handler = MessageHandler(Filters.text, do_any)

    updater.dispatcher.add_handler(test_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(check_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
