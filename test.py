"""response = "Фролов Е.А."
d = response.split()
print(d)
if d[0].count('.') > 0:
    en = d[0]
    las = d[1]
else:
    en = d[1]
    las = d[0]

print(las, en)
    """
"""
from parser import get_lst_prepod
from sqlighter import SQLighter

db = SQLighter('bd.db')
db.create_table()

for i in get_lst_prepod():
    print(i)
    db.add_teacher(*i)"""

from parser import get_resp_prepod
from sqlighter import SQLighter

db = SQLighter('bd.db')
db.create_timetable(4)
for key, item in get_resp_prepod(25).items():
    print(key, end=': \n')
    for key1, item in item.items():
        print(key1, *item)
        print()
    print()