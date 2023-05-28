#-*- coding: utf-8 -*-
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.gis.db import models as geomodels
from django.contrib.gis import forms

# Create your models here.
private_storage = FileSystemStorage(location=settings.PRIVATE_STORAGE_ROOT)
media_storage = FileSystemStorage(location=settings.MEDIA_ROOT)


TYPE_AGENCY = (
        ('GOV', 'государственная организация'),
        ('CIV', 'частная корпорация'),
    )
TYPE_USE = (
        ('MIL', 'военное'),
        ('CIV', 'гражданское'),
        ('DUABLE', 'двойное'),
    )
TYPE_STATUS = (
        ('ACTIVE', 'в эксплуатации'),
        ('PASSIVE', 'не используется'),
    )   
TYPE_COVARAGE = (
        ('GLOB', 'глобальное'),
        ('REGION', 'региональное'),
    )
TYPE_ORBIT = (
        ('LEO', 'низкая'),
        ('AV_CIRC', 'средневысокая круговая'),
    )
TYPE_SAT = (
        ('USE', 'в эксплуатации'),
        ('LITTER', 'выведен из системы'),
        ('LEAVE', 'потерян из-за аварии'),
        ('TEST', 'на проверке'),
        ('READY', 'готовы к запуску'),
        ('PLAN', 'план'),
    )   
# TYPE_SAT = (
        # ('S', 'КА связи'),
        # ('R', 'КА ретрансляции'),
    # )
TYPE_ZS = (
        ('A', 'Тип А'),
        ('B', 'Тип Б'),
    )
TYPE_MOD = (
        ('AM', 'АМ'),
        ('QM', 'ЧМ'),
        ('FM', 'ФМ'),
    )
TYPE_REGIME = (
        ('1', 'активный'),
        ('0', 'пассивный'),
    )
    
TYPE_ANTENNA = (
        ('AF', 'АФАР'),
        ('F', 'ФАР'),
        ('DISH', 'зеркало'),
    )
