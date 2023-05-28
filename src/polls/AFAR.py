#!/usr/bin/env python
# coding: utf-8

from math import *
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
import plotly.graph_objects as go
import numpy as np

# # 1. Расчет массы АФАР + СОТР для заданной средней излучаемой мощности средств МКС РЭБ
#1. Расчет площади АФАР, м2:
def squre_AFAR(x,y):
    s = x*y
    return s

#2. Расчет удельной излучаемой мощности АФАР на единицу поверхности, Вт/м2:
def power_AFAR(p,squre_AFAR):
    pp = p/squre_AFAR
    return pp
#3. Расчет площади АФАР для заданной средней излучаемой мощности, м2:
def squre_power_AFAR(ave_p, power_AFAR):
    s = ave_p/power_AFAR
    return s
#4. Расчет удельной массы АФАР на единицу поверхности, т/м2:
def ave_mass_AFAR(mass, squre_AFAR):
    m = mass/squre_AFAR
    return m
#5. Расчет массы АФАР+СОТР для заданной средней излучаемой мощности, т:
def all_mass_AFAR(mass, squre_AFAR):
    m = mass*squre_AFAR
    return m

# # 2. Расчет числовых значений характеристик антенной решетки
#1. Расчет КНД передающей антенны в направлении максимального излучения, дБ:
def KND_decoder(k_construct, wave, d):
    g1_KND = 4*math.pi*k_construct*(math.pi*((d/wave)**2)/wave**2)
    return g1_KND

#2. Вычисление КУ передающей антенны:
def GL_decoder(k_construct, wave, d, nu):
    return (KND_decoder(k_construct, wave, d)*nu)

#3. Расчет КУ приемной антенны, дБ:
"""
k_construct - коэффициент, зависящий от конструкции, качества выполнения антенны и уровня ее потерь
wave - длина волны, м
d - диаметр антенны (прд/прм), м
goodness - добротность приемного средства дБ
T -шумовая температура приемного устройства, выраженная в К
ang - значения угла отклонения от оси ДН, град
"""
def KU_encoder (k_construct, wave, d, goodness, T, ang):
    try:
        g_max = goodness + 10*math.log(T)
        g_l = 2+15*math.log(d/wave)
        ang_m = 20*wave/d*math.sqrt(g_max-g_l)
        if d/wave>=100:
            ang_r = 15.85*((d/wave)**(-0.6))
            if ang>0 and ang<ang_m:
                return (g_max-2.5*0.001*((ang*d/wave)**2))
            elif ang>=ang_m and ang<ang_r:
                return (g_l)
            elif ang>=ang_r and ang<48:
                return (32-25*math.log(ang))
            elif ang>=48 and ang<180:
                return (-10)
            else:
                print ("Некорректное значение ула отклонения от оси")
        elif d/wave<100:
            ang_r = 100*(d/wave)
            if ang>0 and ang<ang_m:
                return (g_max-2.5*0.001*((ang*d/wave)**2))
            elif ang>=ang_m and ang<ang_r:
                return (g_l)
            elif ang>=ang_r and ang<48:
                return (52-10*math.log(d/wave)-25*math.log(ang))
            elif ang>=48 and ang<180:
                return (10-10*math.log(d/wave))
            else:
                print ("Некорректное значение ула отклонения от оси")
        else:
            print ("Ошибка входных данных")
    except:
        
        print ('Введено некорректное число параметров')



"""
k_construct - коэффициент, зависящий от конструкции, качества выполнения антенны и уровня ее потерь
wave - длина волны, м
d - диаметр антенны (прд/прм), м
nu - КПД
ang - значения угла отклонения от оси ДН, град
"""
def KU_encoder_without_goodness (k_construct, wave, d, nu, ang):
    g_max = KND_decoder(k_construct, wave, d)*nu
    g_l = 2+15*math.log(d/wave)
    ang_m = 20*wave/d*math.sqrt(g_max-g_l)
    if d/wave>=100:
        ang_r = 15.85*((d/wave)**(-0.6))
        if ang>0 and ang<ang_m:
            return (g_max-2.5*0.001*((ang*d/wave)**2))
        elif ang>=ang_m and ang<ang_r:
            return (g_l)
        elif ang>=ang_r and ang<48:
            return (32-25*math.log(ang))
        elif ang>=48 and ang<180:
            return (-10)
        else:
            print ("Некорректное значение ула отклонения от оси")
    elif d/wave<100:
        ang_r = 100*(d/wave)
        if ang>0 and ang<ang_m:
            return (g_max-2.5*0.001*((ang*d/wave)**2))
        elif ang>=ang_m and ang<ang_r:
            return (g_l)
        elif ang>=ang_r and ang<48:
            return (52-10*math.log(d/wave)-25*math.log(ang))
        elif ang>=48 and ang<180:
            return (10-10*math.log(d/wave))
        else:
            print ("Некорректное значение ула отклонения от оси")
    else:
        print ("Ошибка входных данных")

##2.1.2 Расчет числовых значений характеристик активной фазированной антенной решетки с использованием ее направленных свойств
"""
az - значение азимута
ang_location - значение угла местности
wave - длина волны, м
d - диаметр антенны (прд/прм), м
"""
#Расчет сдвиг фаз между токами соседних вибраторов в азимутальной плоскойсти
def _shift_vibro_az(wave, d, az, ang_location):
    return ((2*math.pi*d)/wave*math.sin(math.radians(az))*math.cos(math.radians(ang_location)))


#Расчет сдвиг фаз между токами соседних вибраторов в угломерной плоскойсти
def _shift_vibro_ang(wave, d, az, ang_location):
    return ((2*math.pi*d)/wave*math.sin(math.radians(az))*math.sin(math.radians(ang_location)))

