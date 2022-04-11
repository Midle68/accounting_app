from tkinter import *
from tkinter import filedialog
import json

COMMON_FONT = ("Arial", 13, "normal")
BOLD_FONT = ("Arial", 13, "bold")


def enable_disable(row):  # Изменение состояния объекта
    def change_state(function):
        row.config(state=NORMAL)
        function()
        row.config(state=DISABLED)
    return change_state


class FinancialReport:
    def __init__(self):
        self.frame = None
        self.rows_entries = []
        self.row = 1
        self.all_rows = {0: "Выручка", 1: "Себестоимость продаж", 2: "Валовая прибыль (убыток)",
                         3: "Коммерческие расходы", 4: "Управленческие расходы", 5: "Прибыль (убыток) от продаж",
                         6: "Доходы от участия в других организациях", 7: "Проценты к получению", 8: "Проценты к уплате",
                         9: "Прочие доходы", 10: "Прочие расходы", 11: "Прибыль (убыток) до налогообложения",
                         12: "Налог на прибыль", 13: "Чистая прибыль"}

    def create_report(self, global_frame):  # Создание ОФР
        self.frame = Frame(global_frame, pady=15, padx=15)
        self.frame.grid(row=1, column=0, columnspan=14)

        # Создание ОФР по каждой из строк 'self.all_rows'
        for i in range(len(self.all_rows)):  # Если строка - результат, то - особые параметры
            if i in [2, 5, 11, 13]:
                self.add_grid(i, result=True)
            else:
                self.add_grid(i)

        save_btn = Button(self.frame, text="Сохранить", width=12, height=3, command=self.save)
        save_btn.grid(row=self.row, column=3)

    def add_grid(self, row_num, result=False):  # Добавление grid-параметров каждой строке
        row_label = Label(self.frame, text=self.all_rows[row_num], font=COMMON_FONT)
        row_label.grid(row=self.row, column=0, sticky="w")

        row_entry = Entry(self.frame, font=COMMON_FONT)
        row_entry.grid(row=self.row, column=3, padx=10)

        self.rows_entries.append(row_entry)

        if result:  # Если строка - результат, то добавляются: 1) кнопка "посчитать" 2) жирный шрифт 3) Entry отключено.
            row_label.config(font=BOLD_FONT)
            row_entry.config(font=BOLD_FONT, state=DISABLED)

            row_count_btn = Button(self.frame, text="Посчитать",
                                   command=lambda: self.count(row_num))
            row_count_btn.grid(row=self.row, column=2)

        self.row += 1

    def count(self, row_num):  # Расчет результата, учитывая номер строки
        add = []
        start_range = 0

        # Учитываются ячейки для сложения и вычитания
        if row_num == 2:
            add = [0]
        elif row_num == 5:
            start_range = 2
            add = [2]
        elif row_num == 11:
            start_range = 5
            add = [5, 6, 7, 9]
        elif row_num == 13:
            start_range = 11
            add = [11]

        end_sum = 0
        # Подсчет значений, избежание ошибок - отсутствие значений, наличие или отсутствие "()" при вычете
        for i in range(start_range, row_num):
            try:
                value = self.rows_entries[i].get()
                if i in add:
                    end_sum += int(value)
                else:
                    try:
                        value = int(value.split("(")[1].split(")")[0])
                    except IndexError:
                        pass
                    end_sum -= int(value)
                    self.rows_entries[i].delete(0, END)
                    self.rows_entries[i].insert(0, f"({value})")
            except ValueError:
                pass

        # Смена состояния Entry и введение значений. При вычете - с "()"
        @enable_disable(self.rows_entries[row_num])
        def change_sum():
            self.rows_entries[row_num].delete(0, END)
            if end_sum:
                self.rows_entries[row_num].insert(0, end_sum)
            else:
                self.rows_entries[row_num].insert(0, f"({end_sum})")

    def save(self):  # Сохранение ОФР
        complete_dict = {}
        for i in range(len(self.rows_entries)):
            complete_dict[i] = self.rows_entries[i].get()

        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON File", ".json")],
                                                 initialdir="/Users/midle/PycharmProjects/Сохраненные файлы по ОФР")

        with open(file_path, mode="w") as data_file:
            json.dump(complete_dict, data_file, indent=4)

    def open_file(self, global_frame, data):  # Открытие файла
        self.create_report(global_frame)

        # Введение значений в кажую строку
        for i in range(len(data)):
            if i in [2, 5, 11, 13]:  # Если строка - результат, смена состояния и ввод значения
                @enable_disable(self.rows_entries[i])
                def enter_sum():
                    self.rows_entries[i].insert(0, data[str(i)])
            else:
                self.rows_entries[i].insert(0, data[str(i)])
