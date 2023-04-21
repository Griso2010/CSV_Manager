import os
import sys


class MyCSV:

    def readToList(self, file_path: None | str | os.PathLike = None, sep: str = ",") -> list[list[str]]:

        self.__reader(file_path, sep)  # Вызывали наш метод открытия файла

        res = list(map(lambda e: e.strip().split(sep), self.file_rows))  # Делаем список наших результатов

        return self.headers, res

    def readToDict(self, file_path: None | str | os.PathLike = None, sep: str = ",",
                   key_field_num: None | int = None) -> dict:
        self.__reader(file_path, sep)  # Вызывали наш метод открытия файла
        self.__select_key(key_field_num)  # Вызвали наш метод выбора ключа

        res = {}
        for next_row in self.file_rows:  # Бежим по строчкам файла
            single_object_dict = {}
            splitted = next_row.strip().split(sep)

            for i in range(len(splitted)): single_object_dict.update({self.headers[i]: splitted[i]})
            res.update({splitted[self.key_field_num]: single_object_dict})  # Создаем и обновляем словарь

        return res

    def __select_key(self, key_field_num):
        # Если не задали ключ
        if key_field_num == None:
            menu = "Select key field:\n"
            for i in range(len(self.headers)):
                menu += f'\n{i} - {self.headers[i]}'

            menu += '\n: '
            self.key_field_num = int(input(menu))
        # Ключ передали как аргумент
        else:
            self.key_field_num = key_field_num

    def __reader(self, file_path, sep):
        file_path = self.__select_file(file_path)  # Определяем наш путь
        with open(file_path, encoding='utf-8') as f:
            self.headers = f.readline().strip().split(sep)
            self.file_rows = f.readlines()

    def __select_file(self, file_path):
        # Если путь файла не указан
        if file_path == None:

            all_files = []
            for next_dir_entry in os.scandir(os.path.dirname(__file__)):  # Сканируем папочку
                if next_dir_entry.is_file() and next_dir_entry.name.split('.')[-1] == 'csv':
                    all_files.append(next_dir_entry)  # Если находим файл csv, добавляем его в список

            # Выбор файла
            menu_string = "Select input file:"
            for i in range(len(all_files)):
                menu_string += f'\n{i} - {all_files[i].name}'

            menu_string += '\n: '
            file_path = os.path.abspath(all_files[int(input(menu_string))])

        return file_path

    def __creating_file(self, file_path: None | str | os.PathLike = None):
        if file_path == None:
            # Проверка на создание нового файла
            match input('Create new file?[y]: ').upper():
                case 'Y':
                    while True:
                        self.file_to_write = os.path.join(os.path.dirname(__file__), input("Enter file name: "))
                        # Если файл с таким названием есть, выдаем ошибку
                        if os.path.exists(self.file_to_write):
                            print("File exists already")
                            continue
                        break

                case _:
                    self.file_to_write = self.__select_file(file_path)
        # Если путь к файлу передан
        else:
            self.file_to_write = file_path
            if os.path.exists(os.path.join(os.path.dirname(__file__), self.file_to_write)):
                print("FILE WRITER ERROR: File exists already")
                sys.exit()

    def writeFromDict(self, data_to_write: dict, file_path: None | str | os.PathLike = None, sep: str = ","):
        # Вызываю метод создания файла, если путь к файлу не указан
        self.__creating_file(file_path)

        # Создание строки, куда будет записана вся информация
        string_to_write = ''
        string_to_write += sep.join(self.headers) + '\n'
        match data_to_write:


            case dict(data_to_write):
                print('Dictionary ')
                self.headers = list((data_to_write[list(data_to_write)[0]]).keys())

                for k, v in data_to_write.items():

                    single_line = ""
                    for next_key in self.headers:
                        single_line += v.get(next_key) + sep

                    single_line = single_line.strip(sep)
                    single_line += "\n"
                    print(single_line)
                    string_to_write += single_line

            case _:
                print("incorrect")

        with open(self.file_to_write, 'w', encoding='utf-8') as f:
            f.write(string_to_write)

    def writeFromList(self, data_to_write: dict, file_path: None | str | os.PathLike = None, sep: str = ","):

        global string_to_write
        match data_to_write:
            case list(data_to_write) | tuple(data_to_write):
                print("List or tuple detected")

                for next_line in data_to_write: string_to_write += sep.join(next_line) + '\n'
                string_to_write = string_to_write.strip()

