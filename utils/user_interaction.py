from api.api_service import HhAPI
from models.vacancy import Vacancy
from storage.json_storage import JSONVacancyStorage
from typing import List


def sort_vac_for_salary(data: List[Vacancy]) -> List[Vacancy]:
    return sorted(data, reverse=True)


def top_sort_vac(data: List[Vacancy], top_n: int) -> List[Vacancy]:
    return data[:top_n]


def print_vac(data: List[Vacancy]) -> None:
    print('\nНайдены вакансии:\n')
    for vac in data:
        print(vac)


def user_interaction() -> None:
    hh_api = HhAPI()
    json_storage = JSONVacancyStorage()

    print('Добро пожаловать!')
    search_query = input('Введите поисковый запрос: ')
    data = hh_api.get_vacancies(search_query)
    vac_data = Vacancy.cast_to_object_list(data)
    json_storage.add_vacancy(vac_data)

    while True:
        print('\n1. Получить все вакансии из файла')
        print('2. Получить топ N вакансий по зарплате')
        print('3. Получить вакансии по желаемой зарплате')
        print('4. Получить вакансии с ключевым словом в описании')
        print('5. Удалить вакансию')
        print('6. Выход\n')

        user_choice = input('\nВыберите опцию: ')
        if user_choice == '1':
            data_to_print = json_storage.get_vacancies()
            print_vac(data_to_print)
        elif user_choice == '2':
            menu_top_n_vac(json_storage)
        elif user_choice == '3':
            pass
        elif user_choice == '4':
            menu_get_vac_for_keyword(json_storage)
        elif user_choice == '5':
            menu_delete_vacancy(json_storage)
        elif user_choice == '6':
            print('\nПока!')
            break
        else:
            print('Неверно введено значение. Попрбуйте еще раз\n')


def menu_top_n_vac(json_storage: JSONVacancyStorage) -> None:
    data = json_storage.get_vacancies()
    n = input(f'\nВведите N: ')
    if not n.isdigit() and int(n) > 0:
        print('\nНеобходимо ввести число')
    sort_data = sort_vac_for_salary(data)
    top_n = top_sort_vac(sort_data, int(n))
    print_vac(top_n)


def menu_get_vac_for_keyword(json_storage: JSONVacancyStorage) -> None:
    keywords = input('\nВведите ключевые слова через пробел: ').split()
    vacancies = json_storage.get_vacancies_by_keywords(keywords)
    if vacancies:
        print_vac(vacancies)
    else:
        print('\nВакансии по данным ключевым словам не найдены')


def menu_delete_vacancy(json_storage: JSONVacancyStorage) -> None:
    vac_for_del = json_storage.get_vacancies()
    print_vac(vac_for_del)
    vacancy_id = input('Введите id вакансии, которую хотите удалить: ')
    if json_storage.delete_vacancy(vacancy_id):
        print(f'\nВакансия с id {vacancy_id} удалена.')
    else:
        print(f'\nВакансия с id {vacancy_id} не найдена.')




