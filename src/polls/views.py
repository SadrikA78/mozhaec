from django.contrib.admin.models import LogEntry
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import plotly.offline as opy
import plotly.graph_objs as go
import datetime
from plotly.offline import plot
from plotly.graph_objs import *
import plotly.express as px
import numpy as np
import geopandas
import shapely
import fiona
from cartopy import crs as ccrs
import folium
import plotly.figure_factory as ff
import numpy as np
import scipy as sp
import scipy.constants
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab
import matplotlib.patches
import cartopy.crs as ccrs
from matplotlib.dates import DateFormatter
import ephem
import requests
import cartopy.feature
import matplotlib.path as mpath
import cartopy
import pandas as pd
import sys
import dash_html_components as html
from django.core.serializers import serialize


from .forms import *
from django.views.generic import ListView, DetailView
from django.forms.formsets import formset_factory


from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, ColumnDataSource
from .satsimulation import *
import cartopy.feature
import matplotlib.path as mpath
from math import * 


from docxtpl import DocxTemplate
from re import search
from django.contrib.gis.gdal import SpatialReference, CoordTransform
import polls.AFAR  as afar

def format_pointstr_from_osmwidget(osm_output):
    srid = 3857
    pattern = '([0-9.]+,[0-9.]+)'
    c = search(pattern, osm_output).group(0).split(sep=',')
    coord = { 
            'srid': srid,
            'lat': c[0],
            'lon': c[1]
           }
    pointstr = "SRID={srid};POINT({lat} {lon})".format(**coord)

    return pointstr
#1. Расчет мощности шума на входе приемного устройства, Вт
def noise_power(P_0w, P_sr, P_sry, m, S, nu, K, wave_1, G_1db, R, dnz,P_sr1, G_0db):
    #data = {}
    #общие вычисления
    P_w = 10**(P_0w/10)
    P_y = P_sry/S
    S_tr = P_sr/P_y
    m_y = m/S
    m_tr = m_y*S
    #передатчик
    P_b = P_sr/nu
    P_sr2 = 10*log(P_sr,10)
    G_2db = 4*pi*K*(S_tr/(wave_1**2))
    G_db = 10*log(G_2db,10)
    P_0 = P_sr2 + G_db + G_1db + 10*log((wave_1/(1000*4*pi*R))**2,10)
    P_p = 10**(P_0/10)
    #приемник
    S_nz = pi*((dnz/2)**2)
    G_11 = 4*pi*K*S_nz/(wave_1**2)
    G = 10*log(G_11,10)
    Psr_1db = 10*log(P_sr1,10)
    P_sdb = Psr_1db + G + G_0db + 10*log((wave_1/(1000*4*pi*R))**2,10)
    P_s = 10**(P_sdb/10)
    #коэффициент подавления
    K_p = P_p/P_s
    # data['Потребляемая мощности на борту КА'] = P_w
    # data['Средняя излучаемая мощность помехи в дБВт']  = P_y
    # data['Площадь АФАР для заданной средней излучаемой мощности, м2']  = S_tr
    # data['Удельная масса АФАР на единицу поверхности, т/м2'] = m_y
    # data['Масса АФАР+СОТР для заданной средней излучаемой мощности, т'] = m_tr
    # data['Потребляемая мощность на борту КА, Вт'] = P_b
    # data['Cредняя излучаемая мощность помехи в дБВт'] = P_sr2
    # data['Коэффициент направленности передающей антенны'] = G_2db
    # data['КНД передающей антенны в дБ'] = G_db
    # data['Мощность помехового сигнала на поверхности Земли, дБВт'] = P_0
    # data['Потери на распространение, дБВт'] = 10*log((wave_1/(1000*4*pi*R))**2,10)
    # data['Мощность помехового сигнала на поверхности Земли в Вт'] = P_p
    # data['Площадь антенны наземного терминала объекта, м2'] = S_nz
    # data['КНД передающей антенны наземного терминала'] = G_11
    # data['КНД передающей антенны наземного терминала в дБ'] = G
    # data['Мощность полезного сигнала на поверхности Земли в дБВт'] = Psr_1db
    # data['Мощность сигнала на поверхности Земли в Вт'] = P_s
    # data['Коэффициент подавления'] = K_p
    return P_p
    
def start(request):
    coords = [(40.7831, -73.9712), (40.6782, -73.9412), (40.7282, -73.7949)]
    map = folium.Map(location=[40.7118, -74.0131], zoom_start=12)
    for coord in coords:
        folium.Marker(location=[coord[0], coord[1]]).add_to(map)
    map._repr_html_()
    import plotly.express as px
    df = px.data.gapminder().query("year == 2007")
    fig = px.line_geo(df, locations="iso_alpha",
                      color="continent", # "continent" is one of the columns of gapminder
                      projection="orthographic")
    #fig.show()
    m = folium.Map([51.5, -0.25], zoom_start=10)
    test = folium.Html('<b>Hello world</b>', script=True)
    popup = folium.Popup(test, max_width=2650)
    folium.RegularPolygonMarker(location=[51.5, -0.25], popup=popup).add_to(m)
    m=m._repr_html_() #updated
    fig = go.Figure()
    t = np.linspace(0, 2*np.pi, 100)
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div', include_plotlyjs = False, show_link = False , link_text = "" )
    #plot_div = plot([Scatter(x=x_data, y=y_data)], output_type='div', include_plotlyjs = False)# Scatter - линия,   Bar - диаграмма  
    #plot_div = plot(fig, output_type='div', include_plotlyjs = False)
    # a = html.Div([html.Div('Example Div', style={'color': 'blue', 'fontSize': 14}),
        # html.P('Example P', className='my-class', id='my-p-element')
        # ], style={'marginBottom': 50, 'marginTop': 25})
        
    fig = go.Figure()
    scatter = go.Scatter(x=[0,1,2,3], y=[0,1,2,3],
                         mode='lines', name='test',
                         opacity=0.6, marker_color='green')
    fig.add_trace(scatter)
    plt_div = plot(fig, output_type='div', include_plotlyjs = False)
    return render(request, "polls/start.html", context={'plot_div': plot_div, 'plt_div':plt_div})#, hh':a,  'map': m})

def show_map(request):  
    #creation of map comes here + business logic
    m = folium.Map([51.5, -0.25], zoom_start=10)
    test = folium.Html('<b>Hello world</b>', script=True)
    popup = folium.Popup(test, max_width=2650)
    folium.RegularPolygonMarker(location=[51.5, -0.25], popup=popup).add_to(m)
    m=m._repr_html_() #updated
    print (m)
    context = {'my_map': m}

    return render(request, 'polls/show_folium_map.html', context)


"""
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    
    передаем на все страницы, для корректного отображения sidebar
"""
#Главная страница
@login_required
def index(request):
    sat_system = SatSystem.objects.all()
    agencies = SpaceAgency.objects.all()
    country = Country.objects.all()
    nkus = NKU.objects.all()
    sats = Satellite.objects.all()
    actions = LogEntry.objects.filter(user=request.user).order_by('action_time').reverse()[:5]
    content = {'sat_system': sat_system, 'country':country, 'agencies':agencies, 'sats':sats, 'nkus':nkus, 'actions':actions}
    return render(request, 'polls/index.html', content)

#Просмотр спутниковой системы
@login_required
def sat_system(request, sat_system_id):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    current_sat_system = SatSystem.objects.get(id=sat_system_id)
    sats = Satellite.objects.filter(sat_system=current_sat_system)
    nku = NKU.objects.filter(sat_system=current_sat_system)
    points_as_geojson = []
    for i in nku:
        points_as_geojson.append(i.map_location)
    if len(Decoder.objects.filter(sat_system=current_sat_system))>0:
        decoder = Decoder.objects.filter(sat_system=current_sat_system)
        content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'sats':sats, 'nku':nku, 'points_as_geojson':points_as_geojson, 'decoder':decoder}
    else:
        content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'sats':sats, 'nku':nku, 'points_as_geojson':points_as_geojson}
    return render(request, 'polls/sat_system.html', content)

