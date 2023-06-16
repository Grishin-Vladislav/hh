from os import getcwd
import json


def write_to_json(vacancies: list[dict[str, str]]) -> None:
    with open(f'{getcwd()}/vacancies.json', 'w') as f:
        json.dump(vacancies, f, indent=4, ensure_ascii=False)
