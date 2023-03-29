import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def create_table(self):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS TEACHERS (
        						id		       INTEGER NOT NULL PRIMARY KEY,
        						last_name	   STRING,
        						initials       STRING,
        						post           STRING,
        						value_teachers INTEGER
        						)""")

    def add_teacher(self, last_name, initials, post, value_teachers):
        with self.connection:
            self.cursor.execute("INSERT INTO `TEACHERS` (`last_name`, `initials`, `post`, `value_teachers`) VALUES(?,?,?,?)",
                                (last_name, initials, post, value_teachers,))

    def delet_teacher(self, last_name, initials):
        with self.connection:
            self.cursor.execute("DELETE FROM `TEACHERS` WHERE `last_name` = ? AND `initials` = ?", (last_name,initials,))

    def create_timetable(self, id):
        with self.connection:
            sql = """CREATE TABLE IF NOT EXISTS TIMETABLE_""" + str(id) + """ (
        						id		    INTEGER NOT NULL PRIMARY KEY,
        						weekday	    STRING,
        						number      STRING,
        						priority    STRING,
        						lesson      STRING,
        						subject     STRING,
        						place       STRING,
        						office      STRING,
        						groups       STRING
        						)"""

            self.cursor.execute(sql)


    def add_timetable(self, id, weekday, subject, group, priority, place, lesson, office, number):
        with self.connection:
            self.cursor.execute("INSERT INTO TIMETABLE_"+ str(id) +" (weekday, subject, groups, priority, place, lesson, office, number) VALUES(?,?,?,?,?,?,?,?)",
                                (weekday, subject, group, priority, place, lesson, office, number))

    def get_id(self, last_name, initials, post=None):
        with self.connection:
            if post is None:
                result = self.cursor.execute("SELECT id, value_teachers last_name FROM TEACHERS WHERE last_name = ? AND initials = ?", (last_name, initials)).fetchall()
            else:
                result = self.cursor.execute("SELECT id, value_tachers FROM TEACHERS WHERE last_name = ? AND initials = ? AND post = ?", (last_name, initials, post)).fetchall()
        return result

    def get_taecher(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `TEACHERS`").fetchall()
            return result

    def get_timetable(self, id):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM TIMETABLE_{id}").fetchall()
            return result