# import os  # imports to work from outside django
# import django
import matplotlib.pyplot as plt

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "legoparce.settings")
# django.setup()
#
from LEGOpng.models import Detmir


def visualise(set_id):  # получает уникальный номер набора LEGO
    dataset = Detmir.objects.filter(lego_sets_set_id=set_id).order_by('detmir_date')  # фильтрует записи из DB
    plot = plt.figure(figsize=(8, 4))  # создаем пустую фигуру (график)
    discprices = []  # пустые списки значений для графиков
    fullprices = []
    dates = []
    for obj in dataset:
        # print(obj.detmir_date, obj.detmir_fullprice, obj.detmir_discprice)
        if not discprices \
                or discprices[-1] != obj.detmir_discprice \
                or fullprices[-1] != obj.detmir_fullprice\
                or obj is dataset[len(dataset)-1]:  # проставляем точки на графике, только если цена менялась
            discprices.append(obj.detmir_discprice)
            fullprices.append(obj.detmir_fullprice)
            dates.append(str(obj.detmir_date)[5:])
    if not fullprices:  # если цен в DB нет, то возвращает пустой график
        return plot, 'Набора не было в продаже'
    minimum = min(discprices + fullprices)
    maximum = max(discprices + fullprices)
    plt.ylim((minimum - minimum / 20), (maximum + maximum / 5))  # нижняя и верхняя границы графика
    plt.plot(discprices, '-b', marker='o', markersize=9, label='Цена со скидкой')  # рисуем графики
    plt.plot(fullprices, '--r', marker='o', markersize=9, label='Цена без скидки')
    plt.xticks(range(len(dates)), [i for i in dates], size='small')
    for i in range(len(fullprices)):
        plt.annotate(fullprices[i], (i, fullprices[i] + fullprices[i] / 40))  # подписываем точки на графике
    for i in range(len(discprices)):
        plt.annotate(discprices[i], (i, discprices[i] + discprices[i] / 40))
    plt.suptitle('История цены для набора: ' + str(set_id))  # подписываем график (заглавие)
    plt.legend()
    plt.ylabel('Цена')  # подписываем оси
    plt.xlabel('Дата')

    return plot, min(discprices)
