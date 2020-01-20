from cell_class import Cell
import sqlite3
import re
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup


def user_id_record(user_id: str):
    con = sqlite3.connect('main_data_base.db')
    cur = con.cursor()
    cur.execute("INSERT INTO users_id (chat_id) VALUES ('{0}')".format(user_id))
    con.commit()
    con.close()


def is_already_in_bd(chat_id: str):
    con = sqlite3.connect('main_data_base.db')
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users_id WHERE chat_id='{0}'".format(chat_id)).fetchall()
    con.commit()
    con.close()
    if len(users) == 0:
        return False
    else:
        return True


def set_user_scene_id_now(chat_id: str, value: str):
    con = sqlite3.connect('main_data_base.db')
    cur = con.cursor()
    cur.execute("UPDATE users_id SET scene_id_now='{1}' WHERE chat_id='{0}'".format(chat_id, value)).fetchall()
    con.commit()
    con.close()


def get_now_scene_id(chat_id: str):
    con = sqlite3.connect('main_data_base.db')
    cur = con.cursor()
    res = cur.execute("SELECT scene_id_now FROM users_id WHERE chat_id='{0}'".format(chat_id)).fetchall()[0][0]
    cur.close()
    con.commit()
    con.close()
    return res


def set_user_name(chat_id: str, value: str):
    con = sqlite3.connect('main_data_base.db')
    cur = con.cursor()
    cur.execute("UPDATE users_id SET Name='{1}' WHERE chat_id='{0}'".format(chat_id, value)).fetchall()
    con.commit()
    con.close()


def get_cell_text(cell_id: str, chat_id: str):
    res = ''
    cell = Cell(cell_id)
    if len(cell.links) == 1:
        res = cell.text
    elif len(cell.links) > 1:
        res = cell.text + '\n'
        con = sqlite3.connect('main_data_base.db')
        cur = con.cursor()
        if cell.id in ['1', '2', '3', '4', '5', '6', '7']:
            for i in range(len(cell.links)):
                if cell.links[i] in get_user_winscene(chat_id):
                    res = res + '\n {0})'.format(i + 1) + \
                        cur.execute("SELECT text FROM cells_id WHERE cell_id='{0}' ".format(cell.links[i])).fetchall()[0][0] + '🔰'
                else:
                    res = res + '\n {0})'.format(i + 1) + \
                        cur.execute("SELECT text FROM cells_id WHERE cell_id='{0}'".format(cell.links[i])).fetchall()[0][0]
        else:
            for i in range(len(cell.links)):
                res = res + '\n {0})'.format(i + 1) + \
                      cur.execute("SELECT text FROM cells_id WHERE cell_id='{0}'".format(cell.links[i])).fetchall()[0][0]
        cur.close()
        con.commit()
        con.close()
    else:
        return 'У тебя в БД у ячейки нет ссылок вообще'
    return res


def get_custom_numeric_keyboard(cell_id: str):
    cell = Cell(cell_id)
    if len(cell.links) == 1:
        return None
    res_list = []
    for i in range(len(cell.links)):
        if i % 3 == 0:
            res_list.append([])
        res_list[i // 3].append(str(i + 1))
    return ReplyKeyboardMarkup(res_list, resize_keyboard=True, one_time_keyboard=True)


def set_user_surname(chat_id: str, value: str):
    con = sqlite3.connect('main_data_base.db')
    cur = con.cursor()
    cur.execute("UPDATE users_id SET Surname='{1}' WHERE chat_id='{0}'".format(chat_id, value)).fetchall()
    con.commit()
    con.close()


def get_user_winscene(chat_id: str):
    con = sqlite3.connect('main_data_base.db')
    cur = con.cursor()
    temp = cur.execute("SELECT win_scene FROM users_id WHERE chat_id='{0}'".format(chat_id)).fetchall()[0][0]
    cur.close()
    con.commit()
    con.close()
    if temp == None:
        res = []
    else:
        res = re.split(' ', temp)
    return res


def update_user_winscene(chat_id: str, winscene_id: str):
    con = sqlite3.connect('main_data_base.db')
    cur = con.cursor()
    temp = cur.execute("SELECT win_scene FROM users_id WHERE chat_id='{0}'".format(chat_id)).fetchall()[0][0]
    if temp == None:
        res = winscene_id
    else:
        if winscene_id in re.split(' ', temp):
            res = temp
        else:
            res = temp + ' {}'.format(winscene_id)
    cur.execute("UPDATE users_id SET win_scene='{1}' WHERE chat_id='{0}'".format(chat_id, res)).fetchall()
    con.commit()
    con.close()
