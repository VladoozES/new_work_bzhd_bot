import re
import sqlite3


class Cell(object):
    def __init__(self, cell_id: str):
        con = sqlite3.connect('main_data_base.db')
        cursor = con.cursor()
        self.id = cell_id
        self.text = cursor.execute("SELECT text FROM cells_id WHERE cell_id='{0}'".format(cell_id)).fetchall()[0][0]
        self.type = cursor.execute("SELECT type FROM cells_id WHERE cell_id='{0}'".format(cell_id)).fetchall()[0][0]
        self.links = re.split(' ', cursor.execute(
            "SELECT links FROM cells_id WHERE cell_id='{0}'".format(cell_id)).fetchall()[0][0])  # links в БД:'1123 11234'
        self.point = int(cursor.execute("SELECT point FROM cells_id WHERE cell_id='{0}'".format(cell_id)).fetchall()[0][0])
        cursor.close()
        con.commit()
        con.close()
