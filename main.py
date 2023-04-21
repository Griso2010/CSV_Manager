import pathlib
from class_csv_manager import MyCSV

my_csv = MyCSV()
FILE_PATH = pathlib.Path(__file__).parent.joinpath('persons.csv')

headers, persons = my_csv.readToList(FILE_PATH, sep=';' )
persons_dict = my_csv.readToDict(FILE_PATH, key_field_num = 0, sep=';' )

my_csv.writeFromDict(persons_dict, sep=';') #



