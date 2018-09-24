import urllib.parse
import urllib.request
import urllib.error
import itertools
import operator
import numpy
import sys
import warnings
import csv
from MonthlyVectors import *
from scipy import linspace, polyval, polyfit, sqrt, stats, randn
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication)


# ==================================================================================================================== #
#                                               API                                                                    #
# ==================================================================================================================== #
def api_fun(**kwargs):
    kwargs['start'] = start
    kwargs['end'] = end
    kwargs['token'] = token
    kwargs['radius'] = radius_
    kwargs['network'] = nw
    kwargs['vars'] = variable_flag

    qsp = urllib.parse.urlencode(kwargs, doseq=True)
    resp = urllib.request.urlopen(base_url + endpoint + '?' + qsp).read()
    #
    response = json.loads(resp.decode('utf-8'))
    return response
# ==================================================================================================================== #
def api_fun_date(**kwargs):
    kwargs['start'] = start
    kwargs['end'] = end
    kwargs['token'] = token
    kwargs['radius'] = radius_
    kwargs['network'] = nw
    kwargs['vars'] = variable_flag
    kwargs['obtimezone'] = 'local'
    #
    print(start)
    print(end)
    qsp = urllib.parse.urlencode(kwargs, doseq=True)
    resp = urllib.request.urlopen(base_url + endpoint + '?' + qsp).read()
    #
    response = json.loads(resp.decode('utf-8'))
    return response
# ==================================================================================================================== #
# ==================================================================================================================== #
#                                             Weights                                                                #
# ==================================================================================================================== #
def weights_fun(Var_timestep, lat_station, long_station):
    distance_lat = []
    distance_long = []

    for i in range(0, len(lat_station)):
        distance_lat.append(lat - float(lat_station[i]))
        distance_long.append(long - float(long_station[i]))
    flag = 0
    for i in range(0, len(distance_lat)):
        if distance_lat[i] == 0 and distance_long[i] == 0:
            var_weighted = Var_timestep[i]
            flag = 3
    #
    if flag == 3:
        nothing = 1
    elif len(Var_timestep) == 1:
        var_weighted = Var_timestep[0]
    else:
        (ar, br) = polyfit(distance_lat, Var_timestep, 1)
        var_lat = br
        (ar, br) = polyfit(distance_long, Var_timestep, 1)
        var_long = br
        var_weighted = (var_lat + var_long)/2

    return var_weighted
# ==================================================================================================================== #
#                                             TIMEZONE
# ==================================================================================================================== #
def get_timezone(start_in, end_in):

    global start, end
    start = start_in
    end = end_in
    print(start)
    print(end)

    try:
        allstationdata_local = api_fun_date()
        Date_local = allstationdata_local['STATION'][0]['OBSERVATIONS']['date_time']
        [year_local, month_local, day_local, hh_local, mm_local] = date_break(Date_local)

        allstationdata = api_fun()
        Date_UTC = allstationdata['STATION'][0]['OBSERVATIONS']['date_time']
        [year_UTC, month_UTC, day_UTC, hh_UTC, mm_UTC] = date_break(Date_UTC)
        #
    except (IndexError):
        tz = QInputDialog.getText(None, 'Input Dialog', 'What is your Time Zone')
        TimeZone = int(tz[0])
    else:
        y_local = year_local[0]
        y_UTC = year_UTC[0]
        hh_local = hh_local[0]
        hh_UTC = hh_UTC[0]

        Delta_year = y_local - y_UTC
        TimeZone = -1 * (24 - hh_local - hh_UTC)



    return TimeZone

