import os
import django
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup


def get_html(adress):  # возвращает HTML код страницы по заданному адресу
    html_code = requests.get(adress).text
    return html_code


def get_tags(html):  # возвращает 'суп' из тэгов <p>
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all('p')
    return tags


def getproducts(tags):  # возвращает список списков [название, номер, цена со скидкой, без скидки]
    names = []
    pattern_num = r'\d{4,}'
    pattern_price = r'\d+\s*\d+'
    count = 0
    for tag in tags:  # алгоритм составлен экспериментальным путем под HTML код сайта detmir.ru
        try:
            if ' LEGO ' in str(tag.contents):
                count = 1
                name = str(tag.contents).replace('Конструктор LEGO', '').strip('[\']').lstrip(' ')
                lego_num = max(re.findall(pattern_num, name), key=len)
                names.append([name, int(lego_num)])
            elif 0 < count < 3 and '₽' in str(tag.contents):
                price = int(re.findall(pattern_price, str(tag.contents))[0].replace(' ', ''))
                names[-1].append(price)
                count += 1
        except Exception:  # все ошибки в исключения ?
            print('SOME ERROR', tag, 'count = ', count)
    return names


def prices_from_list_to_sql(products_list):  # вносит данные в БД, возвращает количество внесенных записей
    count = 0
    for legoset in products_list:
        if len(legoset) == 4:
            print('legoset ', legoset)
            try:  # проверка на наличие существующей записи в БД за сегодня
                b = Detmir.objects.get(lego_sets_set_id=legoset[1], detmir_date=date)
                if b:
                    print(legoset[1], 'уже создан', date)
            except Detmir.DoesNotExist:
                while True:  # проверка на наличие набора в БД. Добавление записи о наборе, затем записи о цене
                    try:
                        b = Detmir(detmir_fullprice=legoset[3], detmir_discprice=legoset[2],
                                   lego_sets_set_id=legoset[1], detmir_date=date)
                        b.save()  # сохраняет каждую позицию из списка в БД
                        count += 1
                    except django.db.utils.IntegrityError:
                        new_set = LegoSets(set_id=legoset[1], set_name=legoset[0])
                        new_set.save()
                        print('added set', legoset[0], legoset[1])
                        continue
                    break
    print(count)
    return count


def get_today_date():
    today_date = datetime.today().strftime('%Y-%m-%d')
    try:
        date_from_db = Dates.objects.get(pk=today_date)  # добавить проверку на наличии текущей даты в БД и добавить,
        # если ее нет
    except Dates.DoesNotExist:
        date_from_db = Dates(date_id=today_date)
        date_from_db.save()
    print(str(date_from_db))
    return date_from_db


def main():
    added_entries_count = 0
    numbered_page = 'https://www.detmir.ru/catalog/index/name/lego/page/'
    # циклом перебираем все ссылки
    num = 52  # сейчас на detmir.ru всего 52 страницы с наборами LEGO
    for n in range(1, num + 1):
        print(f'{n} из {num}')
        tags_soup = get_tags(get_html(numbered_page + str(n) + '/'))
        products = getproducts(tags_soup)
        for product in products:  # дополнительная проверка на длину вложенного списка (отсутствие цены без скидки)
            if len(product) == 3:
                product.append(product[2])
        added_entries = prices_from_list_to_sql(products)  # загоняет список в БД
        added_entries_count += added_entries
    print('Всего добавлено в БД', added_entries_count)
    return added_entries_count


if __name__ == '__main__':

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "legoparce.settings")
    django.setup()

    from LEGOpng.models import Detmir, LegoSets, Dates

    date = get_today_date()
    detmir_count = main()

    if detmir_count > int(date.detmir_count or 0):
        date.detmir_count = detmir_count
        date.save()