#Добавление бортового оборудования
#(1)
@login_required
def add_BA_1(request, sat_system_id):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    current_sat_system = SatSystem.objects.get(id=sat_system_id)
    sats = Satellite.objects.filter(sat_system=current_sat_system)
    nku = NKU.objects.filter(sat_system=current_sat_system)
    list_tag =['name', 'antenna', 'modulation', 'regime', 'power_output', 'num_cannal', 'KPD', 'sensity', 'diapazon_V']
    if request.POST:
        for i in sats:
            new_BA = Decoder(
                sat_system=current_sat_system, satellite=i, name=request.POST['name'], antenna=request.POST['antenna'], modulation=request.POST['modulation'], power_output=request.POST['power_output'], 
                sensity=request.POST['sensity'], regime=request.POST['regime'], KPD=request.POST['KPD'], num_cannal=request.POST['num_cannal'], diapazon_V = request.POST['diapazon_V']
                )
            new_BA.save()
        return HttpResponseRedirect('/add_BA_2/'+str(sat_system_id))
    content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'sats':sats, 'nku':nku, 'TYPE_ANTENNA':TYPE_ANTENNA, 'TYPE_MOD':TYPE_MOD, 'TYPE_REGIME':TYPE_REGIME}
    return render(request, 'polls/add_BA_1.html', content)
#Добавление бортового оборудования
#(2)
@login_required
def add_BA_2(request, sat_system_id):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    current_sat_system = SatSystem.objects.get(id=sat_system_id)
    sats = Satellite.objects.filter(sat_system=current_sat_system)
    nku = NKU.objects.filter(sat_system=current_sat_system)
    decs = Decoder.objects.filter(sat_system=current_sat_system)
    list_tag =['lenth_a', 'width_a', 'lenth_arm', 'lenth_sign_az', 'lenth_sign_ang', 'num_sign_az', 'num_sign_ang']
    if request.POST:
        for i in decs:
            new_AFAR = Decoder_antenna(
                decoder=i, lenth_a=request.POST['lenth_a'], width_a=request.POST['width_a'], lenth_arm=request.POST['lenth_arm'], lenth_sign_az=request.POST['lenth_sign_az'], 
                lenth_sign_ang=request.POST['lenth_sign_ang'], num_sign_az=request.POST['num_sign_az'], num_sign_ang=request.POST['num_sign_ang']
                )
            new_AFAR.save()
        return HttpResponseRedirect('/sat_system/'+str(sat_system_id))
    content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'sats':sats, 'nku':nku}
    return render(request, 'polls/add_BA_2.html', content)

#Изменение бортового оборудования
#(1)
@login_required
def edit_BA_1(request, sat_system_id):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    current_sat_system = SatSystem.objects.get(id=sat_system_id)
    sats = Satellite.objects.filter(sat_system=current_sat_system)
    nku = NKU.objects.filter(sat_system=current_sat_system)
    try:
        BA = Decoder.objects.filter(sat_system=current_sat_system).order_by('id')[0]
        content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'sats':sats, 'nku':nku, 'TYPE_ANTENNA':TYPE_ANTENNA, 'TYPE_MOD':TYPE_MOD, 'TYPE_REGIME':TYPE_REGIME, 'BA':BA}
    except IndexError:
        content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'sats':sats, 'nku':nku, 'TYPE_ANTENNA':TYPE_ANTENNA, 'TYPE_MOD':TYPE_MOD, 'TYPE_REGIME':TYPE_REGIME}        
    list_tag =['name', 'antenna', 'modulation', 'regime', 'power_output', 'num_cannal', 'KPD', 'sensity', 'diapazon_V']
    if request.POST:
        Decoder.objects.filter(sat_system=current_sat_system).delete()
        for i in sats:
            new_BA = Decoder(
                sat_system=current_sat_system, satellite=i, name=request.POST['name'], antenna=request.POST['antenna'], modulation=request.POST['modulation'], power_output=float(request.POST['power_output']), 
                sensity=request.POST['sensity'], regime=request.POST['regime'], KPD=request.POST['KPD'], num_cannal=request.POST['num_cannal'], diapazon_V = request.POST['diapazon_V']
                )
            new_BA.save()
        return HttpResponseRedirect('/add_BA_2/'+str(sat_system_id))
    return render(request, 'polls/edit_BA_1.html', content)
#(2)
@login_required
def edit_BA_2(request, sat_system_id):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    current_sat_system = SatSystem.objects.get(id=sat_system_id)
    sats = Satellite.objects.filter(sat_system=current_sat_system)
    nku = NKU.objects.filter(sat_system=current_sat_system)
    decs = Decoder.objects.filter(sat_system=current_sat_system)
    DECODER = Decoder_antenna.objects.get(decoder=Decoder.objects.filter(sat_system=current_sat_system).order_by('id')[0])
    list_tag =['lenth_a', 'width_a', 'lenth_arm', 'lenth_sign_az', 'lenth_sign_ang', 'num_sign_az', 'num_sign_ang']
    if request.POST:
        for i in decs:
            Decoder_antenna.objects.filter(decoder=i).delete()
            new_AFAR = Decoder_antenna(
                decoder=i, lenth_a=request.POST['lenth_a'], width_a=request.POST['width_a'], lenth_arm=request.POST['lenth_arm'], lenth_sign_az=request.POST['lenth_sign_az'], 
                lenth_sign_ang=request.POST['lenth_sign_ang'], num_sign_az=request.POST['num_sign_az'], num_sign_ang=request.POST['num_sign_ang']
                )
            new_AFAR.save()
        return HttpResponseRedirect('/sat_system/'+str(sat_system_id))
    content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'sats':sats, 'nku':nku, 'DECODER': DECODER}
    return render(request, 'polls/edit_BA_2.html', content)

# #Оценивание спутниковой системы (меню)
@login_required
def sat_system_estimate(request, sat_system_id,  sat_id, nku_id):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    terminals = Terminal.objects.all()
    if sat_id==0 and nku_id==0:
        current_sat_system = SatSystem.objects.get(id=sat_system_id)
        content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'terminals':terminals}
    elif nku_id==0:
        current_sat_system = SatSystem.objects.get(id=sat_system_id)
        sat = Satellite.objects.get(id=sat_id)
        content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'sat':sat, 'terminals':terminals}
    return render(request, 'polls/sat_system_estimate.html', content)
    
#Создание поиска 1 точка
@login_required
def point_search(request, sat_system_id,  sat_id, nku_id):
    #TLE_RAW(tle_full)
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    agency = SpaceAgency.objects.all()
    sats = Satellite.objects.all()
    nkus = NKU.objects.all()
    current_sat_system = SatSystem.objects.get(id=sat_system_id)
    # if request.method == 'POST':
        # print (request.POST['name'])
        # return HttpResponseRedirect('/')
    form = PointSearchForm()
    if sat_id==0 and nku_id==0:
        content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'sats':sats, 'nkus':nkus, 'form':form}
    elif nku_id==0:
        sat = Satellite.objects.get(id=sat_id)
        content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'sats':sats, 'nkus':nkus, 'form':form, 'sat':sat}
    return render(request,'polls/point_search.html', content)



#####СОЗДАНИЕ
#Создание космического оператора
@login_required        
def new_sat_operator(request):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    agency = SpaceAgency.objects.all()
    list_tag =['name', 'acronym', 'logo', 'country', 'type', 'data_foundation', 'CEO']
    if request.POST:
        new_Space_Ag = SpaceAgency(
            name=request.POST['name'], acronym=request.POST['acronym'], logo=request.POST['logo'], country=Country.objects.get(id=(request.POST['country'])), type=request.POST['type'],
            data_foundation=request.POST['data_foundation'].split('/')[2]+'-'+request.POST['data_foundation'].split('/')[1]+'-'+request.POST['data_foundation'].split('/')[0], CEO=request.POST['CEO'], launch_capable=True
            )
        new_Space_Ag.save()
        return HttpResponseRedirect('/')
    content = {'sat_system': sat_system, 'country':country, 'agency':agency, 'TYPE_AGENCY':TYPE_AGENCY}
    return render(request,'polls/create/new_sat_operator.html', content)
