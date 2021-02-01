from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('baseout', views.LegoSetsEntry.as_view(), name='baseout'),
    path('<int:pk>', views.SetDetailView.as_view(), name='set-detail')
]
