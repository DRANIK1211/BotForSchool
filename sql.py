import sqlite3 as sql

con = sql.connect("base.db")
cursor = con.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS users ("
    "id INTEGER PRIMARY KEY,"
    "username TEXT NOT NULL,"
    "role TEXT NOT NULL,"
    "count INTEGER"  # User, Admin, IT, Xoz
    ")"
)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS applications ("
    "id INTEGER PRIMARY KEY,"
    "sendersName TEXT NOT NULL,"
    "room TEXT NOT NULL,"
    "description TEXT NOT NULL,"
    "departament TEXT NOT NULL,"
    "date TEXT NOT NULL,"
    "status TEXT NOT NULL,"
    "performerName TEXT DEFAULT 'Not Started'"
    ")"
)


def search_user(id_user):
    user = cursor.execute("SELECT * FROM users WHERE id = ?", (id_user,)).fetchall()
    return user
    # Ищем в таблице users людей с id, в ответе массив [id, username, role, count]


def add_user(mas):  # Принимает массив параметров в формате [id, username, role, count]
    res = True
    try:  # Пробуем зарегистрировать пользователя. Если ошибок нет, возвращаем истину
        cursor.execute("INSERT INTO users (id, username, role, count) VALUES (?, ?, ?, ?)", mas)
        con.commit()
    except Exception as e:  # Если возникли ошибки, возвращаем для вывода
        res = f"Ошибка при добавлении пользователя: {e}"
    return res
    # Регистрация людей в бд


def send_application(username, cab, opis, otdel, date):
    st = "Отправлена"
    length = len(cursor.execute("SELECT * FROM applications").fetchall())
    try:
        res = cursor.execute(
            f'''INSERT INTO applications
            (id, sendersName, room, description, departament, date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (length, username, cab, opis, otdel, date, st))
    except Exception as e:  # Если возникли ошибки, возвращаем для вывода
        res = f"Ошибка: {e}"
    con.commit()
    return [length, res]


def get_otdel(otdel):
    return cursor.execute(f"SELECT id FROM users WHERE role = ?", (otdel,)).fetchall()


def delete_application_user(num):
    performerName = cursor.execute(f"SELECT performerName FROM applications WHERE id = ?", (num,)).fetchall()[0][0]
    status = cursor.execute("SELECT status FROM applications WHERE id = ?", (num,)).fetchall()[0][0]
    if status == "Выполнена" or status == "Удалена":
        return status
    cursor.execute(f"UPDATE applications SET status = ? WHERE id = ?", ("Удалена", num,))
    con.commit()
    if performerName != "Not Started":
        return cursor.execute("SELECT id FROM users WHERE username = ?", (performerName,)).fetchall()[0][0]
    else:
        return "Not Started"


def get_applications_user(id):
    username = cursor.execute("SELECT username FROM users WHERE id = ?", (id,)).fetchall()[0][0]
    mas_applications = cursor.execute("SELECT * FROM applications WHERE sendersName = ? AND status IN (?, ?)",
                                      (username, "Отправлена", "Выполняется")).fetchall()
    return mas_applications


def get_applications_otdel(id):
    user_role = cursor.execute("SELECT role FROM users WHERE id = ?", (id,)).fetchall()[0][0]
    mas_applications = cursor.execute("SELECT * FROM applications WHERE departament = ?"
                                      " AND status = ?", (user_role, "Отправлена")).fetchall()
    return mas_applications


def get_status_application(id):
    status = cursor.execute("SELECT status FROM applications WHERE id = ?", (id,)).fetchall()[0][0]
    name_user = cursor.execute("SELECT sendersName FROM applications WHERE id = ?", (id,)).fetchall()[0][0]
    id_user = cursor.execute("SELECT id FROM users WHERE username = ?", (name_user,)).fetchall()[0][0]
    return [status, id_user, name_user]


def execute_application(id_user, id_application):
    cursor.execute("UPDATE applications SET status = ? WHERE id = ?",
                   ("Выполняется", id_application))
    name = cursor.execute("SELECT username FROM users WHERE id = ?", (id_user,)).fetchall()[0][0]
    cursor.execute("UPDATE applications SET performerName = ? WHERE id = ?",
                   (name, id_application))
    con.commit()


def execute_application_finish(id):
    cursor.execute("UPDATE applications SET status = ? WHERE id = ?",
                   ("Выполнена", id))
    username = cursor.execute("SELECT performerName FROM applications WHERE id = ?", (id,)).fetchall()[0][0]
    if username != "Not Started":
        count = int(cursor.execute("SELECT count FROM users WHERE username = ?", (username,)).fetchall()[0][0])
        count += 1
        cursor.execute("UPDATE users SET count = ? WHERE username = ?", (count, username))
    con.commit()


def search_id(id_application):
    username = cursor.execute("SELECT sendersName FROM applications WHERE id = ?", (id_application,)).fetchall()[0][0]
    user_id = cursor.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchall()[0][0]
    return user_id


def add_app():
    st = "Отправлена"
    length = len(cursor.execute("SELECT * FROM applications").fetchall())
    try:
        res = cursor.execute(
            f'''INSERT INTO applications
                (id, sendersName, room, description, departament, date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (length, "путинцев тарас андреевич", "13244", "апвпава", "ИТ", "2025-02-05 20:58", st))
    except Exception as e:  # Если возникли ошибки, возвращаем для вывода
        print(f"Ошибка: {e}")
    con.commit()


def delete(id):
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    con.commit()


con.commit()