#Расчет нормированной амплитудной характеристики направленности АР
"""
az - значение азимута
ang_location - значение угла места
"""
def norm_feature_AFAR(wave, d_1, d_2, L, n_1, n_2, nu, az, ang_location, shift_vibro_az, shift_vibro_ang):
    az = radians(az)
    ang_location = radians(ang_location)
    a1 = (cos(2*pi*L*sin(az)*sin(ang_location)/wave) - cos(2*pi*L/wave))/(sqrt(1-sin(az**2)*sin(ang_location**2)))
    a2 = sin(n_1*(2*pi*d_1*sin(az)*cos(ang_location)/wave - shift_vibro_az)/2)/sin((2*pi*d_1*sin(az)*cos(ang_location)/wave - shift_vibro_az)/2)
    a3 = sin(n_2*(2*pi*d_2*sin(az)*sin(ang_location)/wave - shift_vibro_ang)/2)/sin((2*pi*d_2*sin(az)*sin(ang_location)/wave - shift_vibro_ang)/2)
    return  (fabs(a1*a2*a3)/(n_1*n_2))  
    
#Исходные данные

# c = 3*(10**8)
# f = 1.575*(10**9)
# wave_1 = c/f
# d_1 = 1.2*wave_1
# L = 0.25*wave_1
# d_2 = 1.2*wave_1
# n_1 = 134
# n_2 = 134
# nu = 0.4
# N = n_1*n_2
# az = 80
# ang_location = 180
"""

#Для азимутальной плоскости
shift_vibro_az = _shift_vibro_az(wave_1, d_1, az, ang_location)

#Для угломерной плоскости
shift_vibro_ang = _shift_vibro_ang(wave_1, d_2, az, ang_location)


#Расчет нормированной амплитудной характеристики направленности АР
list_norm_feature_AFAR =[]
for i in np.arange(0,360,0.9):
    try:
        list_norm_feature_AFAR.append(norm_feature_AFAR(wave_1, d_1, d_2, L, n_1, n_2, nu, i, 180, shift_vibro_az, shift_vibro_ang))
    except ZeroDivisionError:
        list_norm_feature_AFAR.append(1)

# list_norm_feature_AFAR =[]
# for i in np.arange(0,360,0.9):
    # list_norm_feature_AFAR.append(norm_feature_AFAR(wave_1, d_1, d_2, L, n_1, n_2, nu, i, 180, shift_vibro_az, shift_vibro_ang))




x = np.arange(0,360)
y = list_norm_feature_AFAR
fig = go.Figure(data=go.Scatter(x=x, y=y, line=dict(color='red')))
fig.show()


trace = go.Scatterpolar(
   r = list_norm_feature_AFAR,
   theta = list(np.arange(0,360)),
   mode = 'lines',
   line_color = 'red',
)
data = [trace]
fig = go.Figure(data = data)
fig.show()


"""

#5. Расчет амплитудной характеристики направленности вибратора (ненормированная амплитудная характеристика направленности АР)
def f_10(wave, L, az, ang_location):
    return fabs((cos(2*pi/wave*L*(sin(2*pi*ang_location/360)*sin(az))) - cos(2*pi*L/wave))/sqrt(1-sin((2*pi*ang_location/360)**2)*sin(az**2)))

"""

list_f_10 =[]
for i in np.arange(0,360):
    try:
        #print (i, norm_feature_AFAR(wave_1, d_1, d_2, L, n_1, n_2, nu, i, 360, shift_vibro_az, shift_vibro_ang))
        list_f_10.append(f_10(wave_1, L, az, i))
    except ZeroDivisionError:
        print ('Error', i)
        list_f_10.append(1)


trace = go.Scatterpolar(
   r = list_f_10,
   theta = list(np.arange(0,360)),
   mode = 'lines',
   line_color = 'red',
)
data = [trace]
fig = go.Figure(data = data)
fig.show()

"""
#6. Расчет множителя системы в случае синфазного и равноамплитудного возбуждения вибраторов
def f_20(wave, d_1, d_2, n_1, n_2, az, ang_location):
    a1 = sin(n_1*2*pi*d_1*sin(az)*cos(2*pi*ang_location/360)/wave*2)/sin(2*pi*d_1*sin(az)*cos(2*pi*ang_location/360)/wave*2)
    a2 = sin(n_2*2*pi*d_2*sin(az)*cos(2*pi*ang_location/360)/wave*2)/sin(2*pi*d_2*sin(az)*cos(2*pi*ang_location/360)/wave*2)
    return fabs(a1*a2)


#7. Расчет КНД в направлении максимального излучения АФАР, Вт:
def D_0(wave, d_1, d_2, L, n_1, n_2, az, ang_location):
    a1 = 4*pi*((n_1*n_2)**2)
    f = lambda az, ang_location: sin((az))*((f_10(wave, L, az, ang_location)*f_20(wave, d_1, d_2, n_1, n_2, az, ang_location))**2)
    a2 = integrate.dblquad(f, 0, 2*pi, lambda az: 0, lambda az: pi)[0]
    return a1/a2

"""
#8. Переводим значение КНД АФАР в дБ
10*log(D_0(wave_1, d_1, d_2, L, n_1, n_2, az, ang_location),10)


#9. Вычисляем коэффициент усиления (КУ) АФАР, Вт:
nu*D_0(wave_1, d_1, d_2, L, n_1, n_2, az, ang_location)


#10. Переводим значения КУ АФАР в дБ:
10*log(nu*D_0(wave_1, d_1, d_2, L, n_1, n_2, az, ang_location),10)
"""