#Создание новой спутниковой системы
@login_required        
def new_sat_system(request):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    agency = SpaceAgency.objects.all()
    list_tag =['name', 'alternative_name', 'logo', 'status', 'country', 'agency', 'usage', 'coverage', 'plan_num_sat', 'num_sat', 'first_launch', 'orbit', 'altitude']
    if request.POST:
        new_sat_system = SatSystem(
            name=request.POST['name'],alternative_name=request.POST['alternative_name'],logo=request.POST['logo'],status=request.POST['status'],country=Country.objects.get(id=(request.POST['country'])), agency=SpaceAgency.objects.get(id=request.POST['agency']),usage=request.POST['usage'], 
            coverage=request.POST['coverage'],plan_num_sat=request.POST['plan_num_sat'],num_sat=request.POST['num_sat'],first_launch=request.POST['first_launch'].split('/')[2]+'-'+request.POST['first_launch'].split('/')[1]+'-'+request.POST['first_launch'].split('/')[0],orbit=request.POST['orbit'],altitude=request.POST['altitude']
            )
        new_sat_system.save()
        return HttpResponseRedirect('/')
    content = {'sat_system': sat_system, 'country':country, 'agency':agency, 'TYPE_USE':TYPE_USE, 'TYPE_STATUS':TYPE_STATUS, 'TYPE_COVARAGE':TYPE_COVARAGE, 'TYPE_ORBIT':TYPE_ORBIT}
    return render(request,'polls/create/new_sat_system.html', content)
#Создание нового КА
@login_required        
def new_ka(request):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    agency = SpaceAgency.objects.all()
    list_tag =['name', 'logo', 'SCN',  'NSSDC_ID', 'country', 'agency', 'sat_system','date_launch','type', 'mass', 'al_orbit',  'nac_orbit', 'period_orbit', 'zone_orbit']
    if request.POST:
        new_ka = Satellite(
            name=request.POST['name'], logo=request.POST['logo'],SCN=request.POST['SCN'],NSSDC_ID=request.POST['NSSDC_ID'], country=Country.objects.get(id=(request.POST['country'])), agency=SpaceAgency.objects.get(id=request.POST['agency']),sat_system=SatSystem.objects.get(id=(request.POST['sat_system'])),
            date_launch=request.POST['date_launch'].split('/')[2]+'-'+request.POST['date_launch'].split('/')[1]+'-'+request.POST['date_launch'].split('/')[0],type=request.POST['type'],mass=request.POST['mass'],al_orbit=request.POST['al_orbit'],nac_orbit=request.POST['nac_orbit'],period_orbit=request.POST['period_orbit'], zone_orbit=0, TLE=request.POST['TLE']
            )
        new_ka.save()
        return HttpResponseRedirect('/')
    content = {'sat_system': sat_system, 'country':country, 'agency':agency, 'TYPE_SAT':TYPE_SAT}
    return render(request,'polls/create/new_ka.html', content)
    #Создание нового ЗС
@login_required        
def new_nsu(request):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    agency = SpaceAgency.objects.all()
    form = MyGeoForm()
    list_tag =['country', 'agency', 'sat_system', 'type', 'location']
    if request.POST:
        pointstr = format_pointstr_from_osmwidget(request.POST['point'])
        new_nsu = NKU(
           country=Country.objects.get(id=(request.POST['country'])), agency=SpaceAgency.objects.get(id=request.POST['agency']),sat_system=SatSystem.objects.get(id=(request.POST['sat_system'])),type=request.POST['type'], 
            location=request.POST['location'],map_location = pointstr
            )
        new_nsu.save()
        return HttpResponseRedirect('/')
    content = {'sat_system': sat_system, 'country':country, 'agency':agency, 'form':form}
    return render(request,'polls/create/new_nsu.html', content)
#Создание терминала
@login_required    
def new_terminal(request, sat_system_id, sat_id):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    agency = SpaceAgency.objects.all()
    form = MyGeoForm()
    list_tag =['name', 'power', 'diametr']
    if request.POST:
        pointstr = format_pointstr_from_osmwidget(request.POST['point'])
        new_terminal = Terminal(name=request.POST['name'], power=request.POST['power'], diametr=request.POST['diametr'], map_location = pointstr)
        new_terminal.save()
        return HttpResponseRedirect('/sat_system/'+str(sat_system_id) +'/'+ str(sat_id) +'/0/estimate/')
    content = {'sat_system': sat_system, 'country':country, 'agency':agency, 'form':form}
    return render(request,'polls/create/add_new_terminal.html', content)
@login_required        
def energy(request):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    agency = SpaceAgency.objects.all()
    content = {'sat_system': sat_system, 'country':country, 'agency':agency}
    return render(request,'polls/earth-moon-system-dynamic.html', content)
    

########################################Рапорта
#рапорт спутниковая система - земная станция
@login_required        
def sys_nsu_raport(request, sat_system_id, z_station_id):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    agency = SpaceAgency.objects.all()
    current_sat_system = SatSystem.objects.get(id=sat_system_id)
    nku = NKU.objects.get(id=z_station_id)
    date = datetime.datetime.now()
    sats = Satellite.objects.filter(sat_system=current_sat_system)
    sat_windows_list=[]
    for sat in sats:
        info = {}
        info['sat'] =  Satellite.objects.get(id=sat.id).name
        info['sat_id'] =  Satellite.objects.get(id=sat.id).id
        #start_time = ephem.Date((2020,4,9))
        start_time = ephem.Date(date)
        end_time = start_time + 1.0 
        res_time = ephem.minute*1
            
        observer_lon = nku.map_location[0]
        observer_lat =  nku.map_location[1]
        gs_name = nku.type
        min_alt_for_comm = 7
        center_freq = 8345e6
        myformat = DateFormatter('%d.%m %H:%M')#('%d %b %I:%M')
            
        f = open(str(settings.PRIVATE_STORAGE_ROOT)+'/'+str(sat.TLE))
        f = f.read()
        mysat = ephem.readtle(f.split('\n')[0], f.split('\n')[1], f.split('\n')[2])
        observer = ephem.Observer()
        observer.lat = str(nku.map_location[1])
        observer.lon = str(nku.map_location[0])
            
        data = np.array(calcSatPosData(mysat, observer, start_time, end_time, res_time))
        #Calc windows where sat is visible to oberserver
        visible_windows_indexes = calcVisibleWindows(data[3], 0)
        visible_ground_track = []
        for window in visible_windows_indexes:
            data_x = data[:, window[0]:window[1]+1] #+1 Because selection to i-1
            visible_ground_track.append(data_x)

        #Calc windows where sat communicaiton is avalable due to altitude angle
        comm_windows_indexes = calcVisibleWindows(data[3], min_alt_for_comm)
        comm_ground_track = []
        for window in comm_windows_indexes:
            data_x = data[:, window[0]:window[1]+1] #+1 Because selection to i-1
            comm_ground_track.append(data_x)
        #Calc points where satellite crosses the equatorial plane
        equatorial_crossing_indexes = getEquatorialCrossing(data[2])
        equ_cross_pts = []
        for crossing in equatorial_crossing_indexes:
            data_x = data[1:2, crossing]
            equ_cross_pts.append(data_x)
        #Calculate communication times
        comm_times = []
        for window in comm_windows_indexes:
            duration_x = data[0][window[1]] - data[0][window[0]]
            comm_times.append(duration_x)

        #Calculate longest connection window
        longest_comm_window_index = 0
        for i in range(len(comm_windows_indexes)):
            length1 = comm_windows_indexes[longest_comm_window_index][1] - comm_windows_indexes[longest_comm_window_index][0]
            length2 = comm_windows_indexes[i][1] - comm_windows_indexes[i][0]
            if length2 >= length1:
                longest_comm_window_index = i
        #Время подключения:
        list_windows=[]
        comm_t = 0
        for i in range(len(comm_windows_indexes)):
            data_windows={}
            start_index = comm_windows_indexes[i][0]
            data_windows['start'] = myformat.format_data(data[0][start_index]) 
            data_windows['end'] = myformat.format_data(data[0][start_index]+(comm_times[0]))
            data_windows['duration'] = int(round(comm_times[i]/ephem.minute))
            comm_t = comm_t + int(round(comm_times[i]/ephem.minute))
            list_windows.append(data_windows)
        info['item'] = len(list_windows)
        info['windows'] = list_windows 
        info['comm_t'] = comm_t
        info['p'] = round(comm_t/(24*60)*100, 3)
        data_cov = []
        for j in data[3]:
            if j<7:
                data_cov.append(None)
            else:
                #data_cov.append(list(sats).index(sat)+1)
                data_cov.append(j)
        info['data_win'] = data_cov
        sat_windows_list.append(info) 
    ###ОТРИСОВКА   
    data_date=[]
    for i in data[0]:
        data_date.append(myformat.format_data(i))
    
    fig = go.Figure()
    comm_win_time = 0
    for jj in sat_windows_list:
        comm_win_time = comm_win_time + jj['comm_t']
        fig.add_trace(go.Scatter(
            x=data_date,
            y=jj['data_win'],
            name=jj['sat'],
        ))

    fig.update_layout(
        autosize=False,
        width=1500,
        height=500,
        margin=dict(
            l=0,
            r=50,
            b=0,
            t=0,
            pad=4
        )# ),
        # yaxis=dict(
            # ticktext=["доступность"],
            # tickvals=[7],
            # tickmode="array",
            # titlefont=dict(size=30),
        # )
    )

    fig.update_yaxes(automargin=True)
    
    plt_div = plot(fig, output_type='div', include_plotlyjs = False)
    comm_win_time = round(comm_win_time/(24*60)*100, 3)
    
    doc = DocxTemplate("my_word_template.docx")
    content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'nku':nku, 'sats':sats, 'date':date, 'sat_windows_list':sat_windows_list, 'plt_div':plt_div, 'comm_win_time':comm_win_time}
    context = content
    doc.render(context)
    doc.save("generated_doc.docx")
    return render(request,'polls/sys_nsu_raport.html', content)