# ==================================================================================================================== #
# ==================================================================================================================== #
#                                             Months
# ==================================================================================================================== #
def months_fun(date_mw, TimeZone):
    global start_vec, end_vec, month_days
    if date_mw % 4 == 0 and date_mw % 100 != 0 or date_mw % 400 == 0:
        leap = 0  # Leap year
    else:
        leap = 0  # NOT leap year
    year = date_mw * 100000000
    #
    start_vec = []
    end_vec = []
    month_days = []

    if TimeZone <= 0:
        Shift_start = TimeZone * -100
        #
        # January
        start_vec.append(str(year + 1010000 + Shift_start))
        end_vec.append(str(year + 2010000 + Shift_start))
        month_days.append(31)
        # February
        start_vec.append(str(year + 2010005 + Shift_start))
        end_vec.append(str(year + 3010000 + Shift_start))
        if leap == 1:
            month_days.append(29)
        else:
            month_days.append(28)
        # March
        start_vec.append(str(year + 3010005 + Shift_start))
        end_vec.append(str(year + 4010000 + Shift_start))
        month_days.append(31)
        # April
        start_vec.append(str(year + 4010005 + Shift_start))
        end_vec.append(str(year + 5010000 + Shift_start))
        month_days.append(30)
        # May
        start_vec.append(str(year + 5010005 + Shift_start))
        end_vec.append(str(year + 6010000 + Shift_start))
        month_days.append(31)
        # June
        start_vec.append(str(year + 6010005 + Shift_start))
        end_vec.append(str(year + 7010000 + Shift_start))
        month_days.append(30)
        # July
        start_vec.append(str(year + 7010005 + Shift_start))
        end_vec.append(str(year + 8010000 + Shift_start))
        month_days.append(31)
        # August
        start_vec.append(str(year + 8010005 + Shift_start))
        end_vec.append(str(year + 9010000 + Shift_start))
        month_days.append(31)
        # September
        start_vec.append(str(year + 9010005 + Shift_start))
        end_vec.append(str(year + 10010000 + Shift_start))
        month_days.append(30)
        # October
        start_vec.append(str(year + 10010005 + Shift_start))
        end_vec.append(str(year + 11010000 + Shift_start))
        month_days.append(31)
        # November
        start_vec.append(str(year + 11010005 + Shift_start))
        end_vec.append(str(year + 12010000 + Shift_start))
        month_days.append(30)
        # December
        start_vec.append(str(year + 12010005 + Shift_start))
        if leap == 1:
            end_vec.append(str(year + 12310000 + Shift_start))
            month_days.append(30)
        else:
            end_vec.append(str(year + 100000000 + 1010000 + Shift_start))
            month_days.append(31)

    else:
        Shift_start = TimeZone * 100
        #
        # January
        start_vec.append(str(year - 100000000 + 12310000 + 2400 - Shift_start))
        end_vec.append(str(year + 1310000 + 2400 - Shift_start))
        month_days.append(31)
        # February
        start_vec.append(str(+ 1310005 + 2400 - Shift_start))
        if leap == 1:
            month_days.append(29)
            end_vec.append(str(year + 2290000 + 2400 - Shift_start))
            # March
            start_vec.append(str(year + 2290005 + 2400 - Shift_start))
        else:
            month_days.append(28)
            end_vec.append(str(year + 2280000 + 2400 - Shift_start))
            # March
            start_vec.append(str(year + 2280005 + 2400 - Shift_start))
        end_vec.append(str(year + 3310000 + 2400 - Shift_start))
        month_days.append(31)
        # April
        start_vec.append(str(year + 3310005 + 2400 - Shift_start))
        end_vec.append(str(year + 4300000 + 2400 - Shift_start))
        month_days.append(30)
        # May
        start_vec.append(str(year + 4300005 + 2400 - Shift_start))
        end_vec.append(str(year + 5310000 + 2400 - Shift_start))
        month_days.append(31)
        # June
        start_vec.append(str(year + 5310005 + 2400 - Shift_start))
        end_vec.append(str(year + 6300000 + 2400 - Shift_start))
        month_days.append(30)
        # July
        start_vec.append(str(year + 6300005 + 2400 - Shift_start))
        end_vec.append(str(year + 7310000 + 2400 - Shift_start))
        month_days.append(31)
        # August
        start_vec.append(str(year + 7310005 + 2400 - Shift_start))
        end_vec.append(str(year + 8310000 + 2400 - Shift_start))
        month_days.append(31)
        # September
        start_vec.append(str(year + 8310005 + 2400 - Shift_start))
        end_vec.append(str(year + 9300000 + 2400 - Shift_start))
        month_days.append(30)
        # October
        start_vec.append(str(year + 9300005 + 2400 - Shift_start))
        end_vec.append(str(year + 10310000 + 2400 - Shift_start))
        month_days.append(31)
        # November
        start_vec.append(str(year + 10310005 + 2400 - Shift_start))
        end_vec.append(str(year + 11300000 + 2400 - Shift_start))
        month_days.append(30)
        # December
        start_vec.append(str(year + 11300005 + 2400 - Shift_start))
        if leap == 1:
            end_vec.append(str(year + 12300000 + 2400 - Shift_start))
            month_days.append(30)
        else:
            end_vec.append(str(year + 12310000 + 2400 - Shift_start))
            month_days.append(31)


