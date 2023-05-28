import sys
import numpy as np
import scipy as sp
import scipy.constants
import matplotlib.pyplot as plt
import matplotlib.pylab
import matplotlib.patches
import cartopy.crs as ccrs
from matplotlib.dates import DateFormatter
import ephem
import requests
import cartopy

def calcSatPosData(sat, observer, start_time, end_time, res_time):
  """
  Calculates and returns a table with the columns timestamp, latitude,
  longitude, elevation, azimuth and distance.

  Parameters
  ----------
  sat: ephem.EarthSatellite
  satellite to do the calculations for
  observer: ephem.Observer
  Position on earth for time reference
  start_time: float
  "Dublin Julian Day" starting times
  end_time: float
  "Dublin Julian Day" ending times
  res_time: float
  "Dublin Julian Day" resolution
  Returns
  -------
  subsat_pints: array_like
  array in the format [[time, longitude, latitude, elevation,
  azimuth, distance]],
  latitudes and longitudes in rad, time as "Dublin Julian Day".

  Version
  -------
  0.2
  """
  #check parameters to avoid infinite loop
  #if(end_time <= start_time):
  # raise Exception("Given end_time lies further in the past than start_time")
  if(res_time <= 0):
    raise Exception("Given res_time is negative, 0, or too small for calculation")
  calc_time = start_time
  longs = []
  lats = []
  elevs = []
  azs = []
  dists = []
  times = []

  while calc_time <= end_time:
    #calculate data
    observer.date = calc_time
    sat.compute(observer)
    #save data
    times.append(observer.date)
    longs.append(sat.sublong*180/np.pi)
    lats.append(sat.sublat*180/np.pi)
    elevs.append(sat.alt*180/np.pi)
    azs.append(sat.az*180/np.pi)
    dists.append(sat.range)

    #increment time
    calc_time += res_time

    subsat_points = [times, longs, lats, elevs, azs, dists]

  return subsat_points


# In[50]:


def calcVisibleWindows(alts, min_alt):
  """
  Calculates the ranges in which the satellite is above the given
  minimum altitude.

  Parameters
  -------------
  data: array_like [altitude]
  Containes altitude values for the calculation window
  min_alt: float
  Minimum altitude angle at which the sat is counted as visible

  Returns
  -----------
  visible_times: array_like [start_index, end_index]
  Table in which each row represents a part of the given altitude
  array
  in which the sat is above the minimum altitude

  Version
  --------
  0.1
  """
  visible_windows = []
  current_window = [0,0]

  last_state = False
  for i in range(len(alts)):
    #Change of state invisible -> visible
    if alts[i] >= min_alt and last_state == False:
      current_window[0] = i
    #Change of state visible -> invisible
    if alts[i] < min_alt and last_state == True:
      current_window[1] = i-1
      visible_windows.append(current_window[:])
    #Cover case in which last element is visible
    if i == len(alts)-1 and alts[i] >= min_alt:
      current_window[1] = i
      visible_windows.append(current_window)
    #Refresh last state
    last_state = alts[i] >= min_alt


  return visible_windows


# In[51]:


def getEquatorialCrossing(lats):
  """
  Calculates the indexes of the given list of latitudes, where it crosses
  the equator

  Parameters
  -------------
  data: array_like
  Latitude values

  Returns
  -----------
  equatorial_crossings: array_like
  List of indexes for the given list of latitudes where the sat
  crosses
  the equator. Index values is alway the point after the crossing.

  Version
  --------
  0.1
  """
  last_state = lats[0] >= 0
  indexes = []
  for i in range(len(lats)):
    if lats[i] >= 0 and last_state == False:
      indexes.append(i)
    if lats[i] < 0 and last_state == True:
      indexes.append(i)
    last_state = lats[i] >= 0
  return indexes
tle_full="""GONETS M-6
1 39250U 13048B   20074.77987361 +.00000039 +00000-0 +21357-3 0  9999
2 39250 082.4887 328.6723 0017628 187.2880 172.7957 12.42939841295149"""