#рапорт спутниковая система - терминал
@login_required        
def sys_terminal_raport(request, sat_system_id, terminal_id):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    agency = SpaceAgency.objects.all()
    current_sat_system = SatSystem.objects.get(id=sat_system_id)
    nku = Terminal.objects.get(id=terminal_id)
    date = datetime.datetime.now()
    sats = Satellite.objects.filter(sat_system=current_sat_system)
    sat_windows_list=[]
    for sat in sats:
        info = {}
        info['sat'] =  Satellite.objects.get(id=sat.id).name
        info['sat_id'] =  Satellite.objects.get(id=sat.id).id
        #start_time = ephem.Date((2020,4,9))
        start_time = ephem.Date(date)
        end_time = start_time + 1.0 
        res_time = ephem.minute*1
            
        observer_lon = nku.map_location[0]
        observer_lat =  nku.map_location[1]
        #gs_name = nku.type
        min_alt_for_comm = 7
        center_freq = 8345e6
        myformat = DateFormatter('%d.%m %H:%M')#('%d %b %I:%M')
            
        f = open(str(settings.PRIVATE_STORAGE_ROOT)+'/'+str(sat.TLE))
        f = f.read()
        mysat = ephem.readtle(f.split('\n')[0], f.split('\n')[1], f.split('\n')[2])
        observer = ephem.Observer()
        observer.lat = str(nku.map_location[1])
        observer.lon = str(nku.map_location[0])
            
        data = np.array(calcSatPosData(mysat, observer, start_time, end_time, res_time))
        #Calc windows where sat is visible to oberserver
        visible_windows_indexes = calcVisibleWindows(data[3], 0)
        visible_ground_track = []
        for window in visible_windows_indexes:
            data_x = data[:, window[0]:window[1]+1] #+1 Because selection to i-1
            visible_ground_track.append(data_x)

        #Calc windows where sat communicaiton is avalable due to altitude angle
        comm_windows_indexes = calcVisibleWindows(data[3], min_alt_for_comm)
        comm_ground_track = []
        for window in comm_windows_indexes:
            data_x = data[:, window[0]:window[1]+1] #+1 Because selection to i-1
            comm_ground_track.append(data_x)
        #Calc points where satellite crosses the equatorial plane
        equatorial_crossing_indexes = getEquatorialCrossing(data[2])
        equ_cross_pts = []
        for crossing in equatorial_crossing_indexes:
            data_x = data[1:2, crossing]
            equ_cross_pts.append(data_x)
        #Calculate communication times
        comm_times = []
        for window in comm_windows_indexes:
            duration_x = data[0][window[1]] - data[0][window[0]]
            comm_times.append(duration_x)

        #Calculate longest connection window
        longest_comm_window_index = 0
        for i in range(len(comm_windows_indexes)):
            length1 = comm_windows_indexes[longest_comm_window_index][1] - comm_windows_indexes[longest_comm_window_index][0]
            length2 = comm_windows_indexes[i][1] - comm_windows_indexes[i][0]
            if length2 >= length1:
                longest_comm_window_index = i
        #Время подключения:
        list_windows=[]
        comm_t = 0
        for i in range(len(comm_windows_indexes)):
            data_windows={}
            start_index = comm_windows_indexes[i][0]
            data_windows['start'] = myformat.format_data(data[0][start_index]) 
            data_windows['end'] = myformat.format_data(data[0][start_index]+(comm_times[0]))
            data_windows['duration'] = int(round(comm_times[i]/ephem.minute))
            comm_t = comm_t + int(round(comm_times[i]/ephem.minute))
            list_windows.append(data_windows)
        info['item'] = len(list_windows)
        info['windows'] = list_windows 
        info['comm_t'] = comm_t
        info['p'] = round(comm_t/(24*60)*100, 3)
        data_cov = []
        for j in data[3]:
            if j<7:
                data_cov.append(None)
            else:
                #data_cov.append(list(sats).index(sat)+1)
                data_cov.append(j)
        info['data_win'] = data_cov
        sat_windows_list.append(info) 
    ###ОТРИСОВКА   
    data_date=[]
    for i in data[0]:
        data_date.append(myformat.format_data(i))
    
    fig = go.Figure()
    comm_win_time = 0
    for jj in sat_windows_list:
        comm_win_time = comm_win_time + jj['comm_t']
        fig.add_trace(go.Scatter(
            x=data_date,
            y=jj['data_win'],
            name=jj['sat'],
        ))

    fig.update_layout(
        autosize=False,
        width=1500,
        height=500,
        margin=dict(
            l=0,
            r=50,
            b=0,
            t=0,
            pad=4
        )# ),
        # yaxis=dict(
            # ticktext=["доступность"],
            # tickvals=[7],
            # tickmode="array",
            # titlefont=dict(size=30),
        # )
    )

    fig.update_yaxes(automargin=True)
    
    plt_div = plot(fig, output_type='div', include_plotlyjs = False)
    comm_win_time = round(comm_win_time/(24*60)*100, 3)
    
    doc = DocxTemplate("my_word_template.docx")
    content  = {'sat_system': sat_system, 'country':country, 'current_sat_system':current_sat_system, 'nku':nku, 'sats':sats, 'date':date, 'sat_windows_list':sat_windows_list, 'plt_div':plt_div, 'comm_win_time':comm_win_time}
    context = content
    doc.render(context)
    doc.save("generated_doc.docx")
    return render(request,'polls/raport/sys_terminal_raport.html', content)