# ==================================================================================================================== #
#                                           Check Matrix
#  ==================================================================================================================== #
def check_matrix(Matrix):
    #
    for i in range(0, len(Matrix[0])):
        row = []
        for j in range(0, len(Matrix)):
            row.append(Matrix[j][i])

# ==================================================================================================================== #
#                                           Write CSV file
#  ==================================================================================================================== #
def mw_csv_fun(Matrix, variable_names, path):
    OPFILE = path + '.csv'
    ofile = open(OPFILE, "w", newline='')
    writer = csv.writer(ofile, delimiter=',')
    #
    writer.writerow(variable_names)
    #
    for i in range(0, len(Matrix[0])):
        row = []
        for j in range(0, len(Matrix)):
            row.append(Matrix[j][i])
        writer.writerow(row)
    ofile.close()

# ====================================================================================================================================================================================================================================== #
# ====================================================================================================================================================================================================================================== #
def MesoWest_fun(lat_inp, long_inp, rad, variable_flag_inp, year_start, year_end, nw_inp):
    global token, base_url, geo_criteria, station, start, end, endpoint, radius_, nw, delta_holes_threshold, flag_numb_stations_year, variable_flag, lat, long
    lat = lat_inp
    long = long_inp
    variable_flag = variable_flag_inp
##########################################################
    token = 'ca01203d0c9746cd998ee8d0007fdf07'
    base_url = 'http://api.mesowest.net/v2/'
    endpoint = 'stations/timeseries'
    # delta_holes_threshold = 2000
    delta_holes_threshold = 20
    flag_numb_stations_year = 0
    radius_ = [lat, long, rad]
    nw = nw_inp
    delta_years = int(year_end - year_start)
    years = []
    for i in range(0, delta_years+1):
        years.append(year_start + i)
    #
    # Get Timezone
    start_tz = str(years[0] * 100000000 + 1010000)
    end_tz = str(years[0] * 100000000 + 2010000)
    TimeZone = get_timezone(start_tz, end_tz)
    print('Timezone: ' + str(TimeZone))
    #
    MultipleYears = []
    year_added = 0
    for w in range(0, len(years)):              #Loop over multiple years
        date_mw = years[w]
        months_fun(date_mw, TimeZone)
        #*******************************************************************************************************
        Variable_year = []
        global distance, code_station, elevation, lat_station, long_station, comp_distance
        for j in range(0, 12):              #Loop over multiple months
            start = start_vec[j]
            end = end_vec[j]
            allstationdata = api_fun()
            numb_stats = allstationdata['SUMMARY']['NUMBER_OF_OBJECTS']
            print('numb stats initially')
            print(numb_stats)
            print('variable flag')
            print(variable_flag)
            print('coordinates')
            print(radius_)
            ###################################
            if numb_stats is 0:                      #this means there are no data available for this month, so the year cannot be completed
                # flag_numb_stations = 3
                break
            else:
                # numb_stats = len(allstationdata['STATION'])
                Stations_Vars = []
                distance = []
                code_station = []
                elevation = []
                lat_station = []
                long_station = []
                comp_distance = []
                for i in range(0, numb_stats):              #Loop over multiple stations
                    try:
                        Date = allstationdata['STATION'][i]['OBSERVATIONS']['date_time']
                    except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                        delta_holes = 1000
                    else:
                        #**********************************************************************************************
                        if variable_flag == 'air_temp':
                            delta_holes = 0
                            try:
                                Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['air_temp_set_0'])
                            except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                try:
                                    Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['air_temp_set_1'])
                                except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                    try:
                                        Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['air_temp'])
                                    except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                        delta_holes = 1000
                        #**********************************************************************************************
                        if variable_flag == 'relative_humidity':
                            delta_holes = 0
                            try:
                                Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['relative_humidity_set_0'])
                            except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                try:
                                    Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['relative_humidity_set_1'])
                                except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                    try:
                                        Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['relative_humidity'])
                                    except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                        delta_holes = 1000
                        #**********************************************************************************************
                        if variable_flag == 'dew_point_temperature':
                            delta_holes = 0
                            try:
                                Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['dew_point_temperature_set_0d'])
                            except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                try:
                                    Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['dew_point_temperature_set_1d'])
                                except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                    try:
                                        Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['dew_point_temperature'])
                                    except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                        delta_holes = 1000
                        #**********************************************************************************************
                        if variable_flag == 'wind_direction':
                            delta_holes = 0
                            try:
                                Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['wind_direction_set_0'])
                            except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                try:
                                    Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['wind_direction_set_1'])
                                except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                    try:
                                        Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['wind_direction'])
                                    except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                        delta_holes = 1000
                        # **********************************************************************************************
                        if variable_flag == 'wind_speed':
                            delta_holes = 0
                            try:
                                Select_variable = (
                                allstationdata['STATION'][i]['OBSERVATIONS']['wind_speed_set_0'])
                            except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                try:
                                    Select_variable = (
                                    allstationdata['STATION'][i]['OBSERVATIONS']['wind_speed_set_1'])
                                except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                    try:
                                        Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['wind_speed'])
                                    except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                        delta_holes = 1000
                        # **********************************************************************************************
                        if variable_flag == 'pressure':
                            delta_holes = 0
                            try:
                                Select_variable = (
                                allstationdata['STATION'][i]['OBSERVATIONS']['pressure_set_0'])
                            except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                try:
                                    Select_variable = (
                                    allstationdata['STATION'][i]['OBSERVATIONS']['pressure_set_1'])
                                except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                    try:
                                        Select_variable = (allstationdata['STATION'][i]['OBSERVATIONS']['pressure'])
                                    except (ValueError, RuntimeError, TypeError, NameError, KeyError):
                                        delta_holes = 1000
                        #**********************************************************************************************

                    if delta_holes == 0:
                        # print('Select Variable')
                        # print(Select_variable)
                        try:
                            (Var_output, delta_holes) = hourlydata(Select_variable, Date, month_days[j],
                                                                   delta_holes_threshold, TimeZone)
                        except (IndexError, KeyError):
                            delta_holes = 100
                        else:
                            nothing = 1

                    if delta_holes <= delta_holes_threshold:
                        Stations_Vars.append(Var_output)
                        code_station.append(allstationdata['STATION'][i]['STID'])
                        # print(allstationdata['STATION'][i]['STID'])
                        distance.append(allstationdata['STATION'][i]['DISTANCE'])
                        elevation.append(allstationdata['STATION'][i]['ELEVATION'])
                        lat_station.append(allstationdata['STATION'][i]['LATITUDE'])
                        long_station.append(allstationdata['STATION'][i]['LONGITUDE'])

                if len(Stations_Vars) > 0:
                    Vec_average = []
                    for h in range(0, len(Stations_Vars[0])):
                        Var_timestep = []
                        for i in range(0, len(Stations_Vars)):
                            Var_timestep.append(Stations_Vars[i][h])
                        Var_average_i = weights_fun(Var_timestep, lat_station, long_station)
                        Vec_average.append(Var_average_i)
                    Variable_year = Variable_year + Vec_average             #add month to the year
                else:
                    numb_stats = 0
                    break
        # End of the year
        print('numb_stats and month/year')
        print(numb_stats)
        print(j)
        print(date_mw)
        if numb_stats > 0:          #If every month was full of data with an acceptable number of holes
            MultipleYears.append(Variable_year)
            year_added = year_added + 1
    # End of multiple years
    print('len multipleyears')
    print(len(MultipleYears))
    if len(MultipleYears) < 1:
        flag_numb_stations_year = 5
        years_data_empty = 5
        return [], years_data_empty
    else:
        Average_Over_Years = []
        for i in range(0, len(MultipleYears[0])):
            variable_buffer = 0
            for j in range(0, len(MultipleYears)):
                variable_buffer = variable_buffer + MultipleYears[j][i]
            Average_Over_Years.append(variable_buffer/len(MultipleYears))
        years_data_empty = 0
        return Average_Over_Years, years_data_empty
#