from django.urls import path
from polls.views import *
from . import views
app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name='start'),
    path('sat_system/<int:sat_system_id>/', views.sat_system, name='sat_system'),
    path('sat_system/<int:sat_system_id>/<int:sat_id>/<int:nku_id>/estimate/', views.sat_system_estimate, name='sat_system_estimate'),
    path('show_map/', views.show_map, name='show_map'),
    #выдача информации 1 точка
    path('point_search/nsu/<int:sat_system_id>/<int:sat_id>/<int:nku_id>/estimate/', views.point_search, name='point_search'),
   
    
    
    ####РАПОРТА
    ##СПУТНИКОВАЯ СИСТЕМА
    ###NSU
    path('raport/sat_nsu/<int:sat_system_id>/<int:z_station_id>', views.sys_nsu_raport, name='sys_nsu_raport'),
    ###Один терминал, абонент
    path('raport/sys_terminal_raport/<int:sat_system_id>/<int:terminal_id>', views.sys_terminal_raport, name='sys_terminal_raport'),
    ##ОДИН КА
    ##NSU
    path('raport/ka_nsu/<int:sat_id>/<int:z_station_id>', views.ka_nsu_raport, name='ka_nsu_raport'),
    ###Один терминал, абонент
    path('raport/ka_terminal/<int:sat_id>/<int:terminal_id>', views.ka_terminal_raport, name='ka_terminal_raport'),
    
    
    ####Энергия
    path('energy/', views.energy, name='energy'),
    
    
    #ДОБАВЛЕНИЕ НОВЫХ ОБЪЕКТОВ
    #Космический оператор
    path('new_sat_operator/', views.new_sat_operator, name='new_sat_operator'),
    #Спутниковая система
    path('new_sat_system/', views.new_sat_system, name='new_sat_system'),
    #КА
    path('new_ka/', views.new_ka, name='new_ka'),
    #Наземная инфраструктура
    path('new_nsu/', views.new_nsu, name='new_nsu'),
    #Бортовое оборудование (1)
    path('add_BA_1/<int:sat_system_id>/', views.add_BA_1, name='add_BA_1'),
    #Бортовое оборудование (2)
    path('add_BA_2/<int:sat_system_id>/', views.add_BA_2, name='add_BA_2'),
    path('add_BA_2/<int:sat_system_id>/', views.add_BA_2, name='add_BA_2'),
    #NSU
    
    #Терминал
    path('new_terminal/<int:sat_system_id>/<int:sat_id>/', views.new_terminal, name='new_terminal'),
    
    ##Изменение
    #(1)
    path('edit_BA_1/<int:sat_system_id>/', views.edit_BA_1, name='edit_BA_1'),
    #(2)
    path('edit_BA_2/<int:sat_system_id>/', views.edit_BA_2, name='edit_BA_2'),
    
]