#рапорт КА - Земная станция
@login_required        
def ka_nsu_raport(request, sat_id, z_station_id):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    agency = SpaceAgency.objects.all()
    sat = Satellite.objects.get(id=sat_id)
    nku = NKU.objects.get(id=z_station_id)
    
    date = datetime.datetime.now()
    #start_time = ephem.Date((2020,4,9))
    start_time = ephem.Date(date)
    end_time = start_time + 1.0 
    res_time = ephem.minute*1
    
    observer_lon = nku.map_location[0]
    observer_lat =  nku.map_location[1]
    gs_name = nku.type
    min_alt_for_comm = 7
    center_freq = 8345e6
    myformat = DateFormatter('%d.%m %H:%M')#('%d %b %I:%M')
    
    f = open(str(settings.PRIVATE_STORAGE_ROOT)+'/'+str(sat.TLE))
    f = f.read()
    mysat = ephem.readtle(f.split('\n')[0], f.split('\n')[1], f.split('\n')[2])
    observer = ephem.Observer()
    observer.lat = str(nku.map_location[1])
    observer.lon = str(nku.map_location[0])
    
    data = np.array(calcSatPosData(mysat, observer, start_time, end_time, res_time))
    #Calc windows where sat is visible to oberserver
    visible_windows_indexes = calcVisibleWindows(data[3], 0)
    visible_ground_track = []
    for window in visible_windows_indexes:
        data_x = data[:, window[0]:window[1]+1] #+1 Because selection to i-1
        visible_ground_track.append(data_x)

        #Calc windows where sat communicaiton is avalable due to altitude angle
    comm_windows_indexes = calcVisibleWindows(data[3], min_alt_for_comm)
    comm_ground_track = []
    for window in comm_windows_indexes:
        data_x = data[:, window[0]:window[1]+1] #+1 Because selection to i-1
        comm_ground_track.append(data_x)
    #Calc points where satellite crosses the equatorial plane
    equatorial_crossing_indexes = getEquatorialCrossing(data[2])
    equ_cross_pts = []
    for crossing in equatorial_crossing_indexes:
        data_x = data[1:2, crossing]
        equ_cross_pts.append(data_x)
    #Calculate communication times
    comm_times = []
    for window in comm_windows_indexes:
        duration_x = data[0][window[1]] - data[0][window[0]]
        comm_times.append(duration_x)

    #Calculate longest connection window
    longest_comm_window_index = 0
    for i in range(len(comm_windows_indexes)):
        length1 = comm_windows_indexes[longest_comm_window_index][1] - comm_windows_indexes[longest_comm_window_index][0]
        length2 = comm_windows_indexes[i][1] - comm_windows_indexes[i][0]
        if length2 >= length1:
            longest_comm_window_index = i

    #Calculate doppler shift
    v_rel = np.array(sp.diff(data[5,:])) * ephem.second / res_time #in m/s
    doppler_shift = center_freq * (np.sqrt((sp.constants.c + v_rel)/(sp.constants.c - v_rel))-1)
    #Вычисление параметров орбиты:
    #-------------------------------------------------------------------
    n = float(mysat._n) #средняя угловая скорость объекта на орбите [оборотов в день]
    my = 3.986e14 #стандартный гравитационный параметр
    a = (my**(1/3))/(((2*n*np.pi)/86400)**(2/3))
    ecc = round(float(mysat._e), 4)
    inc = round(float(mysat._inc)*180/np.pi, 4)
    raan = round(float(mysat._raan)*180/np.pi, 4)
    ap = round(float(mysat._ap)*180/np.pi, 4)
    av_anom = round(float(mysat._M)*180/np.pi, 4)
    kepler = {}
    kepler['poluos'] = int(round(a/1000))
    kepler['excentri'] = ecc
    kepler['naklon'] = inc
    kepler['el_uz'] = raan
    kepler['pericentr'] = ap
    kepler['av_anom'] = av_anom
    list_windows=[]
    for i in range(len(comm_windows_indexes)):
        data_windows={}
        start_index = comm_windows_indexes[i][0]
        data_windows['start'] = myformat.format_data(data[0][start_index]) 
        data_windows['end'] = myformat.format_data(data[0][start_index]+(comm_times[0]))
        data_windows['duration'] = int(round(comm_times[i]/ephem.minute))
        list_windows.append(data_windows)
    summ = 0
    for jj in list_windows:
        summ = jj['duration'] + summ
       
    plt.figure(figsize=[18,14])
    world_map = plt.axes(projection=ccrs.PlateCarree())
    world_map.stock_img()
    # #Observer
    world_map.plot(observer.lon*180/np.pi, observer.lat*180/np.pi,"b*",ms=10,transform=ccrs.Geodetic(), label="observer")
    # #Ground track
    world_map.plot(data[1],data[2],"r",ms=4, transform=ccrs.Geodetic(), label="ground track")
    #Plot ground track where sat is visible to observer
    for point in visible_ground_track:
        world_map.plot(point[1],point[2],"y",ms=4,transform=ccrs.Geodetic())
    #Plot ground track where altitude is high enough for communication
    for point in comm_ground_track:
        world_map.plot(point[1],point[2],"g",ms=4,transform=ccrs.Geodetic())
    #Plot ground track for best connection
    world_map.plot(comm_ground_track[longest_comm_window_index][1],comm_ground_track[longest_comm_window_index][2],"black",ms=4,transform=ccrs.Geodetic())
    #Plot indexes of equatorial crossings
    for i in range(len(equ_cross_pts)):
        world_map.text(equ_cross_pts[i][0], 0, i+1)
    #Cosmetics
    #plt.title("Ground track for satellite (" + str(sat_id) + """) from """ + myformat.format_data(start_time-0.5) + " to " + myformat.format_data(end_time-0.5) + " regarding GS " + gs_name + ".")
    world_map.gridlines()
    patch_a = matplotlib.patches.Patch(color="red", label="спутник ниже горизонта")
    patch_b = matplotlib.patches.Patch(color="yellow", label="спутник выше горизонта")
    patch_c = matplotlib.patches.Patch(color="green", label="спутник на высоте передачи")
    patch_d = matplotlib.patches.Patch(color="black", label="самое большое окно")
    patch_e = matplotlib.patches.Patch(color="blue", label="земная станция")
    plt.legend(handles=[patch_a, patch_b, patch_c, patch_d, patch_e], bbox_to_anchor=(0.5, 0.0), loc="upper center", ncol = 20)
    #plt.show()
    path_to_load2 = (str(settings.MEDIA_ROOT)+'/sat2.png')
    plt.savefig(path_to_load2)
    
    f = plt.figure(figsize=[18,18])
    world_map = plt.axes(projection=ccrs.Orthographic(observer_lon,observer_lat))
    #world_map = plt.axes(projection=ccrs.NorthPolarStereo(), sharex = world_map1, sharey = world_map1)
    f.subplots_adjust(bottom=0.05, top =0.95, left = 0.04, right = 0.95, wspace = 0.02)
    #world_map.set_extent([-180,180,-90,-60], ccrs.PlateCarree())
    world_map.stock_img()
    #Observer
    world_map.plot(observer.lon*180/np.pi, observer.lat*180/np.pi,"b*",ms=10,transform=ccrs.Geodetic(), label="observer")
    #Ground track
    world_map.plot(data[1],data[2],"r",ms=4,transform=ccrs.Geodetic(), label="ground track")
    #Plot ground track where sat is visible to observer
    for point in visible_ground_track:
      #print (len(point[1]))
      world_map.plot(point[1],point[2],"y",ms=4,transform=ccrs.Geodetic())
    #Plot ground track where altitude is high enough for communication
    for point in comm_ground_track:
      world_map.plot(point[1],point[2],"g",ms=4,transform=ccrs.Geodetic())
    #Plot ground track for best connection
    world_map.plot(comm_ground_track[longest_comm_window_index][1],comm_ground_track[longest_comm_window_index][2],"black",ms=4,transform=ccrs.Geodetic())
    #Plot indexes of equatorial crossings
    for i in range(len(equ_cross_pts)):
      world_map.text(equ_cross_pts[i][0], 0, i+1)
    #Cosmetics
    world_map.gridlines()
    theta = np.linspace(0,2*np.pi,100)
    center, radius = [0.5,0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts*radius+center)
    #world_map.set_boundary(circle, transform=world_map.transAxes)
    patch_a = matplotlib.patches.Patch(color="red", label="спутник ниже горизонта")
    patch_b = matplotlib.patches.Patch(color="yellow", label="спутник выше горизонта")
    patch_c = matplotlib.patches.Patch(color="green", label="спутник на высоте передачи")
    patch_d = matplotlib.patches.Patch(color="black", label="самое большое окно")
    patch_e = matplotlib.patches.Patch(color="blue", label="земная станция")
    plt.legend(handles=[patch_a, patch_b, patch_c, patch_d, patch_e], bbox_to_anchor=(0.5, 0.0), loc="upper center", ncol = 20)
    #plt.show()
    path_to_load1 = (str(settings.MEDIA_ROOT)+'/sat1.png')
    plt.savefig(path_to_load1)
    fig = go.Figure()
    data_date=[]
    for i in data[0]:
        data_date.append(myformat.format_data(i))
    scatter = go.Line(x=data_date, y=data[3],
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig.add_trace(scatter)
    
    fig.update_layout(
        autosize=False,
        width=500,
        height=300,
        margin=dict(
            l=0,
            r=50,
            b=0,
            t=0,
            pad=4
        )# ),
        # yaxis=dict(
            # ticktext=["доступность"],
            # tickvals=[7],
            # tickmode="array",
            # titlefont=dict(size=30),
        # )
    )

    fig.update_yaxes(automargin=True)
    
    plt_div = plot(fig, output_type='div', include_plotlyjs = False)
   

   #### AZIMUTE
    fig_az =  go.Figure()
    scatter = go.Line(x=data_date, y=data[4],
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig_az.add_trace(scatter)
    
    fig_az.update_layout(
        autosize=False,
        width=500,
        height=300,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
        )
    )

    fig_az.update_yaxes(automargin=True)
    plt_div_az = plot(fig_az, output_type='div', include_plotlyjs = False)
    
    
    ###Расстояние от КА до ЗС
    fig_al =  go.Figure()
    scatter = go.Line(x=data_date, y=data[5],
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig_al.add_trace(scatter)
    
    fig_al.update_layout(
        autosize=False,
        width=500,
        height=300,
        margin=dict(
            l=0,
            r=50,
            b=0,
            t=0,
            pad=4
        )
    )

    fig_al.update_yaxes(automargin=True)
    plt_div_al = plot(fig_al, output_type='div', include_plotlyjs = False)
    
    
    ###Доплеровский сдвиг
    fig_shift =  go.Figure()
    scatter = go.Line(x=data_date, y=doppler_shift,
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig_shift.add_trace(scatter)
    
    fig_shift.update_layout(
        autosize=True,
        margin=dict(
            l=0,
            r=50,
            b=0,
            t=0,
            pad=4
        )
    )

    fig_shift.update_yaxes(automargin=True)
    plt_div_shift= plot(fig_shift, output_type='div', include_plotlyjs = False)
    
    ###HEAT MAP
    fig_heatmap =  go.Figure()
    quakes = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')
    scatter = go.Densitymapbox(lat=quakes.Latitude, lon=quakes.Longitude, z=quakes.Magnitude, radius=10)
    fig_heatmap.add_trace(scatter)
    
    fig_heatmap.update_layout(
        mapbox_style="stamen-terrain",
        mapbox_center_lon=180,
        autosize=True,
        margin=dict(
            l=0,
            r=50,
            b=0,
            t=0,
            pad=4
        )
    )

    fig_heatmap.update_yaxes(automargin=True)
    plt_div_heatmap= plot(fig_heatmap, output_type='div', include_plotlyjs = False)
    
    
    date = datetime.datetime.now()
    content  = {'sat_system': sat_system, 'country':country, 'sat':sat, 'nku':nku, 'date':date, 'list_windows':list_windows, 'kepler':kepler, 'plt_div':plt_div, 'plt_div_az':plt_div_az, 'plt_div_al':plt_div_al, 'plt_div_shift':plt_div_shift, 'summ':summ, 'plt_div_heatmap':plt_div_heatmap}
    return render(request,'polls/ka_nsu_raport.html', content)

#рапорт КА - терминал
@login_required        
def ka_terminal_raport(request, sat_id, terminal_id):
    sat_system = SatSystem.objects.all()
    country = Country.objects.all()
    agency = SpaceAgency.objects.all()
    sat = Satellite.objects.get(id=sat_id)
    nku = Terminal.objects.get(id=terminal_id)
    date = datetime.datetime.now()
    c = 3*(10**8) #скорость света, м/с
    f = 1.575*(10**9)
    wave_1 = c/f #длина волны, м
    d_1 = 1.2*wave_1
    L = 0.25*wave_1
    d_2 = 1.2*wave_1
    n_1 = 134
    n_2 = 134
    nu = 0.4
    N = n_1*n_2
    az = 80
    ang_location = 180
    m = 1.6 #масса АФАР+СОТР, т (для расчета удельной массы)
    x = 6#ширина АФАР
    y = 2#длина АФАР
    S = x*y #площадь АФАР
    P_sry = 1000#средняя излучаемая мощность, Вт (для расчета уделной мощности)
    M_KA = 2.7#- масса КА, т
    P_sr = 1000#средняя излучаемая мощность, Вт
    P_sr1 = 100 #средняя излучаемая мощность объекта (Mil), Вт
    dnz = 0.7 #диаметр наземной антенны наземного терминала, м
    k_Bol = 1.38/(10**23) #постоянная Больцмана, Дж/К
    K = 0.8 #коэффициент, зависящий от конструкции, качества выполнения антенны и уровня ее потерь
    R = 40000 #дальность от радиолинии КА-ЗС, км
    nu = 0.5 #КПД антенны
    #f = 10 *(10**9) #заданный диапазон частоты, Гц
    P_0w = -157 #Мощность шума, дБВт
    #Примем КНД передающей??? антенны наземного терминала, дБ:
    G_1db = 10
    #Примем КНД приемной антенны наземного терминала, дБ:
    G_0db = 40
    
    #Для азимутальной плоскости
    shift_vibro_az = afar._shift_vibro_az(wave_1, d_1, az, ang_location)

    #Для угломерной плоскости
    shift_vibro_ang = afar._shift_vibro_ang(wave_1, d_2, az, ang_location)
    


    #Расчет нормированной амплитудной характеристики направленности АР
    list_norm_feature_AFAR =[]
    for i in np.arange(0,360,0.9):
        try:
            list_norm_feature_AFAR.append(afar.norm_feature_AFAR(wave_1, d_1, d_2, L, n_1, n_2, nu, i, 180, shift_vibro_az, shift_vibro_ang))
        except ZeroDivisionError:
            list_norm_feature_AFAR.append(1)
    #### АФАР 1 рисунок
    fig_AFAR_1 =  go.Figure()
    scatter = go.Line(x=np.arange(0,360), y=list_norm_feature_AFAR,
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig_AFAR_1.add_trace(scatter)
    
    fig_AFAR_1.update_layout(
        autosize=False,
        width=900,
        height=500,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
        )
    )

    fig_AFAR_1.update_yaxes(automargin=True)
    plt_div_AFAR_1 = plot(fig_AFAR_1, output_type='div', include_plotlyjs = False)
    
    list_f_10 =[]
    for i in np.arange(0,360):
        try:
            list_f_10.append(afar.f_10(wave_1, L, az, i))
        except ZeroDivisionError:
            print ('Error', i)
            list_f_10.append(1) 
    fig_AFAR_2 =  go.Figure()
    scatter = go.Scatterpolar(r = list_norm_feature_AFAR, theta = list(np.arange(0,360)),
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig_AFAR_2.add_trace(scatter)
    
    fig_AFAR_2.update_layout(
        autosize=False,
        width=500,
        height=300,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
        )
    )

    fig_AFAR_2.update_yaxes(automargin=True)
    plt_div_AFAR_2 = plot(fig_AFAR_2, output_type='div', include_plotlyjs = False)
    
    ###Расчет амплитудной характеристики направленности вибратора 
    list_f_10 =[]
    for i in np.arange(0,360):
        try:
            list_f_10.append(afar.f_10(wave_1, L, az, i))
        except ZeroDivisionError:
            print ('Error', i)
            list_f_10.append(1) 
    fig_AFAR_3 =  go.Figure()
    scatter = go.Scatterpolar(r = list_f_10, theta = list(np.arange(0,360)),
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig_AFAR_3.add_trace(scatter)
    
    fig_AFAR_3.update_layout(
        autosize=False,
        width=500,
        height=300,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
        )
    )

    fig_AFAR_3.update_yaxes(automargin=True)
    plt_div_AFAR_3 = plot(fig_AFAR_3, output_type='div', include_plotlyjs = False)
    
    
    start_time = ephem.Date(date)
    end_time = start_time + 1.0 
    res_time = ephem.minute*1
    
    observer_lon = nku.map_location[0]
    observer_lat =  nku.map_location[1]
    #gs_name = nku.type
    min_alt_for_comm = 7
    center_freq = nku.power
    myformat = DateFormatter('%d.%m %H:%M')#('%d %b %I:%M')
    
    f = open(str(settings.PRIVATE_STORAGE_ROOT)+'/'+str(sat.TLE))
    f = f.read()
    mysat = ephem.readtle(f.split('\n')[0], f.split('\n')[1], f.split('\n')[2])
    observer = ephem.Observer()
    observer.lat = str(nku.map_location[1])
    observer.lon = str(nku.map_location[0])
    
    data = np.array(calcSatPosData(mysat, observer, start_time, end_time, res_time))
    #Calc windows where sat is visible to oberserver
    visible_windows_indexes = calcVisibleWindows(data[3], 0)
    visible_ground_track = []
    for window in visible_windows_indexes:
        data_x = data[:, window[0]:window[1]+1] #+1 Because selection to i-1
        visible_ground_track.append(data_x)

        #Calc windows where sat communicaiton is avalable due to altitude angle
    comm_windows_indexes = calcVisibleWindows(data[3], min_alt_for_comm)
    comm_ground_track = []
    for window in comm_windows_indexes:
        data_x = data[:, window[0]:window[1]+1] #+1 Because selection to i-1
        comm_ground_track.append(data_x)
    #Calc points where satellite crosses the equatorial plane
    equatorial_crossing_indexes = getEquatorialCrossing(data[2])
    equ_cross_pts = []
    for crossing in equatorial_crossing_indexes:
        data_x = data[1:2, crossing]
        equ_cross_pts.append(data_x)
    #Calculate communication times
    comm_times = []
    for window in comm_windows_indexes:
        duration_x = data[0][window[1]] - data[0][window[0]]
        comm_times.append(duration_x)

    #Calculate longest connection window
    longest_comm_window_index = 0
    for i in range(len(comm_windows_indexes)):
        length1 = comm_windows_indexes[longest_comm_window_index][1] - comm_windows_indexes[longest_comm_window_index][0]
        length2 = comm_windows_indexes[i][1] - comm_windows_indexes[i][0]
        if length2 >= length1:
            longest_comm_window_index = i

    #Calculate doppler shift
    v_rel = np.array(sp.diff(data[5,:])) * ephem.second / res_time #in m/s
    doppler_shift = center_freq * (np.sqrt((sp.constants.c + v_rel)/(sp.constants.c - v_rel))-1)
    #Вычисление параметров орбиты:
    #-------------------------------------------------------------------
    n = float(mysat._n) #средняя угловая скорость объекта на орбите [оборотов в день]
    my = 3.986e14 #стандартный гравитационный параметр
    a = (my**(1/3))/(((2*n*np.pi)/86400)**(2/3))
    ecc = round(float(mysat._e), 4)
    inc = round(float(mysat._inc)*180/np.pi, 4)
    raan = round(float(mysat._raan)*180/np.pi, 4)
    ap = round(float(mysat._ap)*180/np.pi, 4)
    av_anom = round(float(mysat._M)*180/np.pi, 4)
    kepler = {}
    kepler['poluos'] = int(round(a/1000))
    kepler['excentri'] = ecc
    kepler['naklon'] = inc
    kepler['el_uz'] = raan
    kepler['pericentr'] = ap
    kepler['av_anom'] = av_anom
    list_windows=[]
    for i in range(len(comm_windows_indexes)):
        data_windows={}
        start_index = comm_windows_indexes[i][0]
        data_windows['start'] = myformat.format_data(data[0][start_index]) 
        data_windows['end'] = myformat.format_data(data[0][start_index]+(comm_times[0]))
        data_windows['duration'] = int(round(comm_times[i]/ephem.minute))
        list_windows.append(data_windows)
    summ = 0
    for jj in list_windows:
        summ = jj['duration'] + summ
       
    plt.figure(figsize=[18,14])
    world_map = plt.axes(projection=ccrs.PlateCarree())
    world_map.stock_img()
    # #Observer
    world_map.plot(observer.lon*180/np.pi, observer.lat*180/np.pi,"b*",ms=10,transform=ccrs.Geodetic(), label="observer")
    # #Ground track
    world_map.plot(data[1],data[2],"r",ms=4, transform=ccrs.Geodetic(), label="ground track")
    #Plot ground track where sat is visible to observer
    for point in visible_ground_track:
        world_map.plot(point[1],point[2],"y",ms=4,transform=ccrs.Geodetic())
    #Plot ground track where altitude is high enough for communication
    for point in comm_ground_track:
        world_map.plot(point[1],point[2],"g",ms=4,transform=ccrs.Geodetic())
    #Plot ground track for best connection
    world_map.plot(comm_ground_track[longest_comm_window_index][1],comm_ground_track[longest_comm_window_index][2],"black",ms=4,transform=ccrs.Geodetic())
    #Plot indexes of equatorial crossings
    for i in range(len(equ_cross_pts)):
        world_map.text(equ_cross_pts[i][0], 0, i+1)
    #Cosmetics
    #plt.title("Ground track for satellite (" + str(sat_id) + """) from """ + myformat.format_data(start_time-0.5) + " to " + myformat.format_data(end_time-0.5) + " regarding GS " + gs_name + ".")
    world_map.gridlines()
    patch_a = matplotlib.patches.Patch(color="red", label="спутник ниже горизонта")
    patch_b = matplotlib.patches.Patch(color="yellow", label="спутник выше горизонта")
    patch_c = matplotlib.patches.Patch(color="green", label="спутник на высоте передачи")
    patch_d = matplotlib.patches.Patch(color="black", label="самое большое окно")
    patch_e = matplotlib.patches.Patch(color="blue", label="земная станция")
    plt.legend(handles=[patch_a, patch_b, patch_c, patch_d, patch_e], bbox_to_anchor=(0.5, 0.0), loc="upper center", ncol = 20)
    #plt.show()
    path_to_load2 = (str(settings.MEDIA_ROOT)+'/sat2.png')
    plt.savefig(path_to_load2)
    
    f = plt.figure(figsize=[18,18])
    world_map = plt.axes(projection=ccrs.Orthographic(observer_lon,observer_lat))
    #world_map = plt.axes(projection=ccrs.NorthPolarStereo(), sharex = world_map1, sharey = world_map1)
    f.subplots_adjust(bottom=0.05, top =0.95, left = 0.04, right = 0.95, wspace = 0.02)
    #world_map.set_extent([-180,180,-90,-60], ccrs.PlateCarree())
    world_map.stock_img()
    #Observer
    world_map.plot(observer.lon*180/np.pi, observer.lat*180/np.pi,"b*",ms=10,transform=ccrs.Geodetic(), label="observer")
    #Ground track
    world_map.plot(data[1],data[2],"r",ms=4,transform=ccrs.Geodetic(), label="ground track")
    #Plot ground track where sat is visible to observer
    for point in visible_ground_track:
      #print (len(point[1]))
      world_map.plot(point[1],point[2],"y",ms=4,transform=ccrs.Geodetic())
    #Plot ground track where altitude is high enough for communication
    for point in comm_ground_track:
      world_map.plot(point[1],point[2],"g",ms=4,transform=ccrs.Geodetic())
    #Plot ground track for best connection
    world_map.plot(comm_ground_track[longest_comm_window_index][1],comm_ground_track[longest_comm_window_index][2],"black",ms=4,transform=ccrs.Geodetic())
    #Plot indexes of equatorial crossings
    for i in range(len(equ_cross_pts)):
      world_map.text(equ_cross_pts[i][0], 0, i+1)
    #Cosmetics
    world_map.gridlines()
    theta = np.linspace(0,2*np.pi,100)
    center, radius = [0.5,0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts*radius+center)
    #world_map.set_boundary(circle, transform=world_map.transAxes)
    patch_a = matplotlib.patches.Patch(color="red", label="спутник ниже горизонта")
    patch_b = matplotlib.patches.Patch(color="yellow", label="спутник выше горизонта")
    patch_c = matplotlib.patches.Patch(color="green", label="спутник на высоте передачи")
    patch_d = matplotlib.patches.Patch(color="black", label="самое большое окно")
    patch_e = matplotlib.patches.Patch(color="blue", label="земная станция")
    plt.legend(handles=[patch_a, patch_b, patch_c, patch_d, patch_e], bbox_to_anchor=(0.5, 0.0), loc="upper center", ncol = 20)
    #plt.show()
    path_to_load1 = (str(settings.MEDIA_ROOT)+'/sat1.png')
    plt.savefig(path_to_load1)
    fig = go.Figure()
    data_date=[]
    for i in data[0]:
        data_date.append(myformat.format_data(i))
    scatter = go.Line(x=data_date, y=data[3],
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig.add_trace(scatter)
    
    fig.update_layout(
        autosize=False,
        width=500,
        height=300,
        margin=dict(
            l=0,
            r=50,
            b=0,
            t=0,
            pad=4
        )# ),
        # yaxis=dict(
            # ticktext=["доступность"],
            # tickvals=[7],
            # tickmode="array",
            # titlefont=dict(size=30),
        # )
    )

    fig.update_yaxes(automargin=True)
    
    plt_div = plot(fig, output_type='div', include_plotlyjs = False)
   

   #### AZIMUTE
    fig_az =  go.Figure()
    scatter = go.Line(x=data_date, y=data[4],
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig_az.add_trace(scatter)
    
    fig_az.update_layout(
        autosize=False,
        width=500,
        height=300,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
        )
    )

    fig_az.update_yaxes(automargin=True)
    plt_div_az = plot(fig_az, output_type='div', include_plotlyjs = False)
    
    
    ###Расстояние от КА до ЗС
    fig_al =  go.Figure()
    scatter = go.Line(x=data_date, y=data[5],
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig_al.add_trace(scatter)
    
    fig_al.update_layout(
        autosize=False,
        width=500,
        height=300,
        margin=dict(
            l=0,
            r=50,
            b=0,
            t=0,
            pad=4
        )
    )

    fig_al.update_yaxes(automargin=True)
    plt_div_al = plot(fig_al, output_type='div', include_plotlyjs = False)
    
    
    ###Доплеровский сдвиг
    fig_shift =  go.Figure()
    scatter = go.Line(x=data_date, y=doppler_shift,
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig_shift.add_trace(scatter)
    
    fig_shift.update_layout(
        autosize=True,
        margin=dict(
            l=0,
            r=50,
            b=0,
            t=0,
            pad=4
        )
    )
    fig_shift.update_yaxes(automargin=True)
    plt_div_shift= plot(fig_shift, output_type='div', include_plotlyjs = False)
    
    list_noise_power = []
    for i in data[5]:
        list_noise_power.append(noise_power(P_0w, P_sr, P_sry, m, S, nu, K, wave_1, G_1db, i, dnz, P_sr1, G_0db))
    fig_K_noise =  go.Figure()
    scatter = go.Line(x=data_date, y=list_noise_power,
                         mode='lines', name='test',
                         opacity=0.8, marker_color='blue')
    fig_K_noise.add_trace(scatter)
    
    fig_K_noise.update_layout(
        autosize=False,
        width=900,
        height=500,
        margin=dict(
            l=0,
            r=50,
            b=0,
            t=0,
            pad=4
        )
    )
    fig_K_noise.update_yaxes(automargin=True)
    plt_K_noise = plot(fig_K_noise, output_type='div', include_plotlyjs = False)
    
    
    
    # fig_test =  go.Figure()
    # N=50
    # random_x = np.linspace(0, 1, N)
    # random_y0 = np.random.randn(N) + 5
    # random_y1 = np.random.randn(N)
    # random_y2 = np.random.randn(N) - 5
    # scatter = go.Mesh3d(x=(30*np.random.randn(N)),
                           # y=(25*np.random.randn(N)),
                           # z=(30*np.random.randn(N)),
                           # opacity=0.5,
                           # color='rgba(100,22,200,0.5)')
    # fig_test.add_trace(scatter)
    # fig_test.update_layout(
        # scene = dict(
                        # xaxis = dict(
                             # backgroundcolor="rgb(200, 200, 230)",
                             # gridcolor="white",
                             # showbackground=True,
                             # zerolinecolor="white",),
                        # yaxis = dict(
                            # backgroundcolor="rgb(230, 200,230)",
                            # gridcolor="white",
                            # showbackground=True,
                            # zerolinecolor="white"),
                        # zaxis = dict(
                            # backgroundcolor="rgb(230, 230,200)",
                            # gridcolor="white",
                            # showbackground=True,
                            # zerolinecolor="white",),),
        # autosize=False,
        # width=900,
        # height=500,
        # margin=dict(
            # l=0,
            # r=50,
            # b=0,
            # t=0,
            # pad=4
        # )
    # )
    # fig_test.update_yaxes(automargin=True)
    # plt_fig_test = plot(fig_test, output_type='div', include_plotlyjs = False)
    fig_test = go.Figure(data=[
        go.Mesh3d(
            x=[0, 1, 2, 0],
            y=[0, 0, 1, 2],
            z=[0, 2, 0, 1],
            # x=(np.arange(0,360)).tolist(),
            # y=(np.arange(0,360)).tolist(),
            # z=(np.arange(0,360)).tolist(),
            colorbar_title='z',
            # colorscale=[[0, 'gold'],
                        # [0.5, 'mediumturquoise'],
                        # [1, 'magenta']],
            # Intensity of each vertex, which will be interpolated and color-coded
            # intensity=[0, 0.33, 0.66, 1],
            # # i, j and k give the vertices of triangles
            # # here we represent the 4 triangles of the tetrahedron surface
            # i=[0, 0, 0, 1],
            # j=[1, 2, 3, 2],
            # k=[2, 3, 1, 3],
            name='y',
            showscale=True
        )
    ])
    fig_test.update_layout(
        scene = dict(
                        xaxis = dict(
                             backgroundcolor="rgb(200, 200, 230)",
                             gridcolor="white",
                             showbackground=True,
                             zerolinecolor="white",),
                        yaxis = dict(
                            backgroundcolor="rgb(230, 200,230)",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="white"),
                        zaxis = dict(
                            backgroundcolor="rgb(230, 230,200)",
                            gridcolor="white",
                            showbackground=True,
                            zerolinecolor="white",),),
        autosize=False,
        width=900,
        height=500,
        margin=dict(
            l=0,
            r=50,
            b=0,
            t=0,
            pad=4
        )
    )
    fig_test.update_yaxes(automargin=True)
    plt_fig_test = plot(fig_test, output_type='div', include_plotlyjs = False)
    
    date = datetime.datetime.now()
    content  = {
        'sat_system': sat_system, 'country':country, 'sat':sat, 'nku':nku, 'date':date, 'list_windows':list_windows, 'kepler':kepler, 
        'plt_div':plt_div, 'plt_div_az':plt_div_az, 'plt_div_al':plt_div_al, 'plt_div_shift':plt_div_shift, 'summ':summ, 
        'plt_div_AFAR_1':plt_div_AFAR_1, 'plt_div_AFAR_2':plt_div_AFAR_2, 'plt_div_AFAR_3':plt_div_AFAR_3, 'plt_K_noise':plt_K_noise, 'plt_fig_test':plt_fig_test
        }
    return render(request,'polls/raport/ka_terminal_raport.html', content)