from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from io import BytesIO
import base64
# from .Parser.pot_visualise import visualise  # old visualiser
from .Parser.pot_from_SQL import visualise
from .models import Detmir, LegoSets
from django.db.models import Count

def index(request):
    context = {'today_date': datetime.today().strftime('%Y-%m-%d')}
    if request.method == 'POST':  # TODO заменить на GET, в адрес ссылки запихнуть параметры
        return HttpResponseRedirect(request.POST['lego_number'])
    else:
        return render(request, 'LEGOpng\index.html', context)


class LegoSetsEntry(ListView):
    model = LegoSets
    ordering = ['set_id']
    template_name = 'LEGOpng\\baseout.html'
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(detmir__detmir_date__isnull=False).annotate(Count('set_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today_date'] = datetime.today().strftime('%Y-%m-%d')
        context['rows_count'] = self.object_list.count()
        return context


class SetDetailView(DetailView):
    model = LegoSets
    context_object_name = 'legoset'
    # template_name = 'LEGOpng\\detailview.html'
    template_name = 'LEGOpng\\LEGO_request.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today_date'] = datetime.today().strftime('%Y-%m-%d')
        context['lego_number'] = self.object.set_id
        plot, context['minprice'] = visualise(context['lego_number'])
        # функция visualise() возвращает объект plot и минимальную стоимость

        stringfile = BytesIO()  # создается объект в памяти
        plot.savefig(stringfile, bbox_inches='tight')  # график сохраняется в объект stringfile
        image_b64 = base64.b64encode(stringfile.getvalue())
        image_b64 = str(image_b64, 'utf8')  # изображение кодируется в байтовую строку
        context['image_b64'] = image_b64
        # print(len(image_b64))
        return context
