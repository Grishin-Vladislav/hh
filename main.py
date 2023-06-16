from parser.hh import HHParser
from files.json import write_to_json

if __name__ == '__main__':
    hh = HHParser(max_workers=int(input('ENTER MAX THREADS: \n')))
    write_to_json(hh.vacancies_info)