def TLE_RAW(tle_full):
    np.set_printoptions(threshold=sys.maxsize)
    #font = {'family' : 'normal',   'weight' : 'normal', 'size' : 8}
    #matplotlib.rc('font', **font)
    #User Parameters
    #-------------------------------------------------------------------
    sat_id = 23802 #Satellite id
    start_time = ephem.Date((2020,3,19)) #Calculation start time
    end_time = start_time + 1.0 #Calculation end time
    res_time = ephem.minute*1 #Calculation time resolution
    observer_lon ="60.801694" #"47.530485" #"60.801694" #Logitude of ground station [deg]
    observer_lat = "59.079296"# "80.794714"#"59.079296" #Latitude of ground station [deg]
    gs_name = "ТОЧКА" #Name of ground station
    min_alt_for_comm = 7 #Minimum elevation angle for communication [deg]
    center_freq = 8345e6 #Transmission center frequency [Hz]
    myformat = DateFormatter('%d %b %H:%M') #Date format
    #Setup
    #-------------------------------------------------------------------
    #Satellite

    #tle = getTle(sat_id)

    #mysat = ephem.readtle(tle[0], tle[1], tle[2])
    mysat = ephem.readtle(tle_full.split('\n')[0], tle_full.split('\n')[1], tle_full.split('\n')[2])
    #Observer
    observer = ephem.Observer()
    observer.lat = "89"
    observer.lon = "0"
    #Calculation
    #-------------------------------------------------------------------
    #contains: [times, longs, lats, alts, azs, dists]
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




    #
    #Print TLE:
    #%%-------------------------------------------------------------------
    print("TLE КА:")
    print(tle_full.split('\n')[0])
    print(tle_full.split('\n')[1])
    print(tle_full.split('\n')[2])
    print()
    #Вычисление параметров орбиты:
    #-------------------------------------------------------------------
    n = float(mysat._n) #средняя угловая скорость объекта на орбите [оборотов в день]
    my = 3.986e14 #стандартный гравитационный параметр
    a = (my**(1/3))/(((2*n*np.pi)/86400)**(2/3))
    ecc = float(mysat._e)
    inc = float(mysat._inc)*180/np.pi
    raan = float(mysat._raan)*180/np.pi
    ap = float(mysat._ap)*180/np.pi
    print("Элементы орбиты:")
    print("большая полуось [км]: " + str(a/1000))
    print("эксцентриситет: " + str(ecc))
    print("наклонение [град]: " + str(inc))
    print("долгота восходящего узла [град]: " + str(raan))
    print("аргумент перицентра [град]: " + str(ap))
    print("средняя аномалия: " + str(ap))
    print()
    #Время подключения:
    #%%-------------------------------------------------------------------
    print("Возможное коммуникационное окно:")
    for i in range(len(comm_windows_indexes)):
        start_index = comm_windows_indexes[i][0]
        print("Соединение на: " + myformat.format_data(data[0][start_index]-0.5) + ", продолжительностью: " + str(comm_times[i]/ephem.hour) + " часов.")
    lcw = comm_windows_indexes[longest_comm_window_index]
    fig, axes = plt.subplots(3, sharex=True, figsize=(5,10))
    axes[0].plot(data[0,lcw[0]:lcw[1]]-0.5, data[3,lcw[0]:lcw[1]])
    axes[0].grid()
    axes[0].set_title("Углы направления радиолинии, азимута и расстояние до спутника (" + str(tle_full.split('\n')[0]) + """) для коммуникационного окна с """ + myformat.format_data(start_time-0.5) + " по " + myformat.format_data(end_time-0.5) + ", для местоположения (" + observer_lon + ', ' + observer_lat + ")")
    axes[0].set_ylabel("Угол направления радиолинии, град.")
    axes[1].plot(data[0,lcw[0]:lcw[1]]-0.5, data[4,lcw[0]:lcw[1]])
    axes[1].grid()
    axes[1].set_ylabel("Угол азимутального положения, град.")
    axes[2].plot(data[0,lcw[0]:lcw[1]]-0.5, data[5,lcw[0]:lcw[1]])
    axes[2].grid()
    axes[2].set_ylabel("Расстояние, м")
    axes[2].xaxis.set_major_formatter(myformat)
    axes[2].set_xlabel("Дата и время")
    fig.autofmt_xdate()
    plt.show()
    #Визуализация доплеровского сдвига
    #%%-------------------------------------------------------------------
    plt.figure()
    plt.plot(data[0,lcw[0]:lcw[1]]-0.5, doppler_shift[lcw[0]:lcw[1]])
    plt.gca().xaxis.set_major_formatter(myformat)
    plt.gcf().autofmt_xdate()
    plt.grid()
    plt.ylabel("Частота доплеровского сдвига, Гц")
    plt.xlabel("Дата и время")
    plt.title("Доплеровский сдвиг для связи со спутником (" + str(tle_full.split('\n')[0]) + """) для коммуникационного окна с """ + myformat.format_data(start_time-0.5) + " по " + myformat.format_data(end_time-0.5) + ", для местоположения (" + observer_lon + ', ' + observer_lat + ")")

    plt.figure(figsize=[18,14])
    '''world_map = Basemap(projection=ccrs.PlateCarree(), resolution=None,
                width=8E6, height=8E6, 
                lat_0=45, lon_0=-100,)'''
    world_map = plt.axes(projection=ccrs.PlateCarree())
    world_map.stock_img()
    #Observer
    world_map.plot(observer.lon*180/np.pi, observer.lat*180/np.pi,"b*",ms=10,transform=ccrs.Geodetic(), label="observer")
    #Ground track
    world_map.plot(data[1],data[2],"r",ms=4,transform=ccrs.Geodetic(), label="ground track")
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
    plt.show()

    f = plt.figure(figsize=[18,18])
    world_map = plt.axes(projection=ccrs.Orthographic(50,90))
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
    #world_map.add_feature(cartopy.feature.LAND)
    #world_map.add_feature(cartopy.feature.OCEAN)
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
    plt.show()