import pandas
import json
from tkinter import *
from tkinter import messagebox, filedialog
from business_journal import BusinessJournal
from balance import Balance
from financial_report import FinancialReport


class Menu:
    def __init__(self):
        self.remains_rows = 0
        self.ops_number = 0
        self.global_frame = None

    def create_starting_gui(self):  # Создание первоначального GUI

        def back_to_menu():
            root.destroy()
            self.create_starting_gui()

        def clear_and_proceed(function):  # Отчистка интерфейса и выбр дальнейшего действия
            self.clear()

            if function == "balance":  # При нажатии на кнопку "Баланс предприятия" - открытие меню баланса
                self.balance_menu()
            elif function == "operations":  # При нажатии на кнопку "Журнал..." - открытие меню хоз. операций
                self.operations_menu()
            elif function == "financial":
                self.financial_report_menu()

        root = Tk()
        root.title("Приложение по бухгалтерскому учету")

        self.global_frame = Frame(root, pady=30, padx=60)
        self.global_frame.grid(row=0, column=0)

        back_btn = Button(self.global_frame, text="Меню", command=back_to_menu)
        back_btn.grid(row=0, column=0)

        headline = Label(self.global_frame, text="Приложение для решения задач\nпо бухгалтерскому учету",
                         font=("Arial", 20, "bold"), padx=15, pady=10)
        headline.grid(row=0, column=1, columnspan=11)

        balance_btn = Button(self.global_frame, text="Баланс\nпредприятия",
                             command=lambda: clear_and_proceed(function="balance"), width=12, height=3)
        balance_btn.grid(row=1, column=0, columnspan=4)

        ops_btn = Button(self.global_frame, text="Журнал\nхозяйственных\nопераций",
                         command=lambda: clear_and_proceed(function="operations"), width=12, height=3)
        ops_btn.grid(row=1, column=4, columnspan=4, padx=10)

        financial_report_btn = Button(self.global_frame, command=lambda: clear_and_proceed(function="financial"),
                                      text="Отчет о\nфинансовых\nрезультатах", width=12, height=3)
        financial_report_btn.grid(row=1, column=8, columnspan=4)

        root.mainloop()

    def balance_menu(self):  # Отображение меню для открытия или создания баланса

        def clear_and_proceed(function):  # Отчистка интерфейса и дальнейшие действия
            if function == "open":  # Открытие баланса
                file_path = filedialog.askopenfilename(defaultextension=".json",
                                                       filetypes=[("JSON File", ".json")],
                                                       initialdir="/Users/midle/PycharmProjects/Сохраненные файлы "
                                                                  "по балансу")

                try:
                    with open(file_path, mode="r") as data_file:
                        data = json.load(data_file)

                    self.clear(headline="Бухгалтерский баланс")

                    balance = Balance()
                    balance.open_file(self.global_frame, data)
                except FileNotFoundError:
                    pass
            elif function == "create":  # Создание нового баланса
                property_rows = rows_entry.get()

                if property_rows == "":  # Если ничего не введенно, то кол-во данных по имуществу - 0
                    property_rows = 0
                try:
                    property_rows = int(property_rows)
                except ValueError:
                    messagebox.showerror(title="Возникла ошибка", message="Проверьте правильность введенных данных")
                else:
                    self.clear(headline="Бухгалтерский баланс")

                    balance = Balance()
                    balance.create_balance(self.global_frame, property_rows)

        open_balance_btn = Button(self.global_frame, text="Открыть\nфайл", width=12, height=3,
                                  command=lambda: clear_and_proceed("open"))
        open_balance_btn.grid(row=1, column=0, columnspan=12)

        # Отдельный Frame для пространства между виджетами
        frame = Frame(self.global_frame, pady=25)
        frame.grid(row=2, column=0, columnspan=12)

        rows_number_label = Label(frame, text="Укажите количество данных по имуществу:", pady=15)
        rows_number_label.grid(row=2, column=0, columnspan=6)

        rows_entry = Entry(frame)
        rows_entry.grid(row=2, column=6, columnspan=6)

        create_balance_btn = Button(frame, text="Создать\nфайл", width=12, height=3,
                                    command=lambda: clear_and_proceed("create"))
        create_balance_btn.grid(row=3, column=0, columnspan=12)

    def operations_menu(self):  # Отображение меню с определением параметров для журнала хозяйственных операций

        def clear_and_proceed(function):  # Отчистка интерфейса и дальнейшие действия
            def create_operations():
                business_journal = BusinessJournal()
                business_journal.create_operations(self.global_frame, self.remains_rows, self.ops_number)

            def check_ops():  # Выведение ошибки при пустой ячейке ввода количества операций
                try:
                    self.ops_number = int(ops_entry.get())
                    self.clear(headline="Журнал хозяйственных операций")
                    create_operations()
                except ValueError:
                    messagebox.showerror(title="Возникла ошибка",
                                         message="Введите количество операций для журнала хозяйственных "
                                                 "операций.")

            if function == "open":  # Открытие нового журнала хоз. операций
                filename = filedialog.askopenfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV File", ".csv")],
                    initialdir="/Users/midle/PycharmProjects/Сохраненные файлы по бух. учету")

                try:
                    with open(filename, mode="r") as data_file:
                        data = pandas.read_csv(data_file)

                        self.clear(headline="Журнал хозяйственных операций")

                        bj = BusinessJournal()
                        bj.open_file(self.global_frame, data)
                except FileNotFoundError:
                    pass
            elif function == "create":  # Создание нового журнала хоз. операций
                if accounts_remains_var.get():

                    # Выведение ошибки при нажатой кнопке "остатки на счетах" и пустой ячейки ввода остатков
                    try:
                        self.remains_rows = int(remains_rows_entry.get())
                    except ValueError:
                        messagebox.showerror(title="Возникла ошибка",
                                             message="Введите количество счетов с остатками.")
                    else:
                        check_ops()
                else:
                    check_ops()

        def check_remains_var():  # Изменение состояния поля для ввода - disabled и normal - для "остатки на счетах"
            if accounts_remains_var.get():
                remains_rows_entry.config(state='normal')
                remains_rows_label.config(fg="black")
            else:
                remains_rows_entry.delete(0, END)
                remains_rows_entry.config(state='disabled')
                remains_rows_label.config(fg="#D1D1D1")

        file_open_btn = Button(self.global_frame, text="Открыть\nфайл", width=12, height=3,
                               command=lambda: clear_and_proceed("open"))
        file_open_btn.grid(row=1, column=0, columnspan=12)

        ops_label = Label(self.global_frame, text="Укажите количество операций: ", pady=20)
        ops_label.grid(row=2, column=0, columnspan=6)

        ops_entry = Entry(self.global_frame)
        ops_entry.grid(row=2, column=6, columnspan=6)

        # Создание Frame для введения 'pady' для обоих элементов относительно других #
        remains_frame = Frame(self.global_frame, pady=20)
        remains_frame.grid(row=3, column=0, columnspan=12)

        # Введение Checkbutton и поля с числом счетов с остатками для "Остатков на счетах"
        accounts_remains_var = BooleanVar()
        accounts_remains_var.set(0)

        accounts_remains_btn = Checkbutton(remains_frame, text="Остатки на счетах",
                                           font=("Arial", 16, "normal"),
                                           variable=accounts_remains_var,
                                           onvalue=1, offvalue=0, command=check_remains_var)
        accounts_remains_btn.grid(row=3, column=0, columnspan=12)

        remains_rows_label = Label(remains_frame, text="Укажите количество счетов с остатками: ", fg="#D1D1D1")
        remains_rows_label.grid(row=4, column=0, columnspan=6)
        remains_rows_entry = Entry(remains_frame, state='disabled')
        remains_rows_entry.grid(row=4, column=6, columnspan=6)

        continue_btn = Button(self.global_frame, text="Создать\nфайл", width=12, height=3,
                              command=lambda: clear_and_proceed("create"))
        continue_btn.grid(row=5, column=0, columnspan=12)

    def financial_report_menu(self):  # Отображение меню "Отчета о финансовых результатах"

        def clear_and_proceed(function):  # Отчистка интерфейса и дальнейшие действия
            if function == "open":
                filename = filedialog.askopenfilename(
                    defaultextension=".json",
                    filetypes=[("JSON File", ".json")],
                    initialdir="/Users/midle/PycharmProjects/Сохраненные файлы по ОФР")
                try:
                    with open(filename, mode="r") as data_file:
                        data = json.load(data_file)

                        self.clear(headline="Отчет о финансовых результатах")

                        financial_report = FinancialReport()
                        financial_report.open_file(self.global_frame, data)
                except FileNotFoundError:
                    pass
            elif function == "create":  # Создание нового баланса
                self.clear(headline="Отчет о финансовых результатах")

                financial_report = FinancialReport()
                financial_report.create_report(self.global_frame)

        file_open_btn = Button(self.global_frame, text="Открыть\nфайл", width=12, height=3,
                               command=lambda: clear_and_proceed("open"))
        file_open_btn.grid(row=1, column=0, columnspan=6)

        continue_btn = Button(self.global_frame, text="Создать\nфайл", width=12, height=3,
                              command=lambda: clear_and_proceed("create"))
        continue_btn.grid(row=1, column=6, columnspan=6)

    def clear(self, headline="Приложение для решения задач\nпо бухгалтерскому учету"):
        # Удаление всех виджетов, кроме заголовка и кнопки "Меню"
        widget_list = self.global_frame.winfo_children()  # Список всех виджетов

        for num in range(len(widget_list)):
            # Виджет с индексом '0' - кнопка "Меню, а с индексом '1' - Заголовок
            if num == 1:
                widget_list[num].config(text=headline)
            elif num > 1:
                # Все остальные виджеты удаляются #
                widget_list[num].destroy()
