#  TODO 1: (+) Обеспечение функционирования остатков на счетах - демонстрация их на счетах хоз. операций и правильное
#     вычисление сальдо по счету
#  TODO 2: (+) Изменение grid-системы в каждом счете - отдельный фрейм для всего счета и отдельных для счетов.
#     Это необходимо для правильной демонстрации горизонтальной черты после остатка по счету (если он есть)
#  TODO 3: (+) Сохранение введенных данных для журнала хозяйственных операций
#  TODO 4: (+) Выведение сохраненных данных в таблицу журнала хозяйственных операций
#  TODO 5: (+) Перенести кнопку "Открыть файл" в меню с определением параметров для журнала хоз. операций
#  TODO 6: (+) Ввести кнопку возврата к первоначальному меню
#  TODO 7: (+) Отредактировать код в "main.py"
#  TODO 8: (+) Отредактировать код в "business_journal.py"
#  TODO 9: (+) Отредактировать код в "account.py" - создать функцию для создания счетов.
#     (+) В конечном счете - "account.py" стал отдельной функцией в классе "BusinessJournal" в "business_journal.py"
#  TODO 10: (+) Отредактировать код в "balance.py"
#  TODO 11: (+) В балансе добавить Scrollbar для строк с данными по имуществу - отдельный Frame внутри global_frame
#  TODO 12: (+) Создание баланса бухгалтерского учета
#  TODO 13: (+) Обеспечение функционирования подсчета итогов по разделам
#  TODO 14: (+) Обеспечение динамичности окон со Scrollbar'ами до опр. лимита (balance.py + business_journal.py)
#  TODO 15: Обеспечение функционирования переноса данных по имуществу в баланс:
#     (+) написать кодовый номер для каждого счета баланса (1, 2, 3...) в отдельном Label'e
#     (+) после строк по имуществу добавить кнопку "Перенос в баланс",
#     (+) ввести данные в баланс, прибавляя имеющиеся в балансе значения
#  TODO 16: (+) Обеспечение функционирования подсчета итогов по пассиву и активу: подсчет сумм по итогам разделов
#     (+) Прокомментировать элемент кода с функционированием кнопок подсчета разделов и итогов по активу и пассиву
#  TODO 17: (+) Изменить меню баланса: открытие файла и его создание с вводом данных по имуществу сделать в одном окне
#     (+) В первоначальное меню добавить кнопку "Отчет о финансовых результатах"
#  TODO 18: (+) Перенести класс UserInterface из 'main.py' в отдельный файл
#  TODO 19: (+) Сохранение баланса бух. учета
#  TODO 20: (+) Открытие баланса бух. учета
#     (+) Введение данных из сохраненного файла в таблицу (используя self.balance_entries & self.properties)
#  TODO 21: (+) Создание отчета о финансовых результатах - GUI
#  TODO 22: (+) Сохранение ОФР
#  TODO 23: (+) Открытие ОФР


from menu import Menu

menu = Menu()
menu.create_starting_gui()