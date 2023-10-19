import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from images import *



# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        # верхняя палень для кнопок
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tree_scroll = ttk.Scrollbar(self)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self,
                                 columns=['ID', 'Name', 'Phone', 'Email'],
                                 height=45, show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tree.yview)

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('Name', width=300, anchor=tk.CENTER)
        self.tree.column('Phone', width=150, anchor=tk.CENTER)
        self.tree.column('Email', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='id')
        self.tree.heading('Name', text='ФИО')
        self.tree.heading('Phone', text='Телефон')
        self.tree.heading('Email', text='"Электронная почта')
        self.tree.pack(side=tk.LEFT)


        self.add_img = tk.PhotoImage(file='./img/add.png')
        self.butn_open_dialog = tk.Button(toolbar, bg='#d7d7d7',
                                          bd=0, image=self.add_img, command=self.open_dialog)
        self.butn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='./img/update.png')
        self.butn_edit_dialog = tk.Button(toolbar, bg='#d7d7d7',
                                          bd=0, image=self.update_img, command=self.open_update_dialog)
        self.butn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        self.butn_delete_dialog = tk.Button(toolbar, bg = '#d7d7d7',
                                            bd = 0, image=self.delete_img, command=self.delete_record
                                            )
        self.butn_delete_dialog.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='./img/search.png')
        self.butn_search_dialog = tk.Button(toolbar, bg='#d7d7d7',
                                            bd=0, image=self.search_img, command=self.open_search_dialog)
        self.butn_search_dialog.pack(side=tk.LEFT)

        self.butn_show_all = ttk.Button(toolbar,text='Показать всё', command=self.view_records)
        self.butn_show_all.place(x=570, y=40)
    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        if self.tree.selection():
            Update()
        else:
            messagebox.showinfo('info', 'Выберите запись!')

    def open_search_dialog(self):
        Search()

    def update_record(self, name, phone, email):
        update = '''
        UPDATE user SET Name = ?, Phone = ? , Email = ?
        WHERE ID=?
        '''
        self.db.cursor.execute(update, (name, phone, email,
                                        self.tree.set(self.tree.selection()[0], '#1')))
        self.db.connect.commit()
        self.view_records()

    def delete_record (self):
        if self.tree.selection():
            for i in self.tree.selection():
                self.db.delete_data(self.tree.set(i, '#1'))
            self.view_records()
        else:
            messagebox.showinfo('info','Выберите запись!')

    def search_record(self, name):
        name = ('%' + name + '%',)
        self.db.search_data(name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end', values=row) for row in self.db.cursor.fetchall()]



    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    def view_records(self):
        select_table = '''
        SELECT * FROM user 
        '''
        self.db.cursor.execute(select_table)
        r = db.cursor.fetchall()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in r]


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавление контакта')
        self.geometry('400x200')
        self.resizable(0, 0)
        self.grab_set()
        self.focus_set()

        label_name = ttk.Label(self, text='ФИО')
        label_name.place(x=50, y=20)
        label_phone = ttk.Label(self, text='Телефон')
        label_phone.place(x=50, y=50)
        label_email = ttk.Label(self, text='Электронная почта')
        label_email.place(x=50, y=80)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=170, y=20)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=170, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=170, y=80)

        self.butn_ok = ttk.Button(self, text='Добавить ')
        self.butn_ok.bind('<Button-1>', lambda ev: self.view.records(
            self.entry_name.get(), self.entry_phone.get(), self.entry_email.get()
        ))

        self.butn_ok.place(x=165, y=120)

        self.butn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.butn_cancel.place(x=165, y=160)


class Update(Child):
    def __init__(self):
        super().__init__()
        self.view = app
        self.db = db
        self.init_edit()
        self.default_data()

    def init_edit(self):
        self.butn_ok.destroy()
        self.title('Редактировать позицию')
        butn_edit = ttk.Button(self, text='Редактировать')
        butn_edit.place(x=160, y=120)
        butn_edit.bind('<Button-1>', lambda ev:
        self.view.update_record(self.entry_name.get(), self.entry_phone.get(), self.entry_email.get()))
        butn_edit.bind('<Button-1>', lambda ev : self.destroy(), add='+')

    def default_data(self):
        select_qr = '''
        SELECT * FROM user WHERE ID = ?
        '''
        self.db.cursor.execute(select_qr, (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0,row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])

class Search (tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(0, 0)
        self.grab_set()
        self.focus_set()

        label_search = ttk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y= 20, width=150)

        butn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        butn_cancel.place(x=185, y = 50)
        butn_search = ttk.Button(self, text='Поиск')
        butn_search.place(x=105, y= 50)
        butn_search.bind('<Button-1>', lambda ev: self.view.search_record(self.entry_search.get()))
        butn_search.bind('<Button-1>', lambda ev: self.destroy(), add='+')

class DataBase:
    def __init__(self):
        self.connect = sqlite3.connect('PhoneBook.db')
        self.cursor = self.connect.cursor()
        self.create_table()
        self.connect.commit()


    def create_table(self):
        table = '''
        CREATE TABLE IF NOT EXISTS user (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Phone TEXT,
        Email TEXT
        )
        '''
        self.cursor.execute(table)

    def insert_data(self, name, phone, email):
        insert = '''
        INSERT INTO user(Name, Phone, Email)
        VALUES (?,?,?)
        '''
        self.cursor.execute(insert, (name, phone, email))

        self.connect.commit()

    def delete_data(self, id):
        delete_qr = '''
        DELETE FROM user
        WHERE ID = ?
        '''
        self.cursor.execute(delete_qr, id)
        self.connect.commit()

    def search_data(self,name):
        select_qr = '''
        SELECT * FROM user WHERE Name LIKE ?
        '''
        self.cursor.execute(select_qr, name)
        self.connect.commit()
def main():
    global db
    global app
    image()
    root = tk.Tk()
    db = DataBase()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга ')
    root.geometry('665x450+300+200')
    root.resizable(0, 0)
    root.mainloop()
    db.connect.close()


if __name__ == '__main__':
    app: Main
    db: DataBase
    main()
