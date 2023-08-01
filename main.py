import flet as ft
import sqlite3
import os
import time

class sql_controller:
    con = None
    cur = None
    last_object = 0
    def __init__(self):
        if ('main.db' in (os.listdir(os.path.realpath(__file__)[:-7] + 'db_folder') )):
            self.con = sqlite3.connect("db_folder/main.db")
            self.cur = self.con.cursor()
        else:
            self.con = sqlite3.connect("db_folder/main.db")
            self.cur = self.con.cursor()
            self.cur.execute("""CREATE TABLE expenditure(id INT auto_increment NOT NULL PRIMARY KEY, name_expenditure VARCHAR(100) NOT NULL)""")
            self.con.commit()

            # просмотреть список таблиц
            # res = self.cur.execute("SELECT name FROM sqlite_master")

            # self.cur.execute("""INSERT INTO expenditure VALUES(0, 'test_ilyA')""")
            # self.con.commit() # закинуть в бд
            # res = self.cur.execute('SELECT * FROM expenditure')

        res = self.cur.execute('SELECT Max(id) from expenditure')
        try:
            self.last_object = int(list(res.fetchone())[0]) + 1
        except:
            self.last_object = 0
        self.cur.close()

    def adding_categor_sql(self, word):
        self.con = sqlite3.connect("db_folder/main.db")
        self.cur = self.con.cursor()
        res = self.cur.execute(f"""SELECT name_expenditure
FROM expenditure
WHERE  name_expenditure = '{word}'
""")


#         res = self.cur.execute(f"""SELECT *
#         FROM expenditure
#         """)
        if res.fetchall().__len__() == 0:

            self.cur = self.cur.execute(f"""INSERT INTO expenditure VALUES({self.last_object}, '{word}')""")
            self.last_object +=1
            self.con.commit()

            return True
        self.cur.close()

    def get_all_meanings(self):
        self.con = sqlite3.connect("db_folder/main.db")
        self.cur = self.con.cursor()
        res = self.cur.execute(f"""SELECT name_expenditure
        FROM expenditure""")
        return list(res.fetchall())



def categor_change(page: ft.Page):
    pass

def main(page: ft.Page):

    db_controller = sql_controller()


    def clicked_add_categor(e):
        pass
    def clicked_start(e):

        page.go("/categor")

    def creating_buttons():
        buttons = []

        buttons.append(
            ft.ElevatedButton('change categories', on_click=clicked_add_categor, width=300, height=100, bgcolor=ft.colors.BLUE_100)
        )

        buttons.append(
            ft.ElevatedButton('debit', on_click=clicked_start, width=300, height=100, bgcolor=ft.colors.GREEN_ACCENT_100, )
        )
        return buttons



    wrapper_categor_list = ft.Ref[ft.Column]()
    categor_name = ft.Ref[ft.TextField]()

    def adding_categor(e):
        if categor_name.current.value.__len__() < 1:
            pass
        else:
            value = categor_name.current.value
            # current_color = ft.colors
            wrapper_categor_list.current.controls.append(
                ft.Container(content=ft.Row([ft.Text(f"Hello, {value}!")]), bgcolor=ft.colors.BLUE_100)
            )
            db_controller.adding_categor_sql(f'{value}')
            page.update()

    def adding_categor_from_bd(is_it, name):
        # current_color = ft.colors
        wrapper_categor_list.current.controls.append(
            ft.Container(content=ft.Row([ft.Text(f"Hello, {name}!")]), bgcolor=ft.colors.BLUE_100)
        )
        page.update()


    def show_categor():
        return db_controller.get_all_meanings()

    def route_change(route):
        page.views.clear()

        page.views.append(
            ft.View(
                '/',
                [
                    ft.Row([
                        ft.Column(spacing=40, controls=creating_buttons()),
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ]
            )
        )
        if page.route == "/categor":

            page.views.append(
                ft.View(
                    "/categor",
                    [
                        ft.AppBar(title=ft.Text("Categor"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Column([

                            ft.TextField(ref=categor_name, label='adding categor'),
                            ft.ElevatedButton('add categor', on_click=adding_categor),
                            ft.Column(ref=wrapper_categor_list, spacing=40)
                        ])
                    ],
                )
            )
            categors_ready_list = show_categor()
            print(categors_ready_list,'ilya')
            for categor in categors_ready_list:
                adding_categor_from_bd(True, categor)


        page.update()


    # def categories_show:

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)














ft.app(target=main, view=ft.AppView.FLET_APP)
