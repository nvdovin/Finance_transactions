from tkinter import ttk
from tkinter import *

import sqlite3
import os
from datetime import datetime


class Transactions:
    def __init__(self) -> None:
        if not os.path.exists('database'):
            os.mkdir('database')
        self.connect = sqlite3.connect('database/database.db')
        self.cursor = self.connect.cursor()

        self.root = Tk()
        self.root.geometry('600x800+300+100')
        self.root.title('Transactions database')
        self.root.resizable(False, False)

        self.transaction_var = IntVar(value=0)

        self.create_database()
        self.hat_form()
        self.root.mainloop

    def hat_form(self):
        """Блок с шапкой приложения"""
        self.main_frame = Frame(self.root, width=600, height=440)
        self.main_frame.pack()
        self.root.geometry(f'{self.main_frame["width"]}x{self.main_frame["height"]}')

        transaction_add = Radiobutton(self.main_frame, text='Внести', value=0, variable=self.transaction_var, font='10', command=self.add_form) 
        transaction_add.grid(row=0, column=1, columnspan=2, sticky='n')
        transaction_del = Radiobutton(self.main_frame, text='Удалить', value=1, variable=self.transaction_var, font='10', command=self.del_form)
        transaction_del.grid(row=0, column=3, columnspan=2, sticky='n')

    def start_form(self):
        """Запуск формы"""
        if self.transaction_var.get() == 0:
            self.add_form()
        else:
            self.del_form()

    def add_form(self):
        try:
            self.id_label.grid_forget()
            self.id_entry.grid_forget()
            self.del_button.grid_forget()
        except:
            pass

        grades_list = ["Еда", "Одежда", "Досуг", "Авто", "Жильё", "Прочее"]

        self.sum_label = Label(self.main_frame, text='Сумма', font='16')
        self.sum_label.grid(row=1, column=0, sticky='n', columnspan=2)

        self.title_label = Label(self.main_frame, text='Название', font='16')
        self.title_label.grid(row=1, column=2, sticky='n', columnspan=2)

        self.grade_label = Label(self.main_frame, text='Категория', font='16')
        self.grade_label.grid(row=1, column=4, sticky='n', columnspan=2)

        self.sum_entry = Entry(self.main_frame, font='13', width=17, border=1)
        self.sum_entry.grid(row=2, column=0, columnspan=2)

        self.title_entry = Entry(self.main_frame, font='13', width=17, border=1)
        self.title_entry.grid(row=2, column=2, columnspan=2)

        self.grade_listbox = ttk.Combobox(self.main_frame, font='13', width=17, values=grades_list)
        self.grade_listbox.grid(row=2, column=4, columnspan=2)

        self.enter_button = Button(self.main_frame, font='14', text='Внести', bd=5, width=40, height=1, command=self.enter_to_database)
        self.enter_button.grid(row=3, column=1, columnspan=4, rowspan=2, pady=10)

        self.build_short_table()

    def del_form(self):
        try:
            self.sum_label.grid_forget()
            self.title_label.grid_forget()
            self.grade_label.grid_forget()
            self.sum_entry.grid_forget()
            self.title_entry.grid_forget()
            self.grade_listbox.grid_forget()
            self.enter_button.grid_forget()
        except:
            pass

        self.id_label = Label(self.main_frame, text='ID записи', font='14')
        self.id_label.grid(row=1, column=1, columnspan=2, sticky='e')
        self.id_entry = Entry(self.main_frame, font='13', width=10)
        self.id_entry.grid(row=1, column=3, columnspan=2, sticky='w')

        self.del_button = Button(self.main_frame, text='Удалить запись', font='14', command=self.delete_from_database)
        self.del_button.grid(row=2, column=2, columnspan=2, pady=15)

        self.build_short_table()

    def build_short_table(self):
        """Создание короткой таблички внизу экрана"""
        show_database_button = Button(self.main_frame, text='Показать историю', font='10', height=1, width=50)
        show_database_button.grid(row=6, column=1, columnspan=4, rowspan=1, sticky='n', pady=30)

        self.short_table = ttk.Treeview(self.root, columns=['id', 'date', 'value', 'title', 'grade'])
        self.short_table.place(width=580, height=200, x=10, y=230)

        self.short_table.column('#0', width=0, anchor='center')                         #0

        self.short_table.column('id', width=20, anchor='center')                        #1
        self.short_table.heading('id', text='ID')

        self.short_table.column('date', width=90, anchor='center')                      #2
        self.short_table.heading('date', text='Дата')

        self.short_table.column('value', width=80, anchor='center')                     #3
        self.short_table.heading('value', text='Сумма')

        self.short_table.column('title', width=110, anchor='center')                    #4
        self.short_table.heading('title', text='Назваие операции')

        self.short_table.column('grade', width=90, anchor='center')                     #5
        self.short_table.heading('grade', text='Статья расходов')

        self.refresh_short_table()

        self.root.mainloop()

    def delete_from_database(self):
        """Удалить данную запись из базы данных"""
        id_from_entry = self.id_entry.get()

        # Получим список всех доступных для удаления записей
        self.cursor.execute(f'''SELECT "id" FROM transactions;''')
        id_list_from_database = self.cursor.fetchall()
        id_list = []
        for _id in id_list_from_database:
            id_list.append(f"{_id[0]}")

        # Удаляем данную запись из базы данных
        if id_from_entry in id_list:
            self.cursor.execute(f''' DELETE FROM "transactions" WHERE "id"={id_from_entry}''')
            print(f'Запись "{id_from_entry}" удалена')
        else:
            print(f'Нет записи с id {id_from_entry} в базе данных')
        self.id_entry.delete(0, END)
        self.refresh_short_table()

        self.build_short_table()

    def refresh_short_table(self):
        """Обновление короткой таблицы"""

        self.short_table.delete(*self.short_table.get_children())

        self.cursor.execute(f''' SELECT "id", "date_time", "money_value", "title", "grade"
                            FROM transactions
                            ORDER BY "id" DESC
                            LIMIT 8;''')
        transactions = self.cursor.fetchall()

        for t in transactions:
            self.short_table.insert('', END, values=t)

    def create_database(self):
        """#### Создаём базу данных, если её нет
        """

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS 
                            transactions
                            (
                            id INT UNIQUE,
                            date_time TEXT,
                            money_value FLOAT,
                            title TEXT,
                            grade TEXT
                            )''')

    def enter_to_database(self):
        """#### Внести запись в БД
        В зависимости от вида действия вносим или удаляем запись"""

        self.cursor.execute('SELECT "id" FROM transactions ORDER BY "id" DESC LIMIT 1;')
        last_id = self.cursor.fetchall()[0][0] + 1
        sum_value = self.sum_entry.get()
        title = self.title_entry.get()
        grade = self.grade_listbox.get()

        self.cursor.execute(f'''INSERT INTO transactions 
                            VALUES(
                            {last_id},
                            "{datetime.now()}",
                            {sum_value}, 
                            "{title}",
                            "{grade}"
                            ) ''')
        self.connect.commit()

        self.sum_entry.delete(0, END)
        self.title_entry.delete(0, END)
        self.grade_listbox.delete(0, END)

        self.refresh_short_table()
        self.root.mainloop()

app = Transactions()
app.add_form()