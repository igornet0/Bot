import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def create_table(self):
        with self.connection:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS TEACHERS (
        						id		   INTEGER NOT NULL PRIMARY KEY,
        						last_name	   STRING,
        						initials     STRING,
        						post STRING,
        						)''')

    def add_teacher(self, last_name, initials, post):
        with self.connection:
            self.cursor.execute("INSERT INTO `TEACHERS` (`first_name`, `initials`, `post`) VALUES(?,?,?)",
                                (last_name, initials, post))

    def delet_teacher(self, last_name, initials):
        with self.connection:
            self.cursor.execute("DELETE FROM `TEACHERS` WHERE `last_name` = ? AND `initials` = ?", (last_name,initials))

    def create_timetable(self, id):
        with self.connection:
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS TIMETABLE_{id}  (
        						id		   INTEGER NOT NULL PRIMARY KEY,
        						weekday	   STRING,
        						subject     STRING,
        						group STRING,
        						priority STRING,
        						)''')

    def add_timetable(self, id, weekday, subject, group, priority):
        with self.connection:
            self.cursor.execute(f"INSERT INTO `TIMETABLE_{id}` (`weekday`, `subject`, `group`, `priority`) VALUES(?,?,?, ?)",
                                (weekday, subject, group, priority))

    def get_id(self, last_name, initials, post=None):
        with self.connection:
            if post is None:
                result = self.cursor.execute("SELECT id FROM `TEACHERS` WHERE `last_name` = ? AND `initials` = ?", (last_name,initials,)).fetchall()
                return result
            else:
                result = self.cursor.execute("SELECT id FROM `TEACHERS` WHERE `last_name` = ? AND `initials` = ? AND `post` = ?", (last_name, initials, post,)).fetchall()
                return result

    def get_taecher(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `TEACHERS`").fetchall()
            return result

    def get_timetable(self, id):
        with self.connection:
            result = self.cursor.execute(f"SELECT * FROM `TIMETABLE_{id}`").fetchall()
            return result