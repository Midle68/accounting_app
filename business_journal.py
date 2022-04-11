import pandas
from tkinter import *
from tkinter import messagebox, filedialog
import tkinter.ttk

FONT = ("Arial", 15, "normal")


class BusinessJournal:
    def __init__(self):
        self.data = pandas.read_csv("accounts_data.csv")
        self.rows = {}
        self.remains_rows = {}
        self.all_c4eta = []
        self.operations_num = 0

    def create_operations(self, global_frame, remains_rows, ops_number):  # Создание журнала хоз. операций

        def scrollbar_func1(event):  # Функция для работы скроллбара для журнала хозяйственных операций
            height = ops_number * 27 + 80
            if height > 310:
                height = 310
            canvas.configure(scrollregion=canvas.bbox("all"), width=790, height=height)

        def create_header():  # Создание Header для хозяйственных операций
            op_number_label = Label(two_frame, text="№")
            op_number_label.grid(row=1, column=0, columnspan=2)
            note_label = Label(two_frame, text="Запись")
            note_label.grid(row=1, column=2, columnspan=2)
            sum_label = Label(two_frame, text="Сумма")
            sum_label.grid(row=1, column=4, columnspan=2)
            debet_label = Label(two_frame, text="Дебет")
            debet_label.grid(row=1, column=6, columnspan=2)
            credit_label = Label(two_frame, text="Кредит")
            credit_label.grid(row=1, column=8, columnspan=2)

        def create_row(row_num):  # Создание одного ряда
            note_label = Label(two_frame, text=row_num - 1, font=FONT)
            note_label.grid(row=row_num, column=0, columnspan=2)

            note_entry = Entry(two_frame, width=30, font=FONT)
            note_entry.grid(row=row_num, column=2, columnspan=2)

            sum_entry = Entry(two_frame, width=12, font=FONT)
            sum_entry.grid(row=row_num, column=4, columnspan=2)

            debet_entry = Entry(two_frame, width=10, font=FONT)
            debet_entry.grid(row=row_num, column=6, columnspan=2)

            credit_entry = Entry(two_frame, width=10, font=FONT)
            credit_entry.grid(row=row_num, column=8, columnspan=2)

            search_btn = Button(two_frame, text="Search", width=5, command=lambda: search_data(row_num - 2))
            search_btn.grid(row=row_num, column=10, columnspan=2)

            # self.rows [ <Номер ряда> ] = [ <Каждый из элементов в строке> ]
            self.rows[row_num - 2] = [note_label, note_entry, sum_entry, debet_entry, credit_entry, search_btn]

        def search_data(row_num):  # Поиска проводки по хозяйственной операции из базы данных - var 'data' (accounts_data.csv)
            try:
                entry = self.rows[row_num][1].get().lower()
                debet_value = int(self.data[self.data["entry"] == entry]["debet"].item())
                credit_value = int(self.data[self.data["entry"] == entry]["credit"].item())

                # Удаление имеющихся и вставка найденных значений в "Дебет" и "Кредит"
                self.rows[row_num][3].delete(0, END)
                self.rows[row_num][4].delete(0, END)
                self.rows[row_num][3].insert(0, debet_value)
                self.rows[row_num][4].insert(0, credit_value)
            except ValueError:  # В случае если ничего не найдено, всплывает окно с ошибкой
                messagebox.showerror(title="Информация не найдена",
                                     message="Проводка для данной записи не была найдена")

        def create_buttons():  # Создание кнопок после журнала хоз. операций
            row_num = ops_number + 3  # Строка для размещения кнопок

            debet_find_entry = Entry(two_frame, width=5)
            debet_find_entry.grid(row=row_num, column=6)

            debet_find_btn = Button(two_frame, text="Поиск", width=5,
                                    command=lambda: search_debet(debet_find_entry))
            debet_find_btn.grid(row=row_num, column=7)

            credit_find_entry = Entry(two_frame, width=5)
            credit_find_entry.grid(row=row_num, column=8)

            credit_find_btn = Button(two_frame, text="Поиск", width=5,
                                     command=lambda: search_credit(credit_find_entry))
            credit_find_btn.grid(row=row_num, column=9)

            creating_accounts_btn = Button(two_frame, text="Построить счета", width=13,
                                           command=try_create_accounts)
            creating_accounts_btn.grid(row=row_num, column=4, columnspan=2)

            save_btn = Button(two_frame, text="Сохранить", pady=10, padx=10, command=try_save)
            save_btn.grid(row=row_num, column=12)

        def search_debet(debet_find_entry):  # Поиск введенного в таблице номера дебета + подчеркивание и выделение
            debet_value = debet_find_entry.get()
            for i in range(len(self.rows)):
                self.rows[i][3].config(font=("Arial", 15, "normal"))  # Шрифт "Дебета" - обычный
                if self.rows[i][3].get() == debet_value:
                    self.rows[i][3].config(font=("Arial", 15, "underline bold"), width=10)  # Подчеркивание "Дебета"

        def search_credit(credit_find_entry):  # Поиск введенного в таблице номера кредита + подчеркивание и выделение
            credit_value = credit_find_entry.get()
            for i in range(len(self.rows)):
                self.rows[i][4].config(font=("Arial", 15, "normal"))  # Шрифт "Кредита" - обычный
                if self.rows[i][4].get() == credit_value:
                    self.rows[i][4].config(font=("Arial", 15, "underline bold"), width=10)  # Подчеркивание "Кредита"

        def try_create_accounts():  # Создание счетов при правильных введенных данных
            try:
                for i in range(len(self.rows)):
                    int(self.rows[i][3].get())
                    int(self.rows[i][4].get())
                    int(self.rows[i][2].get())
            except ValueError:
                messagebox.showerror(title="Возникла ошибка",
                                     message="Проверьте правильность введенных данных. Ячейки 'Сумма', 'Дебет', "
                                             "'Кредит' должны быть заполнены и содержать числа.")
            else:
                self.compiling_accounts()

        def try_save():  # Сохранение данных
            file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=[("CSV File", ".csv")],
                                                     initialdir="/Users/midle/PycharmProjects/Сохраненные файлы "
                                                                "по бух. учету")
            try:
                data = {}  # Ввод в словарь всей необходимой информации для сохранения
                for i in range(len(self.rows)):
                    # data[<номер строки операции>] = [<хоз. операция>, <сумма>, <дебет>, <кредит>]
                    data[f"row_{i}"] = [self.rows[i][1].get(), self.rows[i][2].get(),
                                        self.rows[i][3].get(), self.rows[i][4].get()]

                for i in range(len(self.remains_rows)):
                    # data["номер строки остатка"] = [<номер счета>, <дебет/кредит>, <наименование>, <сумма>]
                    data[f"remain_row_{i}"] = [self.remains_rows[i][0].get(), self.remains_rows[i][1].get(),
                                               self.remains_rows[i][2].get(), self.remains_rows[i][3].get()]

                pandas.DataFrame(data).to_csv(file_path)
            except FileNotFoundError:  # Игнорирование ошибки, если пользователь закрывает окно
                pass

        messagebox.showinfo(message="Напоминание. Для построения счетов необходимо, чтобы 1) все ячейки были "
                                    "заполнены, 2) в разделах 'Сумма', 'Дебет' и 'Кредит' числа не должны содержать "
                                    "запятых, точек или пробелов.")

        one_frame = Frame(global_frame, width=790, height=400, bd=1, relief=GROOVE)
        one_frame.grid(row=1, column=0, columnspan=13, rowspan=ops_number)

        # Внедрение скроллбара с помощью двух Frame
        # Взято отсюда: https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
        canvas = Canvas(one_frame)
        two_frame = Frame(canvas)

        scrollbar = Scrollbar(one_frame, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left")
        canvas.create_window((0, 0), window=two_frame, anchor="nw")
        two_frame.bind("<Configure>", scrollbar_func1)

        create_header()

        for row in range(ops_number):
            create_row(row + 2)

        create_buttons()  # Создание кнопок после журнала хоз. операций

        if remains_rows != 0:  # Если количество строк-полей для остатков на счетах > 0, тогда создание остатков
            self.create_remains(global_frame, remains_rows)

    def create_remains(self, global_frame, remains_rows):  # Создание полей для ввода остатков на счетах

        def scrollbar_func2(event):  # Функция для работы скроллбара для остатков на счетах
            height = remains_rows * 27 + 30
            if height > 187:
                height = 187
            remains_canvas.configure(scrollregion=remains_canvas.bbox("all"), width=460, height=height)

        def create_remains_header(row_num):  # Создание Header для остатков на счетах
            account_label = Label(remains_two_frame, text="Счет")
            account_label.grid(row=row_num, column=0)
            debet_credit_label = Label(remains_two_frame, text="Дебет/Кредит")
            debet_credit_label.grid(row=row_num, column=1)
            operation_label = Label(remains_two_frame, text="Хозяйственная операция")
            operation_label.grid(row=row_num, column=2)
            sum_label = Label(remains_two_frame, text="Сумма")
            sum_label.grid(row=row_num, column=3)

        def create_remain_row(row_num, number):  # Создание одной строки полей для остатков на счетах
            account_entry = Entry(remains_two_frame, width=7)
            account_entry.grid(row=row_num, column=0)

            debet_credit_entry = Entry(remains_two_frame, width=10)
            debet_credit_entry.grid(row=row_num, column=1)

            operation_entry = Entry(remains_two_frame)
            operation_entry.grid(row=row_num, column=2)

            sum_entry = Entry(remains_two_frame, width=8)
            sum_entry.grid(row=row_num, column=3)

            # self.remains_rows[<Номер строки>] = [<Номер счета>, <Дебет/Кредит> <Хозяйственная операция>, <Сумма>]
            self.remains_rows[number] = [account_entry, debet_credit_entry, operation_entry, sum_entry]

        remains_label = Label(global_frame, text="Остатки на счетах", pady=15, font=("Arial", 20, "normal"))
        remains_label.grid(row=len(self.rows) + 2, column=0, columnspan=5)

        # Размещение всех остатков в Frame #
        remains_frame = Frame(global_frame, bd=1, relief=GROOVE)
        remains_frame.grid(row=len(self.rows) + 3, column=0, columnspan=5)

        # Внедрение скроллбара с помощью двух Frame
        # Взято отсюда: https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
        remains_canvas = Canvas(remains_frame)
        remains_two_frame = Frame(remains_canvas)

        scrollbar2 = Scrollbar(remains_frame, orient=VERTICAL, command=remains_canvas.yview)
        remains_canvas.configure(yscrollcommand=scrollbar2.set)

        scrollbar2.pack(side="right", fill="y")
        remains_canvas.pack(side="left")
        remains_canvas.create_window((0, 0), window=remains_two_frame, anchor="nw")
        remains_two_frame.bind("<Configure>", scrollbar_func2)

        row = len(self.rows) + 3
        create_remains_header(row)

        for num in range(remains_rows):  # Создание строк-полей для остатков на счетах
            row = len(self.rows) + 4 + num
            create_remain_row(row, num)

    def compiling_accounts(self):  # Построение счетов в отдельном окне
        remains = {}

        # Добавление остатков в словарь 'remains', если они имеются
        if len(self.remains_rows):
            for i in self.remains_rows:
                try:  # Проверка правильности введенных данных
                    account = int(self.remains_rows[i][0].get())
                    debet_credit_sum = int(self.remains_rows[i][3].get())
                except ValueError:
                    messagebox.showerror(title="Возникла ошибка",
                                         message="Проверьте правильность введенных данных в остатках на счетах")
                    break
                else:
                    # Проверка правильности введенных данных по 'Дебет/Кредит' и их ввод в словарь
                    debet_credit = self.remains_rows[i][1].get().capitalize()
                    if debet_credit == "Кредит" or debet_credit == "Дебет":
                        remains[account] = {"debet_credit": debet_credit, "sum": debet_credit_sum}
                    else:
                        messagebox.showerror(title="Возникла ошибка",
                                             message="Проверьте правильность введенных данных в остатках на счетах")
                        break

        if len(self.remains_rows) == len(remains):
            # Сбор всех необходимых счетов в отсортированный список
            all_accounts = []
            for i in range(len(self.rows)):
                all_accounts.append(int(self.rows[i][3].get()))
                all_accounts.append(int(self.rows[i][4].get()))

            for i in remains.keys():
                all_accounts.append(i)
            all_accounts = sorted(list(set(all_accounts)))

            # В отдельных списках по дебету и кредиту вводится номер операции, проводка и сумма
            debet_values = []
            credit_values = []
            for i in range(len(self.rows)):
                debet_values.append(
                    {
                        "note": i,
                        "account": int(self.rows[i][3].get()),
                        "sum": int(self.rows[i][2].get())
                    }
                )
                credit_values.append(
                    {
                        "note": i,
                        "account": int(self.rows[i][4].get()),
                        "sum": int(self.rows[i][2].get())
                    }
                )

            # Добавление каждого счета в self.all_c4eta со всеми данными
            for account_num in all_accounts:
                dt_values = []
                ct_values = []
                remain = {}

                # Поиск совпадения номера счета в списке счетов по дебету
                for value in debet_values:
                    if account_num == value["account"]:
                        dt_values.append({"op_number": value["note"], "sum": value["sum"]})

                # Поиск совпадения номера счета в списке счетов по кредиту
                for value in credit_values:
                    if account_num == value["account"]:
                        ct_values.append({"op_number": value["note"], "sum": value["sum"]})

                # Изменение словаря remain, если есть остатки по номеру счету
                if account_num in remains:
                    remain = remains[account_num]

                self.all_c4eta.append(
                    {
                        "account_number": account_num,
                        "remain": remain,
                        "debet_values": dt_values,
                        "credit_values": ct_values,
                    }
                )

            # Построение счетов бухгалтерского учета
            self.create_accounts(column=0, row=0)

    def open_file(self, root, data):  # Извлечение и ввод данных из файла в журнал хоз. операций
        columns = data.columns.values.tolist()
        rows_number = 1
        remains_number = 0

        for i in range(len(columns)):  # Подсчет количества хоз. операций и остатков на счетах
            if i:  # Колонна с индексом "0" - Unnamed. Следовательно, ее пропускаем
                if columns[i] == f"row_{i - 1}":
                    rows_number = i
                else:
                    remains_number = i - rows_number

        # Создание журнала хоз. операций, учитывая кол-во операций и остатков
        self.create_operations(root, remains_number, rows_number)

        # Извлечение данных по дебету и кредиту из файла и введение их в таблицу
        rows_data = []
        for i in range(rows_number + 1):
            if i:
                column_data = data.iloc[:, i]  # Данные о колонне с индексом 'i'
                rows_data.append(column_data)

        for i in range(len(rows_data)):
            note_string = rows_data[i][0]
            if str(note_string) == "nan":  # Если наименование отсутствует ('nan'), то она становится пустой
                note_string = ""
            try:
                op_sum = int(rows_data[i][1])
            except:
                op_sum = rows_data[i][1]
                if str(op_sum) == "nan":
                    op_sum = ""

            try:
                debet = int(rows_data[i][2])
            except:
                debet = rows_data[i][2]
                if str(debet) == "nan":
                    debet = ""

            try:
                credit = int(rows_data[i][3])
            except:
                credit = rows_data[i][3]
                if str(credit) == "nan":
                    credit = ""

            # Ввод данных по строкам хозяйственных операций в таблицу
            self.rows[i][1].insert(1, note_string)
            self.rows[i][2].insert(1, op_sum)
            self.rows[i][3].insert(1, debet)
            self.rows[i][4].insert(1, credit)

        # Извлечение данных по остаткам на счетах и введение их в таблицу
        remains_data = []
        for i in range(remains_number):
            # Извлечение данных в колоннах, идущих после колонн с данными о хоз. операциях
            remains_column = data.iloc[:, rows_number + i + 1]
            remains_data.append(remains_column)

        for i in range(len(remains_data)):

            try:
                account_num = int(remains_data[i][0])
            except:
                account_num = remains_data[i][0]
                if str(account_num) == "nan":
                    account_num = ""

            try:
                debet_credit = int(remains_data[i][1])
            except:
                debet_credit = remains_data[i][1]
                if str(debet_credit) == "nan":
                    debet_credit = ""

            note_string = remains_data[i][2]
            if str(note_string) == "nan":  # Если наименование отсутствует ("nan"), то он становится пустым
                note_string = ""

            try:
                remain_sum = int(remains_data[i][3])
            except:
                remain_sum = remains_data[i][3]
                if str(remain_sum) == "nan":
                    remain_sum = ""

            # Ввод всех данных по строке остатков на счетах в таблицу
            self.remains_rows[i][0].insert(1, account_num)
            self.remains_rows[i][1].insert(1, debet_credit)
            self.remains_rows[i][2].insert(1, note_string)
            self.remains_rows[i][3].insert(1, remain_sum)

    def create_accounts(self, column: int, row: int):  # Открытие и отображение счетов бухгалтерского учета
        root = Tk()
        root.title("Счета бухгалтерского учета")
        root.config(pady=20, padx=20)

        def scrollbar_func(event):  # Функция для обеспечение работы скроллбара
            canvas.configure(scrollregion=canvas.bbox("all"), width=1200, height=700)

        starting_column = column
        starting_row = row
        addition = 0
        max_rows = 0

        one_frame = Frame(root, width=1200, height=700, bd=1, relief=GROOVE)
        one_frame.grid(row=0, column=0)

        # Внедрение скроллбара с помощью двух Frame
        # Взято отсюда: https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
        canvas = Canvas(one_frame)
        two_frame = Frame(canvas)
        scrollbar = Scrollbar(one_frame, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left")
        canvas.create_window((0, 0), window=two_frame, anchor="nw")
        two_frame.bind("<Configure>", scrollbar_func)

        # Выведение каждого счета в GUI
        for i in range(len(self.all_c4eta)):
            remain_len = 0

            # Для правильного подсчета кол-ва строк счета: если есть остаток - remain_len = 2, иначе - remain_len = 0
            if self.all_c4eta[i]["remain"] != {}:
                remain_len = 2

            # Определение количества строк счета
            if len(self.all_c4eta[i]["debet_values"]) + remain_len > len(self.all_c4eta[i]["credit_values"]) + remain_len:
                rows = len(self.all_c4eta[i]["debet_values"]) + remain_len
            else:
                rows = len(self.all_c4eta[i]["credit_values"]) + remain_len

            # Выявление максимального кол-ва строк в ряду для правильного отображения следующего ряда
            if rows + 6 + remain_len > max_rows:
                max_rows = rows + 6 + remain_len

            first_frame = Frame(two_frame, pady=10, padx=10)
            first_frame.grid(row=starting_row, column=starting_column, columnspan=3,
                             rowspan=rows + 6 + remain_len)

            debet_label = Label(first_frame, text="Дебет", width=8)
            debet_label.grid(row=starting_row, column=starting_column)

            account_name = Label(first_frame, text=self.all_c4eta[i]["account_number"], width=4)
            account_name.grid(row=starting_row, column=starting_column + 1)

            credit_label = Label(first_frame, text="Кредит", width=8)
            credit_label.grid(row=starting_row, column=starting_column + 2)

            starting_row += 1

            # Горизонтальная линия после строки: "Дебет <Номер счета> Кредит"
            hr_line = tkinter.ttk.Separator(first_frame, orient=HORIZONTAL)
            hr_line.grid(row=starting_row, column=starting_column, columnspan=3, sticky="ew")
            starting_row += 1

            # Второй Frame для ввода всех операций по счету и сальдо
            second_frame = Frame(first_frame)
            second_frame.grid(row=starting_row, column=starting_column, columnspan=3)

            # Вертикальная линия вдоль всех записей, а также ячейки с суммами дебета и кредита
            vert_rows = rows + 6 + remain_len
            ver_line = tkinter.ttk.Separator(second_frame, orient=VERTICAL)
            ver_line.grid(row=starting_row, column=starting_column + 1, rowspan=vert_rows, sticky="ns")
            starting_row += 1

            # Раздельное построение дебета и кредита и раздельное определение числа их строк
            remain_sum = 0

            debet_row = 0
            # Если остаток по счету есть и он в дебете - отображение остатка в GUI
            if remain_len != 0 and self.all_c4eta[i]["remain"]["debet_credit"] == "Дебет":
                remain_sum = self.all_c4eta[i]["remain"]["sum"]  # Сумма остатка
                debet_remain = Label(second_frame, text=remain_sum)
                debet_remain.grid(row=starting_row, column=starting_column)
                debet_row += 1

                # Если строка с остатками последняя, то горизонтальная линия после нее не показывается #
                if len(self.all_c4eta[i]["credit_values"]) > 1 or len(self.all_c4eta[i]["debet_values"]) != 0:
                    remain_debet_hr_line = tkinter.ttk.Separator(second_frame, orient=HORIZONTAL)
                    remain_debet_hr_line.grid(row=starting_row + debet_row,
                                              column=starting_column, sticky="ew")
                    debet_row += 1

            for num in range(len(self.all_c4eta[i]["debet_values"])):  # Отображение каждой строки дебета
                # Если в кредите есть остаток, вторая строка в дебете будет через строку, т. к. линия занимает строку
                if num == 1 and remain_len == 2 and self.all_c4eta[i]["remain"]["debet_credit"] == "Кредит":
                    debet_row += 1

                debet_one = Label(second_frame,
                                  text=f'{self.all_c4eta[i]["debet_values"][num]["op_number"] + 1}) '
                                       f'{self.all_c4eta[i]["debet_values"][num]["sum"]}')
                debet_one.grid(row=starting_row + debet_row, column=starting_column)
                debet_row += 1

            credit_row = 0
            # Если остаток по счету есть и он в кредите - отображение остатка в GUI
            if remain_len != 0 and self.all_c4eta[i]["remain"]["debet_credit"] == "Кредит":
                remain_sum = self.all_c4eta[i]["remain"]["sum"]  # Сумма остатка
                credit_remain = Label(second_frame, text=remain_sum)
                credit_remain.grid(row=starting_row, column=starting_column + 2)
                credit_row += 1

                # Если строка с остатками последняя, то горизонтальная линия после нее не показывается
                if len(self.all_c4eta[i]["debet_values"]) > 1 or len(self.all_c4eta[i]["credit_values"]) != 0:
                    remain_credit_hr_line = tkinter.ttk.Separator(second_frame, orient=HORIZONTAL)
                    remain_credit_hr_line.grid(row=starting_row + credit_row,
                                               column=starting_column + 2, sticky="ew")
                    credit_row += 1

            for num in range(len(self.all_c4eta[i]["credit_values"])):  # Отображение каждой строки кредита
                # Если в дебете есть остаток, вторая строка в кредите будет через строку, т. к. линия занимает строку
                if num == 1 and remain_len == 2 and self.all_c4eta[i]["remain"]["debet_credit"] == "Дебет":
                    credit_row += 1

                credit_one = Label(second_frame, text=f'{self.all_c4eta[i]["credit_values"][num]["op_number"] + 1}) '
                                                      f'{self.all_c4eta[i]["credit_values"][num]["sum"]}')
                credit_one.grid(row=starting_row + credit_row, column=starting_column + 2)
                credit_row += 1

            # Добавление к общему кол-ву строк число строк дебета или кредита, смотря чего больше
            if debet_row > credit_row:
                starting_row += debet_row
            else:
                starting_row += credit_row

            # Горизонтальная линия для разделения записей и сумм кредита и дебета #
            balance_line = tkinter.ttk.Separator(second_frame, orient=HORIZONTAL)
            balance_line.grid(row=starting_row, column=starting_column, columnspan=3, sticky="ew")
            starting_row += 1

            # Раздельный подсчет сумм дебета и кредита и замена нулевой суммы на "-"
            debet_sum = 0
            for num in range(len(self.all_c4eta[i]["debet_values"])):
                debet_sum += self.all_c4eta[i]["debet_values"][num]["sum"]
            balance_debet = Label(second_frame, text=debet_sum, width=10)

            if debet_sum:
                balance_debet.config(text="-")
            balance_debet.grid(row=starting_row, column=starting_column)

            credit_sum = 0
            for num in range(len(self.all_c4eta[i]["credit_values"])):
                credit_sum += self.all_c4eta[i]["credit_values"][num]["sum"]
            balance_credit = Label(second_frame, text=credit_sum, width=10)

            if credit_sum:
                balance_credit.config(text="-")
            balance_credit.grid(row=starting_row, column=starting_column + 2)

            starting_row += 1

            # Горизонтальная линия для разграничения сальдо и сумм дебета и кредита
            last_line = tkinter.ttk.Separator(second_frame, orient=HORIZONTAL)
            last_line.grid(row=starting_row, column=starting_column, columnspan=3, sticky="ew")
            starting_row += 1

            # Вычисление значения окончательного сальдо
            if remain_len:
                if self.all_c4eta[i]["remain"]["debet_credit"] == "Дебет":
                    debet_sum += remain_sum
                elif self.all_c4eta[i]["remain"]["debet_credit"] == "Кредит":
                    credit_sum += remain_sum

            difference = debet_sum - credit_sum
            column = starting_column

            # Если сальдо > 0, то - оно в дебете (column=0), иначе - в кредите (column=2) и избавляемся от минуса
            if difference < 0:
                column = starting_column + 2
                difference *= -1

            balance = Label(second_frame, text=difference)
            balance.grid(row=starting_row, column=column)

            # Для размещение следующего счета - добавляем к первоначальной колонне 3
            starting_column += 3

            # После 5 счетов в одном ряду, следующие счета - вниз на ряд, а "addition" += макс. кол-во строк в ряду + 1
            i += 1
            if i != 0 and i % 5 == 0:
                addition += max_rows + 1
                starting_column = 0
            starting_row = row + addition

        # Стирание данных по всем счетам для правильного отображения данных в следующий раз
        self.all_c4eta = []

        root.mainloop()