#Класс страны
class Country(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Страна')
    img = models.FileField('Флаг', storage=media_storage)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        
#Класс космического агенства, оператора
class SpaceAgency (models.Model):
    name = models.CharField(max_length = 128, verbose_name='Космическое агенство')
    acronym = models.CharField(max_length = 128, verbose_name='Сокращенное название')
    logo = models.FileField('Логотип', storage=media_storage, default='settings.MEDIA_ROOT/anonymous.png')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, verbose_name='Страна происхождения', related_name='agency')
    type = models.CharField(default=TYPE_AGENCY[0][0], max_length = 128, choices=TYPE_AGENCY, verbose_name='Тип')
    data_foundation = models.DateField(default=datetime.date.today, verbose_name='Дата основания')
    CEO = models.CharField(default='', max_length = 128, verbose_name='Генеральный директор')
    launch_capable = models.BooleanField(default = True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Космическое агенство'
        verbose_name_plural = 'Космические агенства'
#Класс космодрома

#Класс спутниковая система
class SatSystem(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Полное название системы')
    alternative_name = models.CharField(default='', max_length = 128, verbose_name='Сокращенное название системы')
    logo = models.FileField('Изображение', storage=media_storage, default='settings.MEDIA_ROOT/anonymous.png')
    status = models.CharField(max_length = 128, choices=TYPE_STATUS, verbose_name='Статус')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, verbose_name='Страна происхождения', related_name='sat_system')
    agency = models.ForeignKey(SpaceAgency, on_delete=models.CASCADE, null=True, verbose_name='Оператор', related_name='sat_system')
    usage = models.CharField(max_length = 128, choices=TYPE_USE, verbose_name='Применение')
    coverage = models.CharField(max_length = 128, choices=TYPE_COVARAGE, verbose_name='Покрытие')
    plan_num_sat = models.IntegerField(default=0, verbose_name='Количество требуемых спутников')
    num_sat = models.IntegerField(default=0, verbose_name='На орбите')
    first_launch = models.DateField(verbose_name='Первый запуск')
    orbit = models.CharField(max_length = 128, choices=TYPE_ORBIT, verbose_name='Орбита')
    altitude = models.IntegerField(default=0, verbose_name='Высота')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Спутниковая система'
        verbose_name_plural = 'Спутниковые системы'
        
#Класс КА
class Satellite(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Наименование КА')
    logo = models.FileField('Изображение', storage=media_storage, default='settings.MEDIA_ROOT/anonymous.png')
    SCN = models.CharField(default=0, max_length = 128, verbose_name='Номер по спутниковому каталогу')
    NSSDC_ID = models.CharField(default=0, max_length = 128, verbose_name='Номер полета')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, related_name='sat')
    agency = models.ForeignKey(SpaceAgency, on_delete=models.CASCADE, null=True, related_name='sat')
    sat_system = models.ForeignKey(SatSystem, on_delete=models.CASCADE, null=True, related_name='sat')
    date_launch = models.DateField(default=datetime.date.today, verbose_name='Дата запуска')
    type = models.CharField(max_length = 128, choices=TYPE_SAT, verbose_name='Тип КА')
    ###баллистика
    mass = models.FloatField(default=1000, verbose_name='Масса спутника, кг')
    al_orbit = models.IntegerField(default=0, verbose_name='Высота орбиты, км')
    nac_orbit = models.FloatField(default=0, verbose_name='Наклонение, °')
    period_orbit = models.IntegerField(default=0, verbose_name='Период обращения, мин')
    zone_orbit = models.IntegerField(default=0, verbose_name='Диаметр зоны покрытия одного спутника, км')
    TLE = models.FileField('Файл TLE', storage=private_storage, default='settings.PRIVATE_STORAGE_ROOT/0.txt')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Спутник'
        verbose_name_plural = 'Спутники'


#Класс наземной инфраструктуры
class NKU(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, related_name='nku')
    agency = models.ForeignKey(SpaceAgency, on_delete=models.CASCADE, null=True, related_name='nku')
    sat_system = models.ForeignKey(SatSystem, on_delete=models.CASCADE, null=True, related_name='nku')
    type = models.CharField(max_length = 128, verbose_name='Тип')
    location = models.CharField(max_length = 128, verbose_name='Местоположение')
    map_location = geomodels.PointField()
    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Пункт управления'
        verbose_name_plural = 'НКУ'
#Класс точки поиска
class SearchPoint(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Название')
    loc = geomodels.PointField()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Точка поиска'
        verbose_name_plural = 'Точки поиска'      
#Класс множества точек поиска
class SearchMultiPoint(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Название')
    loc = geomodels.MultiPointField()
    #objects = geomodels.GeoManager()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Множество точек поиска'
        verbose_name_plural = 'Множества точек поиска'          

#Класс района поиска
class SearchPoligon(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Название')
    loc = geomodels.PolygonField()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район поиска'
        verbose_name_plural = 'Районы поиска'            

#Класс мультиполигона поиска
class SearchMultiPoligon(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Название')
    loc = geomodels.MultiPolygonField()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Множество районов поиска'
        verbose_name_plural = 'Множества районов поиска'      
# #Класс ЗС
# class Station(models.Model):
    # name = models.CharField(max_length = 128, verbose_name='Наименование ЗС')
    # type = models.CharField(max_length = 128,choices=TYPE_ZS, verbose_name='Тип ЗС')
    # #map_location = geomodels.PointField()
    # def __str__(self):
        # return self.name

    # class Meta:
        # verbose_name = 'Земная станция'
        # verbose_name_plural = 'Земные станции'

#Класс ЗС
class EarthStation(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Наименование ЗС')
    type = models.CharField(max_length = 128,choices=TYPE_ZS, verbose_name='Тип ЗС')
    map_location = geomodels.PointField()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Земная станция'
        verbose_name_plural = 'Земные станции'
        
#Класс многофункциональной космической системы
class MKS(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Наименование МКС')
    satellites = models.ManyToManyField(Satellite, verbose_name='Космический сегмент', blank=True)
    stations = models.ManyToManyField(EarthStation, verbose_name='Наземный сегмент', blank=True)
    class Meta:
        verbose_name = 'Многофункциональная космическая система'
        verbose_name_plural = 'Многофункциональные космические системы'


#Класс системы спутниковой связи и ретрансляции
class SSC(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Наименование системы')
    satellites_communication = models.ManyToManyField(Satellite, related_name='ka_communication', blank=True)
    satellites_transfer = models.ManyToManyField(Satellite, related_name='ka_transfer', blank=True)
    stations = models.ManyToManyField(EarthStation, verbose_name='Наземный сегмент', blank=True)
    class Meta:
        verbose_name = 'Система спутниковой связи и ретрянсляции'
        verbose_name_plural = 'Системы спутниковой связи и ретрянсляции'    
    
#Класс радиолинии
class Redioline (models.Model):
    satellite = models.ForeignKey(Satellite, on_delete=models.CASCADE, null=True)
    station = models.ForeignKey(EarthStation, on_delete=models.CASCADE, null=True)
    velocity = models.FloatField(default=80, verbose_name='Скорость')
    noize_stable = models.FloatField(default=80, verbose_name='Помехоустойчивость')
    class Meta:
        verbose_name = 'Радиолиния'
        verbose_name_plural = 'Радиолинии'    
        
#Класс приемника
class Encoder(models.Model):
    station = models.ForeignKey(EarthStation, on_delete=models.CASCADE, null=True)
    #station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length = 128, verbose_name='Наименование приемника')
    #diapason = ???#диапазон
    modulation = models.CharField(max_length = 128,choices=TYPE_MOD, verbose_name='Вид модуляции')
    sensity = models.FloatField(default=80, verbose_name='Чувствительность')
    #scale = ???#частота пропускания
    noize = models.FloatField(default=80, verbose_name='Коэффициент шума')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Приемник'
        verbose_name_plural = 'Приемники'

#Класс антены приемника
class Encoder_antenna(models.Model):
    encoder = models.ForeignKey(Encoder, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length = 128, verbose_name='Наименование антенны')
    type = models.CharField(max_length = 128,choices=TYPE_ANTENNA, verbose_name='Тип антенной системы')
    diametr = models.FloatField(default=80, verbose_name='Диаметр антенны')
    lenth_vawe = models.FloatField(default=80, verbose_name='Длина волны')
    num_vibro = models.IntegerField(default=80, verbose_name='Количество вибраторов')
    wave_num = models.FloatField(default=80, verbose_name='Волновое число')
    radius = models.FloatField(default=80, verbose_name='Радиус раскрытия')
    focus = models.FloatField(default=80, verbose_name='Фокусное расстояние')
    k_radius = models.FloatField(default=80, verbose_name='Коэффициент вытянутости')
    angle_os = models.FloatField(default=80, verbose_name='Угол отклонения луча от оси')
    KPD = models.FloatField(default=80, verbose_name='Коэффициент полезного действия')
    k_retire = models.FloatField(default=80, verbose_name='Коэффициент потерь')
    k_power = models.FloatField(default=80, verbose_name='Коэффициент усиления антенны')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Антена приемника'
        verbose_name_plural = 'Антены приемника'


#Класс передатчика
class Decoder(models.Model):
    sat_system = models.ForeignKey(SatSystem, on_delete=models.CASCADE, null=True, related_name='decoder')
    satellite = models.ForeignKey(Satellite, on_delete=models.CASCADE, null=True, related_name='decoder')
    #station = models.ForeignKey(EarthStation, on_delete=models.CASCADE, null=True, related_name='decoder')
    name = models.CharField(max_length = 128, verbose_name='Наименование приемника')
    antenna = models.CharField(default='АФАР', max_length = 128,choices=TYPE_ANTENNA, verbose_name='Тип антенны')
    modulation = models.CharField(max_length = 128,choices=TYPE_MOD, verbose_name='Вид модуляции')
    power_output = models.FloatField(default=80, verbose_name='Мощность выходного сигнала')
    sensity = models.FloatField(default=1, verbose_name='Уровень потерь антенны')
    regime = models.CharField(max_length = 128,choices=TYPE_REGIME, verbose_name='Режим работы')
    KPD = models.FloatField(default=1, verbose_name='Коэффициент полезного действия')
    num_cannal = models.IntegerField(default=80, verbose_name='Количество каналов')
    diapazon_V = models.FloatField(default=10**10, verbose_name='Количество каналов')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Передатчик'
        verbose_name_plural = 'Передатчики'


#Класс антены передатчика
class Decoder_antenna(models.Model):
    decoder = models.ForeignKey(Decoder, on_delete=models.CASCADE, null=True, related_name='dec_antenna')
    #name = models.CharField(max_length = 128, verbose_name='Наименование антенны')
    #type = models.CharField(default=80,max_length = 128,choices=TYPE_ANTENNA, verbose_name='Тип антенной системы')
    lenth_a = models.FloatField(default=0, verbose_name='Длина антенны')
    width_a = models.FloatField(default=0, verbose_name='Ширина антенны')
    #lenth_vawe = models.FloatField(default=80, verbose_name='Длина волны')
    lenth_arm = models.FloatField(default=1, verbose_name='Длина плеча')
    num_sign_az = models.IntegerField(default=5, verbose_name='Количество излучателей в аз. плоскости')
    num_sign_ang = models.IntegerField(default=5, verbose_name='Количество излучателей в угл. плоскости')
    lenth_sign_az = models.FloatField(default=1, verbose_name='Расстояние между излучателями в аз. плоскости')
    lenth_sign_ang = models.FloatField(default=1, verbose_name='Расстояние между излучателями в угл. плоскости')
    #angle_os = models.FloatField(default=80, verbose_name='Угол отклонения луча от оси')
    #k_retire = models.FloatField(default=80, verbose_name='Коэффициент потерь')
    #k_power = models.FloatField(default=80, verbose_name='Коэффициент усиления антенны')
    # def __str__(self):
        # return self.name

    class Meta:
        verbose_name = 'Антена передатчика'
        verbose_name_plural = 'Антены передатчика'

#Класс терминала/абонента
class Terminal(models.Model):
    name = models.CharField(max_length = 128, verbose_name='Наназвание терминала')
    map_location = geomodels.PointField()
    power = models.IntegerField(default=100, verbose_name='Средняя излучаемая мощность')
    diametr = models.FloatField(default=0, verbose_name='Диаметр антенны')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Терминал'
        verbose_name_plural = 'Терминалы'
