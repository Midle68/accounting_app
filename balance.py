import json
from tkinter import *
from tkinter import ttk, messagebox, filedialog
HEAD_FONT = ("Arial", 13, "normal")
CHAPTER_FONT = ("Arial", 13, "bold")
COMMON_FONT = ("Arial", 12, "normal")
BOLD_COMMON_FONT = ("Arial", 12, "bold")


def enable_disable(property_obj):
    def change_state(function):
        property_obj.config(state=NORMAL)
        function()
        property_obj.config(state=DISABLED)
    return change_state


class Balance:
    def __init__(self):
        self.balance_entries = []
        self.balance_number = 0
        self.properties = {}
        self.entries_row = 0
        self.row = 0
        self.starting_column = 0
        self.property_row = 1

    def create_balance(self, global_frame, property_rows):  # Создание баланса

        def scrollbar_func1(event):  # Функция для работы Scrollbar баланса
            canvas.configure(scrollregion=canvas.bbox("all"), width=1250, height=750)

        def create_property_composition():  # Создание полей для данных по имуществу

            def property_scrollbar_func(event):
                height = property_rows * 27 + 55
                if height > 300:
                    height = 300
                property_canvas.configure(scrollregion=property_canvas.bbox("all"), width=680, height=height)

            # Внедрение скроллбара с помощью двух Frame
            # Взято отсюда: https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
            pre_property_frame = Frame(first_frame)
            pre_property_frame.grid(row=self.property_row, column=self.starting_column, pady=15)

            property_canvas = Canvas(pre_property_frame)
            property_frame = Frame(property_canvas)
            property_scrollbar = Scrollbar(pre_property_frame, orient=VERTICAL, command=property_canvas.yview)
            property_canvas.configure(yscrollcommand=property_scrollbar.set)

            property_scrollbar.pack(side="right", fill="y")
            property_canvas.pack(side="left")
            property_canvas.create_window((0, 0), window=property_frame, anchor="nw")
            property_frame.bind("<Configure>", property_scrollbar_func)

            # Создание Header для данных по имуществу
            create_property_header(property_frame)
            self.property_row += 1

            for i in range(property_rows):  # По введенному кол-ву - создание полей для данных об имуществе
                row_num = Label(property_frame, text=i + 1, width=5)
                row_num.grid(row=self.property_row, column=self.starting_column)

                property_name = Entry(property_frame, width=30)
                property_name.grid(row=self.property_row, column=self.starting_column + 1)

                property_sum = Entry(property_frame, width=7)
                property_sum.grid(row=self.property_row, column=self.starting_column + 2)

                active_passive_number = Entry(property_frame, width=13)
                active_passive_number.grid(row=self.property_row, column=self.starting_column + 3)

                start_end = Entry(property_frame, width=13)
                start_end.grid(row=self.property_row, column=self.starting_column + 4)

                # self.properties[<Номер ряда>] = [<Номер ряда>, <наименование>, <сумма>, <актив/пассив>]
                self.properties[self.property_row - 1] = [row_num, property_name, property_sum,
                                                          active_passive_number, start_end]

                self.property_row += 1

            transfer_properties = Button(property_frame, text="Перенос", width=13, command=self.transfer_properties)
            transfer_properties.grid(row=self.property_row, column=self.starting_column + 4)
            self.property_row += 1

        def create_property_header(property_frame):  # Создание Header для данных по имуществу
            row_number = Label(property_frame, text="№")
            row_number.grid(row=self.property_row, column=self.starting_column)

            property_type = Label(property_frame, text="Виды имущества, обязательств и капитала")
            property_type.grid(row=self.property_row, column=self.starting_column + 1)

            property_sum = Label(property_frame, text="Сумма")
            property_sum.grid(row=self.property_row, column=self.starting_column + 2)

            active_passive = Label(property_frame, text="№ Актива / Пассива")
            active_passive.grid(row=self.property_row, column=self.starting_column + 3)

            start_end = Label(property_frame, text="Начало / Конец")
            start_end.grid(row=self.property_row, column=self.starting_column + 4)

        def create_balance_header():  # Создание Header для баланса
            indicator_name = Label(balance_frame, text="Наименование показателя", font=HEAD_FONT)
            indicator_name.grid(row=self.row, column=self.starting_column, columnspan=2, sticky="s")

            start_sum_label = Label(balance_frame, text="Сумма\nна начало периода", font=HEAD_FONT)
            start_sum_label.grid(row=self.row, column=self.starting_column + 2)

            end_sum_label = Label(balance_frame, text="Сумма\nна конец периода", font=HEAD_FONT)
            end_sum_label.grid(row=self.row, column=self.starting_column + 3)

            self.row += 1

        def create_balance_rows():  # Создание строк баланса
            fixed_assets_label = Label(balance_frame, text="АКТИВ\nI. ВНЕОБОРОТНЫЕ АКТИВЫ", font=CHAPTER_FONT)
            fixed_assets_label.grid(row=self.row, column=0, columnspan=2, sticky="ns")  # pady = 10
            self.row += 1

            intangible_assets = Label(balance_frame, text="Нематериальные активы", font=COMMON_FONT)
            add_entry_grid(intangible_assets, 0)
            add_entries()

            researches_results = Label(balance_frame, text="Результаты исследований и разработок", font=COMMON_FONT)
            add_entry_grid(researches_results, 1)
            add_entries()

            core_funds = Label(balance_frame, text="Основные средства", font=COMMON_FONT)
            add_entry_grid(core_funds, 2)
            add_entries()

            profitable_investments = Label(balance_frame, text="Доходные вложения в материальные ценности",
                                           font=COMMON_FONT)
            add_entry_grid(profitable_investments, 3)
            add_entries()

            financial_investments = Label(balance_frame, text="Финансовые вложения", font=COMMON_FONT)
            add_entry_grid(financial_investments, 4)
            add_entries()

            delayed_tax_benefits = Label(balance_frame, text="Отложенные налоговые активы", font=COMMON_FONT)
            add_entry_grid(delayed_tax_benefits, 5)
            add_entries()

            other_fixed_assets = Label(balance_frame, text="Прочие внеоборотные активы", font=COMMON_FONT)
            add_entry_grid(other_fixed_assets, 6)
            add_entries()

            first_chapter_result = Label(balance_frame, text="Итого по разделу I", font=BOLD_COMMON_FONT)
            first_chapter_result.grid(row=self.row, column=0, sticky="w")
            first_chapter_btn = Button(balance_frame, text="Посчитать",
                                       command=lambda: self.calculate_chapter_result("Итого по разделу I"))
            first_chapter_btn.grid(row=self.row, column=1)
            add_result_entries()

            current_assets = Label(balance_frame, text="II. ОБОРОТНЫЕ АКТИВЫ", font=CHAPTER_FONT)
            current_assets.grid(row=self.row, column=0, columnspan=2, sticky="ns")
            self.row += 1

            stock = Label(balance_frame, text="Запасы", font=COMMON_FONT)
            add_entry_grid(stock, 8)
            add_entries()

            vat_acquired_values = Label(balance_frame, text="НДС по приобретенным ценностям", font=COMMON_FONT)
            add_entry_grid(vat_acquired_values, 9)
            add_entries()

            receivables = Label(balance_frame, text="Дебиторская задолженность", font=COMMON_FONT)
            add_entry_grid(receivables, 10)
            add_entries()

            current_financial_investments = Label(balance_frame, text="Финансовые вложения (без ден. эквивалентов)",
                                                  font=COMMON_FONT)
            add_entry_grid(current_financial_investments, 11)
            add_entries()

            cash_and_equivalents = Label(balance_frame, text="Денежные средства и денежные эквиваленты",
                                         font=COMMON_FONT)
            add_entry_grid(cash_and_equivalents, 12)
            add_entries()

            other_current_assets = Label(balance_frame, text="Прочие оборотные активы", font=COMMON_FONT)
            add_entry_grid(other_current_assets, 13)
            add_entries()

            second_chapter_result = Label(balance_frame, text="Итого по разделу II", font=BOLD_COMMON_FONT)
            second_chapter_result.grid(row=self.row, column=0, sticky="w")
            second_chapter_btn = Button(balance_frame, text="Посчитать",
                                        command=lambda: self.calculate_chapter_result("Итого по разделу II"))
            second_chapter_btn.grid(row=self.row, column=1)
            add_result_entries()

            self.row = 1
            self.starting_column = 5
            create_balance_header()

            capital_reserves = Label(balance_frame, text="ПАССИВ\nIII. КАПИТАЛ И РЕЗЕРВЫ", font=CHAPTER_FONT)
            capital_reserves.grid(row=self.row, column=self.starting_column, columnspan=2, sticky="ns")
            self.row += 1

            authorized_capital = Label(balance_frame, text="Уставный капитал", font=COMMON_FONT)
            add_entry_grid(authorized_capital, 15)
            add_entries()

            own_shares = Label(balance_frame, text="Собственные акции", font=COMMON_FONT)
            add_entry_grid(own_shares, 16)
            add_entries()

            revaluation_current_assets = Label(balance_frame, text="Переоценка внеоборотных активов",
                                               font=COMMON_FONT)
            add_entry_grid(revaluation_current_assets, 17)
            add_entries()

            additional_capital = Label(balance_frame, text="Добавочный капитал", font=COMMON_FONT)
            add_entry_grid(additional_capital, 18)
            add_entries()

            reserved_capital = Label(balance_frame, text="Резервный капитал", font=COMMON_FONT)
            add_entry_grid(reserved_capital, 19)
            add_entries()

            retained_profit = Label(balance_frame, text="Нераспределенная прибыль", font=COMMON_FONT)
            add_entry_grid(retained_profit, 20)
            add_entries()

            third_chapter_result = Label(balance_frame, text="Итого по разделу III", font=CHAPTER_FONT)
            third_chapter_result.grid(row=self.row, column=self.starting_column, sticky="w")
            third_chapter_btn = Button(balance_frame, text="Посчитать",
                                       command=lambda: self.calculate_chapter_result("Итого по разделу III"))
            third_chapter_btn.grid(row=self.row, column=self.starting_column + 1)
            add_result_entries()

            long_term_liabilities = Label(balance_frame, text="IV. ДОЛГОСРОЧНЫЕ ОБЯЗАТЕЛЬСТВА", font=CHAPTER_FONT)
            long_term_liabilities.grid(row=self.row, column=self.starting_column, columnspan=2, sticky="ns")
            self.row += 1

            long_term_borrowed_funds = Label(balance_frame, text="Заемные средства", font=COMMON_FONT)
            add_entry_grid(long_term_borrowed_funds, 22)
            add_entries()

            delayed_tax_liabilities = Label(balance_frame, text="Отложенные налоговые обязательства",
                                            font=COMMON_FONT)
            add_entry_grid(delayed_tax_liabilities, 23)
            add_entries()

            long_term_estimated_liabilities = Label(balance_frame, text="Оценочные обязательства", font=COMMON_FONT)
            add_entry_grid(long_term_estimated_liabilities, 24)
            add_entries()

            other_long_term_liabilities = Label(balance_frame, text="Прочие обязательства", font=COMMON_FONT)
            add_entry_grid(other_long_term_liabilities, 25)
            add_entries()

            fourth_chapter_result = Label(balance_frame, text="Итого по разделу IV", font=CHAPTER_FONT)
            fourth_chapter_result.grid(row=self.row, column=self.starting_column, sticky="w")
            fourth_chapter_btn = Button(balance_frame, text="Посчитать",
                                        command=lambda: self.calculate_chapter_result("Итого по разделу IV"))
            fourth_chapter_btn.grid(row=self.row, column=self.starting_column + 1)
            add_result_entries()

            short_term_liabilities = Label(balance_frame, text="V. КРАТКОСРОЧНЫЕ ОБЯЗАТЕЛЬСТВА", font=CHAPTER_FONT)
            short_term_liabilities.grid(row=self.row, column=self.starting_column, columnspan=2, sticky="ns")
            self.row += 1

            short_term_borrowed_funds = Label(balance_frame, text="Заемные средства", font=COMMON_FONT)
            add_entry_grid(short_term_borrowed_funds, 27)
            add_entries()

            accounts_payable = Label(balance_frame, text="Кредиторская задолженность", font=COMMON_FONT)
            add_entry_grid(accounts_payable, 28)
            add_entries()

            future_earnings = Label(balance_frame, text="Доходы будущих периодов", font=COMMON_FONT)
            add_entry_grid(future_earnings, 29)
            add_entries()

            short_term_estimated_liabilities = Label(balance_frame, text="Оценочные обязательства", font=COMMON_FONT)
            add_entry_grid(short_term_estimated_liabilities, 30)
            add_entries()

            other_short_term_liabilities = Label(balance_frame, text="Прочие обязательства", font=COMMON_FONT)
            add_entry_grid(other_short_term_liabilities, 31)
            add_entries()

            fifth_chapter_result = Label(balance_frame, text="Итого по разделу V", font=CHAPTER_FONT)
            fifth_chapter_result.grid(row=self.row, column=self.starting_column, sticky="w")
            fifth_chapter_btn = Button(balance_frame, text="Посчитать",
                                       command=lambda: self.calculate_chapter_result("Итого по разделу V"))
            fifth_chapter_btn.grid(row=self.row, column=self.starting_column + 1)
            add_result_entries()
            self.row += 1

            self.starting_column = 0

            result_line = ttk.Separator(balance_frame, orient=HORIZONTAL)
            result_line.grid(row=self.row, column=self.starting_column, columnspan=9, sticky="ew", pady=10)
            self.row += 1

            assets_result = Label(balance_frame, text="Итого по Активу", font=CHAPTER_FONT)
            assets_result.grid(row=self.row, column=self.starting_column, sticky="w")
            assets_result_btn = Button(balance_frame, text="Посчитать",
                                       command=lambda: self.calculate_end_result(active_or_passive="Active"))
            assets_result_btn.grid(row=self.row, column=self.starting_column + 1)
            add_result_entries()

            self.starting_column = 5
            self.row -= 1

            passive_results = Label(balance_frame, text="Итого по Пассиву", font=CHAPTER_FONT, pady=10)
            passive_results.grid(row=self.row, column=self.starting_column, sticky="w")
            passive_results_btn = Button(balance_frame, text="Посчитать",
                                         command=lambda: self.calculate_end_result(active_or_passive="Passive"))
            passive_results_btn.grid(row=self.row, column=self.starting_column + 1)
            add_result_entries()

            save_btn = Button(balance_frame, text="Сохранить", width=12, height=3, command=self.save)
            save_btn.grid(row=self.row, column=self.starting_column + 3)

        def add_entries():
            start_sum_entry = Entry(balance_frame, width=15, font=COMMON_FONT)
            start_sum_entry.grid(row=self.row, column=self.starting_column + 2, padx=10)

            end_sum_entry = Entry(balance_frame, width=15, font=COMMON_FONT)
            end_sum_entry.grid(row=self.row, column=self.starting_column + 3)

            # self.balance_entries.append(
            #     {
            #         row_text: [self.balance_number, start_sum_entry, end_sum_entry]
            #     }
            # )

            self.balance_entries.append([self.balance_number, start_sum_entry, end_sum_entry])

            self.row += 1
            self.entries_row += 1
            self.balance_number += 1

        def add_result_entries():  # Поля c итогами раздела находятся в состоянии 'disabled'
            start_sum_entry = Entry(balance_frame, width=15, font=COMMON_FONT, state=DISABLED)
            start_sum_entry.grid(row=self.row, column=self.starting_column + 2, padx=5)

            end_sum_entry = Entry(balance_frame, width=15, font=COMMON_FONT, state=DISABLED)
            end_sum_entry.grid(row=self.row, column=self.starting_column + 3, padx=10)

            self.balance_entries.append([self.balance_number, start_sum_entry, end_sum_entry])

            self.row += 1
            self.entries_row += 1
            self.balance_number += 1

        def add_entry_grid(entry, number):  # Введение всех значений параметра "grid" для виджета с данными об имуществе
            entry.grid(row=self.row, column=self.starting_column, sticky="w")

            property_num_label = Label(balance_frame, text=number, font=COMMON_FONT)
            property_num_label.grid(row=self.row, column=self.starting_column + 1, sticky="e")

        # Внедрение скроллбара с помощью двух Frame #
        # Взято отсюда: https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame #
        one_frame = Frame(global_frame, width=790, height=400, bd=1, relief=GROOVE)
        one_frame.grid(row=1, column=0, columnspan=14)

        canvas = Canvas(one_frame)
        first_frame = Frame(canvas)

        scrollbar = Scrollbar(one_frame, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left")
        canvas.create_window((0, 0), window=first_frame, anchor="nw")
        first_frame.bind("<Configure>", scrollbar_func1)

        if property_rows:  # Отображение данных по имуществу, если они есть
            create_property_composition()

        # Создание Frame со всеми полями #
        balance_frame = Frame(first_frame)
        balance_frame.grid(row=self.property_row, column=0, columnspan=9, padx=15, pady=5)

        vertical_line = ttk.Separator(balance_frame, orient=VERTICAL)
        vertical_line.grid(row=self.row, column=4, rowspan=23, sticky="ns", padx=15)

        self.row += 1

        create_balance_header()

        create_balance_rows()

    def calculate_chapter_result(self, row_text):  # Подсчет суммы по разделу
        # Установление диапазона строк для подсчета суммы по разделу
        if row_text == "Итого по разделу I":
            start_range = 0
            end_range = 7
        elif row_text == "Итого по разделу II":
            start_range = 8
            end_range = 14
        elif row_text == "Итого по разделу III":
            start_range = 15
            end_range = 21
        elif row_text == "Итого по разделу IV":
            start_range = 22
            end_range = 26
        else:
            start_range = 27
            end_range = 32

        chapter_start_entry = list(self.balance_entries[end_range])[1]
        chapter_end_entry = list(self.balance_entries[end_range])[2]
        chapter_start_sum = 0
        chapter_end_sum = 0

        for i in range(start_range, end_range):  # Получение данных из строк баланса на начало и конец
            property_row = list(self.balance_entries[i])
            try:
                property_start_value = int(property_row[1].get())
                chapter_start_sum += property_start_value
            except ValueError:
                pass

            try:
                property_end_value = int(property_row[2].get())
                chapter_end_sum += property_end_value
            except ValueError:
                pass

        # Изменение состояния виджета Entry итога по разделу и введение суммы
        @enable_disable(chapter_start_entry)
        def change_start_sum():
            chapter_start_entry.delete(0, END)
            chapter_start_entry.insert(0, chapter_start_sum)

        @enable_disable(chapter_end_entry)
        def change_end_sum():
            chapter_end_entry.delete(0, END)
            chapter_end_entry.insert(0, chapter_end_sum)

    def calculate_end_result(self, active_or_passive: str):  # Подсчеты итоговой суммы по активу / пассиву
        chapters = {}
        try:
            if active_or_passive == "Active":  # Если подсчет по активу, то в расчет - итоги I и II на начало и конец
                first_chapter_start = int(list(self.balance_entries[7])[1].get())
                first_chapter_end = int(list(self.balance_entries[7])[2].get())

                second_chapter_start = int(list(self.balance_entries[14])[1].get())
                second_chapter_end = int(list(self.balance_entries[14])[2].get())
                chapters["start"] = [first_chapter_start, second_chapter_start]
                chapters["end"] = [first_chapter_end, second_chapter_end]
            else:  # Если подсчет по пассиву, то в расчет - итоги II, III & IV на начало и конец
                third_chapter_start = int(list(self.balance_entries[21])[1].get())
                third_chapter_end = int(list(self.balance_entries[21])[2].get())

                fourth_chapter_start = int(list(self.balance_entries[26])[1].get())
                fourth_chapter_end = int(list(self.balance_entries[26])[2].get())

                fifth_chapter_start = int(list(self.balance_entries[32])[1].get())
                fifth_chapter_end = int(list(self.balance_entries[32])[2].get())
                chapters["start"] = [third_chapter_start, fourth_chapter_start, fifth_chapter_start]
                chapters["end"] = [third_chapter_end, fourth_chapter_end, fifth_chapter_end]
        except ValueError:
            messagebox.showerror(title="Возникла ошибка",
                                 message="Проверьте правильность введенных данных. "
                                         "Вероятно ячейки с итогами по разделам пусты.")
        else:
            # Вычисляем итоговую сумму по итогам разделом на начало периода
            result_sum_start = 0
            for i in chapters["start"]:
                result_sum_start += i

            # Вычисляем итоговую сумму по итогам разделом на конец периода
            result_sum_end = 0
            for i in chapters["end"]:
                result_sum_end += i

            # Выбор поля для ввода в зависимости от значения введенного параметра
            if active_or_passive == "Active":
                result_properties = list(self.balance_entries[33])
            else:
                result_properties = list(self.balance_entries[34])

            result_start_entry = result_properties[1]
            active_end_entry = result_properties[2]

            # Смена состояния и ввод итоговой суммы на начало
            @enable_disable(result_start_entry)
            def change_start_sum():
                result_start_entry.delete(0, END)
                result_start_entry.insert(0, result_sum_start)

            # Смена состояния и ввод итоговой суммы на конец
            @enable_disable(active_end_entry)
            def change_start_sum():
                active_end_entry.delete(0, END)
                active_end_entry.insert(0, result_sum_end)

    def transfer_properties(self):  # Перенос данных по имуществу в баланс
        # Перенос каждой строчки из данных по имуществу
        for i in range(len(self.properties)):
            property_row_data = self.properties[i + 1]
            start_end = property_row_data[4].get()

            # Проверка значения поля "Начало / Конец"
            if start_end == "Начало":
                property_period = 1
            elif start_end == "Конец":
                property_period = 2
            else:
                continue  # Иначе - пропуск дальнейших действий
            try:
                # Проверка значений полей "Сумма" и "№ Актива / Пассива"
                active_passive_number = int(property_row_data[3].get())
                property_sum = int(property_row_data[2].get())
            except ValueError:
                pass
            else:
                try:  # Если значение из "№ Актива / Пассива" неправильно - ошибка
                    balance_property = list(self.balance_entries[active_passive_number])[property_period]
                except IndexError:
                    messagebox.showerror(title="Возникла ошибка",
                                         message="Проверьте правильность введенных данных в поле\n'№ Актива / Пассива'")
                else:
                    property_value = balance_property.get()  # Получение числового значения из таблицы по заданному ряду
                    if property_value == "":
                        property_value = 0
                    try:
                        property_value = int(property_value)
                    except ValueError:
                        messagebox.showerror(title="Возникла ошибка",
                                             message="Проверьте правильность введенных данных в таблице бух. баланса")
                    else:
                        # Сложение значения из таблицы с значением из данных по имуществу
                        #   удаление и замена значения в таблице
                        final_sum = property_value + property_sum
                        balance_property.delete(0, END)
                        balance_property.insert(0, final_sum)

    def save(self):  # Сохранение данных по бух. балансу
        # Сохранение данных в отдельный список
        complete_dict = []
        for i in range(len(self.balance_entries)):
            row_num = i
            row_start = self.balance_entries[i][1].get()
            row_end = self.balance_entries[i][2].get()
            complete_dict.append(
                {
                    "form": "balance",
                    "num": row_num,
                    "start": row_start,
                    "end": row_end,
                }
            )

        try:  # Если нет данных по имуществу, то пропуск ошибки
            for i in range(len(self.properties)):
                row_num = i + 1
                row_note = self.properties[i + 1][1].get()
                row_sum = self.properties[i + 1][2].get()
                row_active_passive = self.properties[i + 1][3].get()
                row_start_end = self.properties[i + 1][4].get()
                complete_dict.append(
                    {
                        "form": "property",
                        "num": row_num,
                        "note": row_note,
                        "sum": row_sum,
                        "active_passive": row_active_passive,
                        "start_end": row_start_end
                    }
                )
        except KeyError:
            pass

        # Сохранение списка в файл
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON File", ".json")],
                                                 initialdir="/Users/midle/PycharmProjects/Сохраненные файлы по балансу")

        with open(file_path, mode="w") as data_file:
            json.dump(complete_dict, data_file, indent=4)

    def open_file(self, global_frame, data):  # Открытие файла и введение данных в таблицу
        # Определение строк с данными по имуществу и создание баланса
        property_rows = 0
        properties = []
        for i in data:
            if i["form"] == "property":
                property_rows += 1
                properties.append(i)

        self.create_balance(global_frame, property_rows)

        # Введение данных в начало и конец каждого счета баланса
        for i in range(len(self.balance_entries)):
            self.balance_entries[i][1].insert(0, data[i]["start"])
            self.balance_entries[i][2].insert(0, data[i]["end"])

        # Заполнение строк с данными по имуществу, если они имеются
        for i in range(property_rows):
            self.properties[i + 1][1].insert(0, properties[i]["note"])
            self.properties[i + 1][2].insert(0, properties[i]["sum"])
            self.properties[i + 1][3].insert(0, properties[i]["active_passive"])
            self.properties[i + 1][4].insert(0, properties[i]["start_end"])
