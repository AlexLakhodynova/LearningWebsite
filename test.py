import sqlite3
connection = sqlite3.connect("instance/tables.db")
cursor = connection.cursor()
cursor.execute("update user set task_date= ?", ("/Test1 2024-09-11 0/Test2 2024-09-15 0",))
connection.commit()