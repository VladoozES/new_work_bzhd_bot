'''
Программа для формирования массивов данных, которые пойдут в БД. Массивы дальше идут в help_working_bd.py в качестве
параметра records.
'''
import re


good_text = open('good.txt')
good_list = [value.rstrip() for value in good_text]
good_text.close()
bad_text = open('bad.txt')
bad_list = [value.rstrip() for value in bad_text]
bad_text.close()

def fuck_it_func(id_value, text_value, links_value):
    scr_id = id_value

    scr_text = text_value
    if id_value in good_list:
        scr_type = 'good'
    elif id_value in bad_list:
        scr_type = 'bad'
    else:
        scr_type = 'other'
    scr_links = links_value
    return "('{0}', '{1}', '{2}', '{3}'),\n".format(scr_id, scr_text, scr_type, scr_links)


text = open('XYN.txt')
new_text = open('resXYN.txt', 'w')
for i in text:
    temp = re.split('<>', i.rstrip())
    new_text.write(fuck_it_func(temp[0], temp[1], temp[2]))
text.close()
new_text.close()
