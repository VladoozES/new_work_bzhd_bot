import re
import sqlite3

# '''
records = [('581',
            'Человек перед вами упал на асфальт и ударился головой, у него большая рана на голове, идет кровь из носа и ушей',
            'other', '5811 5812'),
           ('5811', 'Вызвать скорую, убедиться что человеку ничего не угрожает и оставить его', 'other', '58111'),
           ('58111', 'Вы оставили человека с переломом черепа одного, вы вообще в своем уме', 'bad', '03'),
           ('5812', 'Вызвать скорую, оценить сознание и дыхание человека', 'other', '58121'),
           ('58121', 'Человек находится в сознании', 'other', '581211 581212 581213'),
           ('581212', 'Посадить человека, при возможности поднять, чтобы кровь уходила от головы', 'bad', '03'),
           ('581213', 'Положить человека, запрокинув голову, чтобы предотвратить кровотечение из носа', 'bad', '03'),
           ('581211', 'Положить человека на спину с приподнятой головой и плечами', 'other', '5812111 5812112'),
           ('5812112', 'Закрыть ушные раковины и нос повязкой, чтобы предотвратить вытекание жидкости', 'bad', '03'),
           ('5812111', 'Закрыть ушные раковины и нос повязкой, давая жидкости вытекать', 'good', '03'),
           ]

con = sqlite3.connect('main_data_base.db')
cur = con.cursor()
for tup in records:
    cur.execute(
        "INSERT INTO cells_id VALUES ('{0}', '{1}', '{2}', '{3}')".format(tup[0], tup[1], tup[2], tup[3]))
cur.close()
con.commit()
con.close()
# '''

'''
con = sqlite3.connect('main_data_base.db')
cur = con.cursor()
cur.execute('CREATE TEMPORARY TABLE t1_backup(cell_id, text, type, links);')
cur.execute('INSERT INTO t1_backup SELECT cell_id, text, type, links FROM cells_id;')
cur.execute('DROP TABLE cells_id;')
cur.execute('CREATE TABLE cells_id(cell_id, text, type, links);')
cur.execute('INSERT INTO cells_id SELECT cell_id, text, type, links FROM t1_backup;')
cur.execute('DROP TABLE t1_backup;')
# cur.execute("DELETE FROM cells_id WHERE cell_id='03'")
# cur.execute("UPDATE cells_id SET links='03' WHERE cell_id='01'")
cur.close()
con.commit()
con.close()
'''
'''
con = sqlite3.connect('main_data_base.db')
cur = con.cursor()
cur.execute("UPDATE users_id SET Surname='{1}' WHERE chat_id='{0}'")
cur.close()
con.commit()
con.close()
'''
