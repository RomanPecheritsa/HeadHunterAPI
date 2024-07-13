from api.api_service import HhAPI
from models.vacancy import Vacancy
from storage.json_storage import JSONVacancyStorage
from typing import List


def sort_vac_for_salary(data: List[Vacancy]) -> List[Vacancy]:
    return sorted(data, reverse=True)


def top_sort_vac(data: List[Vacancy], top_n: int) -> List[Vacancy]:
    return data[:top_n]


def print_vac(data: List[Vacancy]) -> None:
    print("Найдены вакансии:\n")
    for vac in data:
        print(vac)


def user_interaction() -> None:
    hh_api = HhAPI()
    json_storage = JSONVacancyStorage()

    print('Добро пожаловать!')
    search_query = input("Введите поисковый запрос: ")
    data = hh_api.get_vacancies(search_query)
    vac_data = Vacancy.cast_to_object_list(data)
    json_storage.add_vacancy(vac_data)

    while True:
        print('\n1. Получить топ N вакансий по зарплате')
        print('2. Получить вакансии по желаемой зарплате')
        print('3. Получить вакансии с ключевым словом в описании')
        print('4. Удалить вакансию')
        print('5. Выход\n')

        user_choice = input('\nВыберите опцию: ')
        if user_choice == '1':
            menu_top_n_vac(json_storage)
        elif user_choice == '2':
            menu_get_vac_for_salary(json_storage)
        elif user_choice == '3':
            menu_get_vac_for_keyword(json_storage)
        elif user_choice == '5':
            print('Пока!')
            break
        else:
            print('Неверно введено значение. Попрбуйте еще раз\n')


def menu_top_n_vac(json_storage):
    data = json_storage.get_vacancies()
    n = input(f'\nВведите N: ')
    if not n.isdigit() and int(n) > 0:
        print('Необходимо ввести число')
    sort_data = sort_vac_for_salary(data)
    top_n = top_sort_vac(sort_data, int(n))
    print_vac(top_n)


def menu_get_vac_for_keyword(json_storage):
    keywords = input("Введите ключевые слова через пробел: ").split()
    vacancies = json_storage.get_vacancies_by_keywords(keywords)
    if vacancies:
        print_vac(vacancies)
    else:
        print("Вакансии по данным ключевым словам не найдены.")


def menu_get_vac_for_salary(json_storage):
    salary = input("Введите желаемую зарплату или диапазон зарплат через дефис: ")



